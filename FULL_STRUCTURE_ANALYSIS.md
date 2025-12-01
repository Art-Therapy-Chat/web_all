# 🔍 전체 구조 분석 및 수정 사항

## 📊 데이터 플로우 (Data Flow)

```
[사용자 입력]
    ↓
[1. 그림 그리기] 
    → drawings: { house: base64, tree: base64, person: base64 }
    ↓
[2. 캡션 생성] /caption
    Input:  image_base64 (string)
    Output: { "caption": "{\"ko\": [\"...\", \"...\"], \"en\": [\"...\", \"...\"]}" }
    ↓
[3. 프론트엔드 파싱]
    captionObj.ko → join(', ') → 화면 표시용
    captionObj.en → join('. ') → 해석용
    ↓
[4. RAG 검색] /rag
    Input:  { caption: string (한국어), image_type: "집"|"나무"|"사람" }
    Output: { rewritten_queries: [...], rag_docs: [...] }
    ↓
[5. 개별 해석] /interpret_single
    Input:  { caption: string (영어), rag_docs: [...], image_type: "집"|"나무"|"사람" }
    Process: Qwen 모델 → 영어 해석 생성
    Output: { interpretation: string (영어) }
    ↓
[6. 번역] /translate
    Input:  { text: string (영어) }
    Output: { translated: string (한국어) }
    ↓
[7. State 저장]
    interpretations: { house: "한국어", tree: "한국어", person: "한국어" }
    interpretationsEN: { house: "English", tree: "English", person: "English" }
    ↓
[8. 질문 생성] /questions
    Input:  { conversation: [...], interpretations: interpretationsEN (영어!) }
    Process: Qwen 모델 → 영어 질문 생성
    Output: { question: string (영어) }
    ↓
[9. 질문 번역] /translate
    Input:  { text: string (영어) }
    Output: { translated: string (한국어) }
    ↓
[10. 사용자 응답]
    → 5회 반복 → [8-9]
    ↓
[11. 최종 해석] /interpret_final
    Input:  { 
      single_results: { house: "한국어", tree: "한국어", person: "한국어" },
      conversation: [...],
      user_info: { name, age, gender }
    }
    Process: GPT-4o → 한국어 종합 해석
    Output: { final: string (한국어) }
```

---

## ✅ 수정된 문제점

### 1. **캡션 형식 불일치** (FIXED ✅)

**문제**:
```python
# 에러 케이스
return json.dumps({"ko": "", "en": ""})  # ❌ 문자열

# 프론트엔드 기대
Array.isArray(captionObj.ko)  # ❌ false → 에러
```

**해결**:
```python
# 모든 에러 케이스를 배열로 통일
return json.dumps({"ko": ["이미지를 읽을 수 없습니다"], "en": ["Unable to read image"]})
```

---

### 2. **질문 생성에 한국어 해석 전달** (FIXED ✅)

**문제**:
```javascript
// ❌ 한국어 번역본 전달
interpretations: {
  house: "집은 크고...",  // 한국어
  tree: "나무는...",
  person: "사람은..."
}
```

**해결**:
```javascript
// ✅ 영어 원본 전달
interpretationsEN: {
  house: "The house is large...",  // English
  tree: "The tree has...",
  person: "The person shows..."
}

// 질문 생성 시
body: JSON.stringify({
  conversation: currentHistory,
  interpretations: interpretationsEN  // ✅ 영어 원본
})
```

---

### 3. **RAG 문서 타입 검증 부족** (FIXED ✅)

**문제**:
```python
# rag_docs가 리스트가 아닐 경우 에러 가능
ref_docs = "\n".join([f"- {doc[:300]}" for doc in req.rag_docs[:3]])
```

**해결**:
```python
if isinstance(req.rag_docs, list):
    ref_docs = "\n".join([f"- {str(doc)[:300]}" for doc in req.rag_docs[:3]])
    logger.info(f"✅ RAG 문서 {len(req.rag_docs[:3])}개를 참고하여 해석")
else:
    logger.warning(f"⚠️  RAG 문서 형식 오류: {type(req.rag_docs)}")
```

---

### 4. **프롬프트 컨텍스트 구성 개선** (FIXED ✅)

**문제**:
```python
# 항상 "Context:" 라벨 사용
Context:
{conversation_text}
{interp_text}
```

**해결**:
```python
# 대화 여부에 따라 적절한 라벨 사용
if conversation_text.strip():
    context_section = f"Previous Conversation:\n{conversation_text}\n{interp_text}"
else:
    context_section = f"Drawing Analysis:{interp_text}"
```

---

## 🔄 프론트엔드 ↔ 백엔드 통신 검증

