from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# 전역 변수로 모델과 토크나이저를 한 번만 로드
_model = None
_tokenizer = None
_model_name = "helena29/Qwen2.5_LoRA_for_HTP"

def _load_model():
    """모델을 한 번만 로드 (싱글톤 패턴)"""
    global _model, _tokenizer
    
    if _model is None:
        print(f"🔥 Loading Qwen HTP Model: {_model_name}")
        print(f"🔍 CUDA Available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"🔍 CUDA Device: {torch.cuda.get_device_name(0)}")
            print(f"🔍 CUDA Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
        
        # 토크나이저 로드
        _tokenizer = AutoTokenizer.from_pretrained(_model_name)
        
        # 모델 로드 (LoRA 어댑터가 이미 병합된 상태)
        _model = AutoModelForCausalLM.from_pretrained(
            _model_name,
            device_map="auto",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        
        print(f"✅ Qwen HTP Model loaded successfully!")
        print(f"✅ Model Device: {_model.device}")
    
    return _model, _tokenizer


def _clean_output(text: str) -> str:
    """
    모델 출력 후처리: 불필요한 텍스트 제거 및 불완전한 문장 처리
    """
    import re
    
    # 따옴표나 마크다운 코드 블록 제거
    text = text.strip('`"\'').strip()
    
    # "Output:", "Answer:", "Response:" 같은 프리픽스 제거
    text = re.sub(r'^(Output|Answer|Response|Result):\s*', '', text, flags=re.IGNORECASE)
    
    # 연속된 공백이나 줄바꿈 정리
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    
    # 불완전한 문장 감지 및 제거
    text = text.strip()
    if text and text[-1] not in '.!?。':
        # 마지막 완전한 문장 부호 찾기
        last_complete_idx = -1
        for i in range(len(text) - 1, -1, -1):
            if text[i] in '.!?。':
                last_complete_idx = i
                break
        
        # 완전한 문장이 있으면 거기까지만 유지
        if last_complete_idx > 0:
            text = text[:last_complete_idx + 1]
    
    return text.strip()


def generate_with_qwen(prompt: str):
    """
    Qwen 모델을 사용해 텍스트 생성
    모델은 최초 1회만 로드되고 재사용됨
    """
    # 모델 로드 (이미 로드되어 있으면 재사용)
    model, tokenizer = _load_model()
    
    print("=" * 80)
    print("📝 [PROMPT] 해석 생성 프롬프트:")
    print("-" * 80)
    print(prompt)
    print("=" * 80)
    
    print(f"🔍 [generate_with_qwen] Model device: {model.device}")
    
    # 입력 텐서 준비
    inputs = tokenizer(prompt, return_tensors="pt")
    
    # 모든 입력을 모델과 같은 디바이스로 이동
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    
    print(f"🔍 [generate_with_qwen] Input device: {inputs['input_ids'].device}")
    
    # 생성 - fine-tuned 모델에 최적화된 파라미터
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=500,   # 적절한 길이로 조정
            min_new_tokens=150,   # 최소 길이 보장
            temperature=0.3,     # 약간 낮춰서 일관성 향상
            top_p=0.9,            # nucleus sampling 추가
            do_sample=True,
            repetition_penalty=1.15,  # 반복 방지 강화
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3  # 3-gram 반복 방지
        )
    
    # 프롬프트 제거: 입력 토큰 이후만 추출
    input_len = inputs["input_ids"].shape[1]
    generated_ids = outputs[0][input_len:]
    
    result = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
    
    # 출력 후처리
    result = _clean_output(result)
    
    print(f"✅ [generate_with_qwen] Generated {len(result)} characters")
    
    return result
