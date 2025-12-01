# 📋 프롬프트 예시 및 기대 출력

## 개별 해석 프롬프트 예시

### 예시 1: 집 (House)

**입력 캡션**: 
```
The house is large with two windows and a door, centered on the page.
```

**생성되는 프롬프트**:
```
Please provide a psychological interpretation of the following HTP test image caption.

Input: The house is large with two windows and a door, centered on the page.

Reference Literature:
- 집이 크게 그려진 경우, 가정에 대한 강한 욕구나 자신의 공간에 대한 중요성을 나타낼 수 있습니다...
- 창문의 개수와 크기는 외부 세계와의 소통 정도를 반영합니다...
- 중앙 배치는 안정감과 균형감을 시사합니다...

Provide a detailed psychological interpretation that:
1. Identifies specific visual features (size, placement, details, omissions)
2. Explains the psychological significance of each feature
3. Synthesizes findings into a coherent psychological assessment

Focus on emotional state, personality traits, and coping mechanisms. Use professional terminology and maintain an analytical, empathetic tone.
```

**기대되는 출력**:
```
Feature Analysis:

The large house suggests a strong emphasis on home and family life, potentially indicating that the individual places significant value on domestic stability and security. This could reflect a person who views their home environment as a central aspect of their identity and well-being.

The presence of two windows indicates a moderate level of openness to external interaction. The individual appears willing to engage with others but maintains some selectivity in their social connections, suggesting a balanced approach to relationships.

The centered placement on the page demonstrates good spatial awareness and a sense of balance in how the person views their position in the world. This central positioning often correlates with feelings of security and self-confidence in one's home environment.

Psychological Synthesis:

Overall, this drawing suggests an individual who values stability, security, and structured domestic life. The combination of a large, centered house with moderate openness (via windows) indicates someone who seeks balance between personal privacy and social engagement. This person likely has a strong sense of self within their family context and approaches life with a relatively grounded and stable perspective.
```

---

### 예시 2: 나무 (Tree)

**입력 캡션**: 
```
The tree is tall and dominant, with a thick trunk but no visible roots, positioned on the left side.
```

**생성되는 프롬프트**:
```
Please provide a psychological interpretation of the following HTP test image caption.

Input: The tree is tall and dominant, with a thick trunk but no visible roots, positioned on the left side.

Reference Literature:
- 나무의 크기는 자아 강도와 생명력을 반영합니다...
- 뿌리의 부재는 안정감 결여나 과거와의 단절을 나타낼 수 있습니다...
- 왼쪽 배치는 과거 지향적 경향을 시사할 수 있습니다...

Provide a detailed psychological interpretation that:
1. Identifies specific visual features (size, placement, details, omissions)
2. Explains the psychological significance of each feature
3. Synthesizes findings into a coherent psychological assessment

Focus on emotional state, personality traits, and coping mechanisms. Use professional terminology and maintain an analytical, empathetic tone.
```

**기대되는 출력**:
```
Feature Analysis:

The tall and dominant tree indicates strong ego strength and a desire for achievement and recognition. This suggests an individual with assertive qualities and possibly high aspirations, someone who seeks to stand out or make a significant impact in their environment.

The thick trunk reinforces the impression of inner strength and resilience. This person likely possesses considerable emotional fortitude and the capacity to withstand challenges, demonstrating robust psychological defenses.

The absence of visible roots is particularly significant, potentially indicating feelings of being ungrounded or disconnected from one's origins or support systems. This may reflect difficulty in acknowledging foundational relationships or a sense of instability despite outward strength.

The left-side positioning suggests a tendency toward past-orientation or introspection. This placement may indicate someone who is influenced by past experiences or who spends considerable time reflecting on previous events.

Psychological Synthesis:

This drawing reveals a complex psychological profile: an individual who presents as strong and capable yet may struggle with feelings of rootlessness or lack of grounding. The combination of dominance without visible foundational support suggests potential vulnerability beneath a strong exterior. This person may benefit from exploring connections to their origins and developing more secure attachment to supportive relationships.
```

---

### 예시 3: 사람 (Person)

**입력 캡션**: 
```
A single person facing forward, with detailed facial features but stick-figure body, no hands visible.
```

**생성되는 프롬프트**:
```
Please provide a psychological interpretation of the following HTP test image caption.

Input: A single person facing forward, with detailed facial features but stick-figure body, no hands visible.

Reference Literature:
- 정면을 향한 인물은 직접적이고 개방적인 태도를 나타냅니다...
- 얼굴의 세부 묘사는 자기 이미지에 대한 관심을 반영합니다...
- 손의 부재는 환경과의 상호작용 어려움을 시사할 수 있습니다...

Provide a detailed psychological interpretation that:
1. Identifies specific visual features (size, placement, details, omissions)
2. Explains the psychological significance of each feature
3. Synthesizes findings into a coherent psychological assessment

Focus on emotional state, personality traits, and coping mechanisms. Use professional terminology and maintain an analytical, empathetic tone.
```

**기대되는 출력**:
```
Feature Analysis:

The forward-facing orientation suggests directness and openness in social presentation. This individual likely approaches interactions with others in a straightforward manner and may value honest, direct communication.

The detailed facial features indicate significant investment in self-image and how one is perceived by others. This attention to facial detail suggests someone who is concerned with social impression and possibly places considerable importance on facial expression and communication.

The stick-figure body presents a notable contrast to the detailed face, suggesting possible discomfort with or disconnection from one's physical self. This disparity may indicate that the individual identifies more strongly with intellectual or emotional aspects of self rather than physical embodiment.

The absence of hands is particularly meaningful, as hands represent our capacity to interact with and manipulate our environment. This omission may indicate feelings of ineffectiveness, difficulty in taking action, or hesitation about one's ability to impact their surroundings.

Psychological Synthesis:

This drawing suggests an individual who presents a direct, open social facade while potentially experiencing internal conflicts about agency and physical embodiment. The person appears invested in how they are perceived socially (detailed face) but may struggle with feelings of effectiveness or control (absent hands, simplified body). This profile indicates someone who might benefit from developing greater integration between their self-concept and sense of personal agency.
```