### ✅ API 1: `/caption`
```javascript
// Request (Frontend)
{ image_base64: "iVBORw0KGgo..." }

// Response (Backend)
{ caption: "{\"ko\": [...], \"en\": [...]}" }  // JSON string

// Parsing (Frontend)
const captionObj = JSON.parse(capJson.caption);
// ✅ captionObj = { ko: ["...", "..."], en: ["...", "..."] }
```

### ✅ API 2: `/rag`
```javascript
// Request (Frontend)
{ 
  caption: "나무는 크다. 가지가 많다.",  // string (한국어, 마침표 구분)
  image_type: "나무"  // "집" | "나무" | "사람"
}

// Response (Backend)
{ 
  rewritten_queries: ["...", "..."],
  rag_docs: ["...", "...", "..."]  // array of strings
}
```

### ✅ API 3: `/interpret_single`
```javascript
// Request (Frontend)
{ 
  caption: "The tree is large. Many branches.",  // string (영어, 마침표 구분)
  rag_docs: ["...", "...", "..."],  // array
  image_type: "나무"  // 한국어
}

// Response (Backend)
{ interpretation: "Feature 1 - Large tree: suggests..." }  // English
```

### ✅ API 4: `/translate`
```javascript
// Request (Frontend)
{ text: "Feature 1 - Large tree: suggests..." }  // English

// Response (Backend)
{ translated: "특징 1 - 큰 나무: ...를 시사합니다" }  // Korean
```

### ✅ API 5: `/questions`
```javascript
// Request (Frontend)
{ 
  conversation: [
    { role: "assistant", content: "..." },
    { role: "user", content: "..." }
  ],
  interpretations: {  // ✅ interpretationsEN (영어)
    house: "The house is large...",
    tree: "The tree has...",
    person: "The person shows..."
  }
}

// Response (Backend)
{ question: "Why did you draw the tree without roots?" }  // English
```

### ✅ API 6: `/interpret_final`
```javascript
// Request (Frontend)
{ 
  single_results: {  // 한국어 번역본
    house: "집은 크고...",
    tree: "나무는...",
    person: "사람은..."
  },
  conversation: [...],
  user_info: { name: "홍길동", age: 25, gender: "male" }
}

// Response (Backend)
{ final: "검사자는 안정적인..." }  // Korean (5 paragraphs)
```

---

## 🎯 변수명 및 타입 일관성

### ✅ 캡션 관련
| 위치 | 변수명 | 타입 | 언어 | 용도 |
|------|--------|------|------|------|
| Backend | caption (return) | `string` (JSON) | - | API 응답 |
| Frontend | capJson.caption | `string` (JSON) | - | 파싱 전 |
| Frontend | captionObj | `object` | - | 파싱 후 |
| Frontend | captionObj.ko | `array` | 한국어 | 배열 |
| Frontend | captionObj.en | `array` | 영어 | 배열 |
| Frontend | koCaption | `string` | 한국어 | 화면 표시 (쉼표) |
| Frontend | enCaption | `string` | 영어 | 해석 입력 (마침표) |
| State | captions[type] | `string` | 한국어 | 최종 저장 |

### ✅ 해석 관련
| 위치 | 변수명 | 타입 | 언어 | 용도 |
|------|--------|------|------|------|
| Backend | interpretation (return) | `string` | 영어 | Qwen 출력 |
| Frontend | intJson.interpretation | `string` | 영어 | 원본 |
| Frontend | window.__interpretationsEN | `object` | 영어 | 임시 저장 |
| State | interpretationsEN[type] | `string` | 영어 | 질문 생성용 |
| Frontend | translateJson.translated | `string` | 한국어 | 번역본 |
| State | interpretations[type] | `string` | 한국어 | 화면 표시 |

### ✅ 질문 관련
| 위치 | 변수명 | 타입 | 언어 | 용도 |
|------|--------|------|------|------|
| Backend | question (return) | `string` | 영어 | Qwen 출력 |
| Frontend | json.question | `string` | 영어 | 원본 |
| Frontend | translateJson.translated | `string` | 한국어 | 번역본 |
| Frontend | questionText | `string` | 한국어 | 화면 표시 |

---

## 📝 프롬프트 품질 분석

### ✅ 1. 개별 해석 프롬프트 (`/interpret_single`)

**강점**:
- ✅ Fine-tuning 형식과 일치: "Please provide a psychological interpretation"
- ✅ 명확한 입력 구분: "Drawing Observations:"
- ✅ 구조화된 요구사항 (1, 2, 3)
- ✅ Reference Literature 적절히 포함

**개선 가능**:
- 캡션이 마침표로 구분된 여러 문장일 때 더 명확한 지시
- 예: "Each sentence represents a separate observation"

