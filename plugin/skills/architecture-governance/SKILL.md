---
name: architecture-governance
description: Design, review, refactor, or normalize non-trivial software architecture and specifications using semantic ownership, explicit contracts, stable documentation, evidence-backed probes, and completion gates. Use for architecture design/review, specification cleanup, large refactors, implementation-vs-design audits, structural defect analysis, ADR/contract normalization, reusable engineering rules, or changes that risk parallel managers/stores/dispatchers/bridges or hidden semantic ordering. Do not use for trivial isolated edits with no architectural or contract impact.
---

# Architecture Governance

이 스킬은 대상 프로젝트의 도메인을 바꾸는 설계 템플릿이 아닙니다. 프로젝트에 이미 있는 의미와 제약을 조사한 뒤, 책임 경계와 계약을 더 분명하게 만들기 위한 작업 규칙입니다.

## 정책의 정본

- `references/rule-registry.json`이 규칙의 유일한 정본입니다.
- `references/engineering-constitution.md`은 정본 규칙을 사람이 읽기 쉽게 펼친 문서입니다.
- 나머지 `references/*.md`는 특정 관점만 모아 보여 주는 보조 문서입니다. 정본과 다른 규칙을 새로 만들면 안 됩니다.
- `templates/*`는 산출물의 틀일 뿐 정책을 정의하지 않습니다.
- `CORE`는 기본적으로 적용하는 규칙, `CONDITIONAL`은 조건이 맞을 때만 적용하는 규칙, `PROFILE`은 프로젝트가 정할 수 있는 관례입니다.

## 작업 순서

1. **자료의 역할부터 나눕니다.** 규범 문서, 구현 현황, 계획, 조사 기록, 예시, 생성 인덱스, 테스트, 코드를 구분합니다. 현재 코드가 존재한다는 사실만으로 그 코드가 아키텍처의 정본이 되지는 않습니다.
2. **책임 경계를 찾습니다.** 이 의미를 누가 정의하는지, 실제 상태를 누가 바꿀 수 있는지, 어떤 의존성과 생산자·소비자가 있는지 확인합니다. 수명주기, 실패·취소·재시도, 영속성·복구, 동시성, 확장 지점도 필요한 범위에서 조사합니다.
3. **질문하기 전에 애매함의 종류를 판정합니다.** `references/decision-policy.md`를 읽고 이미 정해진 설계인지, 구현 자유인지, 지역 설계/명세 결함인지, 실제 제품 정책이 비어 있는지 구분합니다. 리팩터링 규모나 구현 난이도만으로 제품 결정을 요구하지 않습니다.
4. **새로 만들기 전에 기존 책임자를 찾습니다.** 기능 전용 Manager·Coordinator·Registry·Dispatcher·Store·Bridge·Adapter를 추가하기보다 기존 정본 책임자를 확장하거나 재설계할 수 있는지 먼저 확인합니다.
5. **중요 계약의 빈칸을 닫습니다.** 해당되는 범위에서 식별자, 소유권, 상태와 전이, 권한, 순서, 가시성·원자성, 실패, 취소, 재시도·멱등성, 재생, 영속성, 재구성, 동시성, 알 수 없는 상태의 처리, 관측 가능성을 정합니다. 정말 해당하지 않는 항목만 `N/A`로 표시합니다.
6. **의존성과 순서를 숨기지 않습니다.** 등록 순서, 소스 순서, 컨테이너 순회, callback 시점, thread scheduling, 이름 조회, 임의의 가변 연결이 정확성을 결정하게 두지 않습니다.
7. **문서 참조를 안정적으로 유지합니다.** 다른 문서를 가리킬 때는 경로와 안정적인 개념명 또는 규칙 ID를 사용합니다. `§12`, `3장 2절`처럼 위치가 바뀌면 깨지는 참조를 의미 식별자로 쓰지 않습니다.
8. **서로 다른 종류의 사실을 섞지 않습니다.** 규범, 구현 현황, 계획, 조사 기록, 작업 절차는 역할이 다릅니다. 한 문서의 사실을 다른 역할의 문서로 옮기면서 의미를 바꾸지 않습니다.
9. **중요한 불변 규칙을 증거로 연결합니다.** 중요한 Probe에는 정상 경로뿐 아니라 반례와 절대로 나타나면 안 되는 상태를 둡니다. module, type, document가 존재한다는 사실만으로 readiness를 올리지 않습니다.
10. **완료를 다시 감사합니다.** `references/completion-gates.md`와 `references/anti-patterns.md`를 확인합니다. 알고 있는 구조 위반을 `임시`라는 말로 완료 처리하지 않습니다.