---

## 질문 생성 프롬프트 예시

### 예시 1: 첫 번째 질문 (해석 기반)

**입력 컨텍스트**:
```
Conversation History:
(empty)

Drawing Interpretations:
- House: The large house suggests strong emphasis on home...
- Tree: The tall tree indicates strong ego strength but absence of roots...
- Person: Forward-facing with detailed face but no hands...
```

**생성되는 프롬프트**:
```
Generate one follow-up question for an HTP psychological assessment.

Context:

Drawing Interpretations:
- House: The large house suggests strong emphasis on home...
- Tree: The tall tree indicates strong ego strength but absence of roots...
- Person: Forward-facing with detailed face but no hands...

Task: Create ONE specific question in English about the drawing choices, focusing on observable features (size, placement, details, omissions, line quality, or drawing sequence). Ask about reasoning or feelings during drawing.

Output only the question:
```

**기대되는 출력**:
```
Why did you choose not to include roots on your tree drawing?
```

---

### 예시 2: 후속 질문 (대화 진행 중)

**입력 컨텍스트**:
```
Conversation History:
ASSISTANT: Why did you choose not to include roots on your tree drawing?
USER: I didn't think about it, I just drew what came naturally.
ASSISTANT: What made you decide to draw the house so large compared to the other elements?
USER: I wanted to show that home is important to me.

Drawing Interpretations:
- House: The large house suggests strong emphasis on home...
- Tree: The tall tree indicates strong ego strength...
- Person: Forward-facing with detailed face but no hands...
```

**생성되는 프롬프트**:
```
Generate one follow-up question for an HTP psychological assessment.

Context:
ASSISTANT: Why did you choose not to include roots on your tree drawing?
USER: I didn't think about it, I just drew what naturally.
ASSISTANT: What made you decide to draw the house so large compared to the other elements?
USER: I wanted to show that home is important to me.

Drawing Interpretations:
- House: The large house suggests strong emphasis on home...
- Tree: The tall tree indicates strong ego strength...
- Person: Forward-facing with detailed face but no hands...

Task: Create ONE specific question in English about the drawing choices, focusing on observable features (size, placement, details, omissions, line quality, or drawing sequence). Ask about reasoning or feelings during drawing.

Output only the question:
```

**기대되는 출력**:
```
Can you tell me about your decision to omit hands from the person drawing?
```

---

## 출력 품질 기준

### ✅ 좋은 출력 특징

1. **구체적**: 캡션의 실제 요소 언급
2. **분석적**: 각 요소의 의미 설명
3. **통합적**: 전체적 심리 상태 종합
4. **전문적**: 심리학 용어 사용
5. **완전한**: 끝까지 완성된 문장

### ❌ 나쁜 출력 특징

1. **모호한**: "그림이 흥미롭습니다" (구체성 없음)
2. **일반적**: "이 사람은 행복해 보입니다" (분석 없음)
3. **단편적**: 한두 문장으로 끝남
4. **반복적**: 같은 내용 반복
5. **불완전**: 중간에 끊김

---

## 모델 출력 검증 체크리스트

### 개별 해석
- [ ] 캡션에서 3개 이상의 구체적 요소 언급
- [ ] 각 요소마다 심리적 의미 설명
- [ ] "Feature Analysis" 섹션 존재
- [ ] "Psychological Synthesis" 섹션 존재
- [ ] 200자 이상의 의미 있는 내용
- [ ] 전문 용어 적절히 사용 (ego strength, coping mechanisms 등)

### 질문
- [ ] 한 문장으로 구성
- [ ] 물음표로 끝남
- [ ] 그림의 구체적 요소 언급 (roots, windows, hands 등)
- [ ] "Why", "Can you tell me", "What made you" 등의 개방형 질문
- [ ] 50-150자 범위
- [ ] 메타 질문 없음

---

## 프롬프트 튜닝 가이드

### temperature 조정 효과

| 값 | 효과 | 추천 상황 |
|----|------|----------|
| 0.5 | 매우 일관적, 보수적 | 반복 문제가 심할 때 |
| 0.65 | 균형잡힌 (현재 설정) | 대부분의 경우 |
| 0.7 | 약간 창의적 | 더 다양한 표현 원할 때 |
| 0.8 | 매우 창의적 | 비권장 (일관성 떨어짐) |

### max_new_tokens 조정 효과

| 값 | 효과 | 추천 상황 |
|----|------|----------|
| 400 | 짧은 출력 | 간결한 해석 원할 때 |
| 600 | 적절한 길이 (현재 설정) | 대부분의 경우 |
| 800 | 긴 출력 | 매우 상세한 해석 원할 때 |
| 1000+ | 너무 김 | 비권장 |

### repetition_penalty 조정 효과

| 값 | 효과 | 추천 상황 |
|----|------|----------|
| 1.0 | 제한 없음 | 비권장 |
| 1.1 | 약간 제한 (현재 설정) | 대부분의 경우 |
| 1.2 | 강한 제한 | 반복이 심할 때 |
| 1.3+ | 매우 강한 제한 | 비권장 (어색한 표현) |
