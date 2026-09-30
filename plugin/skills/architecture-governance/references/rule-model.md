# Rule Model

`rule-registry.json`이 이 스킬의 유일한 canonical policy registry다. 각 rule은 다음 의미를 가진다.

- `id`: 안정적인 semantic rule ID. 문서 위치 번호 대신 이 ID를 참조한다.
- `statement`: 규칙 자체.
- `rationale`: 왜 필요한지.
- `portability`: `CORE`, `CONDITIONAL`, `PROFILE`.
- `strength`: `MUST`, `SHOULD`, `DEFAULT`.
- `applies_when`: CONDITIONAL rule을 활성화할 근거.
- `does_not_apply_when`: 예외 조건.
- `enforcement`: review/lint/probe/compile/runtime 등 권장 검증 수단.
- `parameters`: profile이나 프로젝트가 선택할 수 있는 세부 값.

## Portability

- **CORE**: 비사소한 소프트웨어 프로젝트에 기본 적용하는 engineering invariant.
- **CONDITIONAL**: 해당 구조나 runtime 조건이 실제로 존재할 때만 적용.
- **PROFILE**: 팀/저장소의 편집·도구 convention. 설정 가능하며 CORE 의미를 약화시키지 못한다.

## Strength

- **MUST**: 위반하면 해당 규칙이 적용되는 범위에서 defect.
- **SHOULD**: 기본적으로 따라야 하지만 명시적 근거가 있는 예외 가능.
- **DEFAULT**: profile의 기본 선택. 다른 선택이 architecture defect라는 뜻은 아니다.
