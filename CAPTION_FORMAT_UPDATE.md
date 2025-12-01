# 🔄 캡션 형식 업데이트 (리스트 구조)

## 변경 사항

캡션 형식을 **단일 문자열**에서 **구조화된 리스트**로 변경했습니다.

---

## 1. 변경 이유

### 기존 문제점
```json
{
  "ko": "나무는 크고 가지가 많으며 뿌리가 깊게 그려졌다",
  "en": "The tree is large with many branches and deeply drawn roots"
}
```
- 여러 관찰 내용이 하나의 긴 문장으로 결합됨
- Qwen 모델이 개별 특징을 구분하기 어려움
- 모델의 fine-tuning 데이터와 형식 불일치

### 개선된 형식
```json
{
  "ko": [
    "나무는 크고 중앙에 위치해 있다",
    "가지가 많고 위쪽으로 뻗어있다",
    "뿌리가 깊게 그려져 있다",
    "나뭇잎이 풍성하게 그려져 있다"
  ],
  "en": [
    "The tree is large and centered",
    "Many branches extending upward",
    "Deeply drawn roots",
    "Abundant foliage"
  ]
}
```
- 각 관찰 내용이 명확히 구분됨
- 모델이 개별 특징을 분석하기 용이
- 더 구조화된 입력으로 일관성 향상

---

## 2. 수정된 파일

### ✅ `caption.py`
1. **프롬프트 예시 변경**: 리스트 형식으로 수정
2. **파싱 검증 추가**: 리스트가 아닌 경우 자동 변환
3. **에러 처리 개선**: 빈 리스트 반환

```python
# 리스트 형식 검증
if not isinstance(obj.get("ko"), list):
    obj["ko"] = [obj.get("ko", "")]
if not isinstance(obj.get("en"), list):
    obj["en"] = [obj.get("en", "")]
```

### ✅ `HTPChatbot.jsx` (프론트엔드)
1. **리스트 처리**: 배열을 문자열로 조합
2. **화면 표시**: 쉼표로 연결
3. **RAG/해석**: 마침표로 연결

```javascript
// 화면 표시용: "특징1, 특징2, 특징3"
const koCaption = Array.isArray(captionObj.ko) 
  ? captionObj.ko.join(', ') 
  : captionObj.ko;

// RAG/해석용: "특징1. 특징2. 특징3"
const enCaption = Array.isArray(captionObj.en)
  ? captionObj.en.join('. ')
  : captionObj.en;
```

### ✅ `multi_main.py` (백엔드)
1. **프롬프트 개선**: "Drawing Observations" 라벨 추가
2. **구조 단순화**: 리스트 형식에 맞춘 지시사항

```python
prompt = f"""Please provide a psychological interpretation of the following HTP test image caption.

Drawing Observations: {req.caption}

Provide a detailed psychological interpretation that:
1. Analyzes each observed feature and its psychological meaning
2. Integrates these features into a comprehensive assessment
3. Discusses emotional state, personality traits, and coping mechanisms
```

---

## 3. 예상 효과

### ✅ 장점

1. **명확한 특징 분리**: 
   - Before: "나무는 크고 가지가 많으며..." (구분 어려움)
   - After: ["나무는 크다", "가지가 많다", ...] (명확)

2. **모델 성능 향상**:
   - 각 특징을 개별적으로 분석 가능
   - Fine-tuning 데이터 형식과 유사

3. **유연성 증가**:
   - 특징 개수에 제한 없음 (3-6개 권장)
   - 추가/삭제 용이

4. **일관성 향상**:
   - 구조화된 입력 → 구조화된 출력
   - 반복 가능한 처리 과정

### ⚠️ 고려사항

1. **GPT-4o-mini 캡션 생성**:
   - 리스트 형식으로 생성하도록 지시
   - 간혹 단일 문자열 반환 시 자동 변환

2. **하위 호환성**:
   - 단일 문자열도 자동으로 리스트로 변환
   - 기존 데이터와 호환 가능

---

## 4. 테스트 체크리스트

### ✅ 캡션 생성 테스트

1. **형식 확인**:
   ```javascript
   console.log('Caption:', captionObj);
   // 기대: { ko: [...], en: [...] }
   ```

2. **배열 길이**:
   - 3-6개의 항목이 생성되는지 확인
   - 너무 적거나 많지 않은지 확인

3. **내용 품질**:
   - 각 항목이 독립적인 관찰 내용인지
   - 중복되는 내용이 없는지

### ✅ 해석 생성 테스트

1. **입력 확인**:
   - 백엔드 로그에서 "Drawing Observations:" 확인
   - 마침표로 구분된 문장들 확인

2. **출력 확인**:
   - 각 관찰 내용을 언급하는지
   - 개별 특징별 심리적 의미 설명하는지

### ✅ 화면 표시 테스트

1. **캡션 섹션**:
   - 쉼표로 구분되어 표시되는지
   - 읽기 편한지

---

## 5. 예시 비교

### Before (단일 문자열)
```
입력: "The tree is large with many branches and deeply drawn roots"

해석: "The large tree suggests..." 
(하나의 덩어리로 처리)
```

### After (리스트 구조)
```
입력: "The tree is large and centered. Many branches extending upward. Deeply drawn roots. Abundant foliage"

해석:
"Feature 1 - Large and centered: suggests...
Feature 2 - Many upward branches: indicates...
Feature 3 - Deep roots: reflects...
Feature 4 - Abundant foliage: demonstrates..."
(각 특징을 개별 분석)
```

---

## 6. 문제 해결

### 🔴 캡션이 배열이 아닌 경우

**증상**: 프론트엔드 에러 발생
```
TypeError: captionObj.ko.join is not a function
```

**해결**: 자동 변환 로직이 작동하므로 정상
```javascript
// 이미 구현된 fallback
const koCaption = Array.isArray(captionObj.ko) 
  ? captionObj.ko.join(', ') 
  : captionObj.ko;  // ← 단일 문자열도 처리
```

### 🔴 캡션이 너무 많은 경우 (7개 이상)

**증상**: 프롬프트가 너무 길어짐

**해결**: `caption.py`에서 제한 추가 (선택사항)
```python
# 최대 6개까지만
obj["ko"] = obj.get("ko", [])[:6]
obj["en"] = obj.get("en", [])[:6]
```

### 🔴 빈 배열 반환

**증상**: `ko: []` 또는 `en: []`

**원인**: GPT 캡션 생성 실패

**해결**: 로그 확인 후 프롬프트 조정
```
⚠️ GPT JSON 파싱 실패, 원본: ...
```

---

## 7. 다음 단계

1. **서버 재시작** (양쪽 모두)
2. **테스트 시나리오 실행**
3. **로그 모니터링**
4. **필요시 캡션 개수 조정** (3-6개 권장)

---

## 📊 성능 비교 (예상)

| 측면 | Before | After |
|------|--------|-------|
| 특징 인식 | 모호함 | 명확함 ⭐⭐⭐⭐⭐ |
| 해석 정확도 | 보통 | 향상 ⭐⭐⭐⭐ |
| 일관성 | 보통 | 향상 ⭐⭐⭐⭐ |
| 구조화 | 낮음 | 높음 ⭐⭐⭐⭐⭐ |
