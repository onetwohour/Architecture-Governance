# Completion Gates

구현이 돌아간다는 사실과 아키텍처적으로 완료되었다는 사실을 구분하는 최종 gate다.

> 이 문서는 읽기 쉬운 projection입니다. 규칙의 정본은 `rule-registry.json`입니다.

## Completion

### R-COMP-001 — “It works” is not a complete definition of done
- **Portability:** CORE
- **Strength:** SHOULD
- **Rule:** 기능 완료는 단일 happy-path 동작이 아니라 프로젝트가 선언한 적용 가능한 correctness, determinism, security, durability, accessibility, performance, extensibility 등의 품질 조건을 누적으로 만족했는지로 판정한다.
- **Why:** 기능 존재와 제품/시스템 완성도를 구분한다.
- **Applies when:** all non-trivial software projects
- **Does not apply when:** —
- **Enforcement:** completion-checklist

### R-COMP-002 — Known architecture violations cannot be closed as temporary debt
- **Portability:** CORE
- **Strength:** MUST
- **Rule:** 완료 범위 안의 알려진 architecture/spec violation을 “임시”, “나중에 정리”라는 이유로 완료 처리하지 않는다. scope에서 제외한다면 owner/status에 명시적으로 남긴다.
- **Why:** 숨은 debt를 완료 상태로 포장하지 않는다.
- **Applies when:** all non-trivial software projects
- **Does not apply when:** —
- **Enforcement:** completion-review