## 문서와 주석의 어투

`references/editorial-policy.md`를 따릅니다.

- 한국어 문서는 한국어 문장 구조로 씁니다. 표준 기술 용어와 코드 식별자만 필요할 때 원문을 유지합니다.
- 영어 명사를 조사와 함께 길게 나열하거나 영어 관용구를 직역한 표현을 습관적으로 쓰지 않습니다.
- 명사 나열보다 누가 무엇을 어떤 조건에서 하는지가 드러나는 문장을 우선합니다.
- 시스템·코드·문서·캐시 등에 모델로 정의되지 않은 의도, 욕구, 지식, 기억, 판단을 부여하지 않습니다.
- 다만 `parser가 잘못된 입력을 거부한다`처럼 실제 계약에 정의된 동작을 능동형으로 쓰는 것은 허용합니다.

## 기본 판단

- 하나의 의미에는 하나의 규범적 정본 책임자가 있습니다.
- Reuse Before Create를 기본으로 삼고 병렬 권위를 만들지 않습니다.
- 표준 확장 지점이 부족하면 우회하기 전에 그 확장 지점을 넓힐 수 있는지 봅니다.
- 공통 추상화에는 독립된 두 번째 사례 또는 명확한 폐쇄형 도메인 법칙이 필요합니다.
- 하나의 의미 변경이 관계없는 계층까지 퍼진다면 책임 경계를 다시 점검합니다.
- 성능을 이유로 소유권·권한·커밋·검증 경계를 우회하지 않습니다.
- 모르는 상태를 임의의 기본값으로 추측하지 않습니다.
- 현재 구현 관행은 구현 상태에 대한 증거이지, 의도한 아키텍처의 증명은 아닙니다.

## 조건부 규칙

`CONDITIONAL` 규칙은 `applies_when` 조건이 프로젝트의 실제 자료로 확인될 때만 적용합니다. 설계에 큰 영향을 주는 조건부 규칙을 적용했다면 왜 해당하는지 적습니다. 중요한 예외가 있다면 그 이유도 함께 적습니다.

## 결과에 남겨야 할 것

아키텍처 의미가 바뀌는 작업이라면 최소한 다음 질문에 답할 수 있어야 합니다.

- 이 의미의 정본 책임자는 누구인가?
- 기존 추상화를 재사용했는가, 재설계했는가?
- 새로 생기거나 바뀐 계약은 무엇인가?
- 의존성과 실행 순서는 어디에 명시되어 있는가?
- 영속 상태, 작업 중 상태, 파생 상태는 어떻게 달라지는가?
- commit, 부수 효과, 외부 입력의 경계는 어디인가?
- 실패·취소·재시도는 어떻게 동작하는가?
- replay와 비결정성에 어떤 영향이 있는가?
- 동시 실행과 stale/late result는 어떻게 처리하는가?
- 변경 전후 readiness와 그 근거는 무엇인가?
- 어떤 Probe·테스트·gate가 추가되거나 바뀌었는가?
- 공통 추상화라면 두 번째 사례의 근거가 있는가?
- 범위 안에 남은 명세 결함은 무엇인가?

필요하면 `templates/architecture-review.md`, `templates/contract.md`, `templates/decision-record.md`, `templates/probe.md`를 사용합니다. 짧은 답이 더 유용한 상황에서 형식을 억지로 채우지는 않습니다.

## 읽기 순서

- 전체 정책과 이유 → `references/engineering-constitution.md`
- 규칙의 정확한 강도·적용 조건·검증 수단 → `references/rule-registry.json`
- 문서·주석·어투 → `references/editorial-policy.md`
- 판단이 필요한 애매한 상황 → `references/decision-policy.md`
- 완료 전 감사 → `references/completion-gates.md`, `references/anti-patterns.md`
- 레지스트리 구조 → `references/rule-model.md`

이 스킬 자체를 수정했다면 스킬 디렉터리에서 `python scripts/validate.py`를 실행합니다.
