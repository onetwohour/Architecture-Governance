# 규칙 모델

`rule-registry.json`이 이 스킬의 유일한 canonical policy registry입니다. 읽기용 문서는 이 레지스트리를 설명하거나 묶어 보여 주는 projection일 뿐, 서로 다른 규칙을 새로 만들지 않습니다.

각 규칙은 다음 정보를 가집니다.

- `id`: 위치가 바뀌어도 유지되는 규칙 ID
- `title`: 사람이 빠르게 찾기 위한 제목
- `statement`: 실제 규칙
- `rationale`: 규칙이 필요한 이유
- `portability`: `CORE`, `CONDITIONAL`, `PROFILE`
- `strength`: `MUST`, `SHOULD`, `DEFAULT`
- `applies_when`: 조건부 규칙이 적용되는 조건
- `does_not_apply_when`: 알려진 예외나 비적용 조건
- `enforcement`: review, lint, probe, compile, runtime 등 권장 검증 수단
- `parameters`: 프로젝트가 정할 수 있는 세부값

## 범용성

- **CORE**: 특별한 반례가 없다면 기본적으로 적용하는 engineering rule
- **CONDITIONAL**: 명시된 조건이 실제 프로젝트에 해당할 때만 적용
- **PROFILE**: 팀이나 저장소가 선택하는 편집·도구 관례. CORE 의미를 약화할 수는 없음

## 강도

- **MUST**: 적용되는 상황에서는 지켜야 함
- **SHOULD**: 구체적인 반례가 없다면 따름
- **DEFAULT**: profile의 기본값이며 조정 가능

문서에서 규칙을 참조할 때는 절 번호가 아니라 파일 경로와 규칙 ID를 사용합니다.