**평가**: ⭐⭐⭐⭐⭐ (5/5)

---

### ✅ 2. 질문 생성 프롬프트 (`/questions`)

**강점**:
- ✅ 간결한 task 설명
- ✅ 대화 유무에 따른 컨텍스트 조정
- ✅ "Output only the question:" - 명확한 출력 형식
- ✅ 해석 요약 (200자) - 컨텍스트 길이 최적화

**개선 가능**:
- 대화가 길어질수록 이전 질문과 중복 가능
- 질문 다양성을 위한 힌트 추가 고려

**평가**: ⭐⭐⭐⭐ (4/5)

---

### ✅ 3. 최종 해석 프롬프트 (`/interpret_final`)

**강점**:
- ✅ 명확한 입력 구조 (집, 나무, 사람 분리)
- ✅ 대화 내용 포함
- ✅ 사용자 정보 (나이, 성별) 반영
- ✅ 구체적인 출력 요구 (5개 문단, 한국어, 따뜻한 어조)

**개선 가능**:
- 한국어 해석 그대로 사용 → 영어 원본 참조 고려 가능
- 하지만 GPT-4o는 다국어 능력이 우수하므로 현재 구조도 적절

**평가**: ⭐⭐⭐⭐⭐ (5/5)

---

## ⚠️ 남은 잠재적 이슈

### 1. **window.__interpretationsEN 사용**
- 전역 변수 사용은 React 패턴에 맞지 않음
- ✅ 이미 state로 변경됨 (setInterpretationsEN)

### 2. **window.__htpFirstQuestionStarted 사용**
- StrictMode 이중 호출 방지용
- 더 나은 방법: useRef 사용

**개선안**:
```javascript
const firstQuestionStartedRef = useRef(false);

if (currentPage === 2 && messages.length === 0 && !isComplete) {
  const hasInterpretation = Object.values(interpretationsEN).some(v => v);
  if (hasInterpretation && !firstQuestionStartedRef.current) {
    firstQuestionStartedRef.current = true;
    startFirstQuestion();
  }
}
```

### 3. **에러 처리 부족**
- API 호출 실패 시 사용자에게 더 명확한 피드백 필요
- 로그만으로는 부족

**개선안**:
```javascript
catch (error) {
  console.error(`Interpretation failed for ${t}:`, error);
  newCaptions[t] = `캡션 생성 실패: ${error.message}`;
  newInterps[t] = `해석 생성 중 오류 발생: ${error.message}`;
  alert(`${tabNames[t].ko} 해석 중 오류가 발생했습니다. 다시 시도해주세요.`);
}
```

---

## 🎯 최종 평가

### 전반적 구조: ⭐⭐⭐⭐ (4.5/5)

**강점**:
- ✅ 명확한 데이터 플로우
- ✅ 모델별 역할 분담 (캡션: GPT Vision, 해석: Qwen, 최종: GPT-4o)
- ✅ 언어 처리 (영어 해석 → 한국어 번역)
- ✅ RAG 통합

**개선된 부분**:
- ✅ 캡션 형식 일관성
- ✅ 영어 해석 전달
- ✅ 타입 검증
- ✅ 프롬프트 컨텍스트

**향후 개선 필요**:
- useRef로 전역 변수 제거
- 더 나은 에러 UX
- 로딩 상태 세분화
- 테스트 코드 추가

---

## 📋 테스트 체크리스트

### Phase 1: 캡션 생성
- [ ] 그림 그리기 → 캡션 배열 형식 확인
- [ ] 콘솔에서 `captionObj` 확인: `{ko: [...], en: [...]}`
- [ ] 3-6개 항목 생성 확인

### Phase 2: 개별 해석
- [ ] 영어 캡션 (마침표 구분) 전달 확인
- [ ] RAG 문서 개수 로그 확인
- [ ] 영어 해석 생성 확인
- [ ] 한국어 번역 확인

### Phase 3: 질문 생성
- [ ] interpretationsEN 전달 확인 (영어)
- [ ] 첫 질문 생성 확인
- [ ] 후속 질문 5회 반복 확인
- [ ] 질문이 그림 요소 언급하는지 확인

### Phase 4: 최종 해석
- [ ] 5개 문단 생성 확인
- [ ] 대화 내용 반영 확인
- [ ] 사용자 정보 반영 확인

---

## 🚀 배포 전 체크리스트

- [x] 캡션 형식 통일
- [x] 영어 해석 전달 경로 확립
- [x] RAG 타입 검증
- [x] 프롬프트 최적화
- [ ] useRef 리팩토링 (선택)
- [ ] 에러 UX 개선 (선택)
- [ ] 통합 테스트
- [ ] 로그 모니터링
