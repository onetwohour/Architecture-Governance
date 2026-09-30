# Decision Policy

무엇이 이미 정해진 설계인지, 구현 자유인지, 설계 결함인지, 실제 제품 정책 선택인지 판정할 때 사용한다.

> 이 문서는 읽기 쉬운 projection입니다. 규칙의 정본은 `rule-registry.json`입니다.

## Decision Policy

### R-DEC-001 — Classify ambiguity before asking for a decision
- **Portability:** CORE
- **Strength:** MUST
- **Rule:** 애매함은 먼저 Specified Architecture, Implementation Freedom, Spec/Local Design Defect, Unspecified Product Policy로 분류한다. 실제 제품 결정 후보는 마지막 경우뿐이다.
- **Why:** 기술적 책임을 제품 선택으로 외부화하지 않는다.
- **Applies when:** all non-trivial software projects
- **Does not apply when:** —
- **Enforcement:** review

### R-DEC-002 — Product-decision threshold is high
- **Portability:** CORE
- **Strength:** MUST
- **Rule:** 제품/사용자 결정을 요구하기 전에 owner와 dependency를 읽고 canonical extension point를 조사하며, 기존 invariant로 우열을 연역할 수 없고 모든 후보가 correctness/security/determinism/extensibility를 만족하며 실제 사용자 경험 차이가 남는지 확인한다.
- **Why:** 질문을 보수성의 대체물로 사용하지 않는다.
- **Applies when:** all non-trivial software projects
- **Does not apply when:** —
- **Enforcement:** decision-checklist

### R-DEC-003 — Implementation difficulty is not product policy
- **Portability:** CORE
- **Strength:** MUST
- **Rule:** 새 type/field가 필요하거나 refactor가 크고 파일이 많이 바뀌거나 기존 internal API를 폐기해야 한다는 이유만으로 제품 결정을 요구하지 않는다.
- **Why:** 구현 비용과 제품 의미는 다른 축이다.
- **Applies when:** all non-trivial software projects
- **Does not apply when:** —
- **Enforcement:** review

### R-DEC-004 — Architecture change means a semantic-law change
- **Portability:** CORE
- **Strength:** MUST
- **Rule:** 변경 규모가 아니라 system-wide closed law, dependency direction, durable truth owner, public contract의 기본 의미, identity/ordering/authority/failure law가 바뀌는지로 architecture change를 판정한다.
- **Why:** 큰 refactor를 architecture change로 과대분류하거나 실제 law 변화를 놓치는 것을 막는다.
- **Applies when:** all non-trivial software projects
- **Does not apply when:** —
- **Enforcement:** change-classification

### R-DEC-005 — Absence from the current document is not proof of an architecture change
- **Portability:** CORE
- **Strength:** MUST
- **Rule:** 요구가 문서에 없다는 사실만으로 architecture 변경을 선언하지 않는다. 기존 extension point나 contract extension으로 자연스럽게 표현 가능한지 먼저 검증한다.
- **Why:** 문서 공백과 구조적 표현 불가능성을 구분한다.
- **Applies when:** all non-trivial software projects
- **Does not apply when:** —
- **Enforcement:** review

### R-DEC-006 — Fix local design defects at their owner
- **Portability:** CORE
- **Strength:** MUST
- **Rule:** closed law를 바꿀 필요 없이 owner-local abstraction이 좁거나 잘못되었다면 하위 workaround를 추가하지 않고 해당 owner를 재설계한다.
- **Why:** 잘못된 local API의 호환성을 보존하기 위해 전역 architecture를 왜곡하지 않는다.
- **Applies when:** all non-trivial software projects
- **Does not apply when:** —
- **Enforcement:** review

### R-DEC-007 — Architecture-defect claims carry a proof burden
- **Portability:** CORE
- **Strength:** MUST
- **Rule:** architecture defect를 주장하려면 현재 owner, 시도한 extension point, 표현 불가능한 정확한 이유, 깨지는 invariant, implementation/contract extension으로 해결 불가능한 이유, 필요한 최소 law change와 최소 반례를 제시한다.
- **Why:** 익숙한 API가 없다는 사실과 구조적으로 표현 불가능한 사실을 분리한다.
- **Applies when:** all non-trivial software projects
- **Does not apply when:** —
- **Enforcement:** decision-record

### R-DEC-008 — Use a deterministic default reasoning order
- **Portability:** CORE
- **Strength:** MUST
- **Rule:** 명시적 제품 결정을 기다릴 필요가 없으면 invariant를 더 강하게 보존하고, canonical owner 재사용, 더 일반적·조합 가능한 abstraction, truth 추가보다 derived state, runtime fallback보다 사전 검증, 암묵 규칙보다 explicit identity/order/failure를 순서대로 선호한다.
- **Why:** 동등해 보이는 내부 선택을 일관된 engineering 기준으로 좁힌다.
- **Applies when:** all non-trivial software projects
- **Does not apply when:** —
- **Enforcement:** review

### R-DEC-009 — Settings are not correctness escape hatches
- **Portability:** CORE
- **Strength:** MUST
- **Rule:** correct/incorrect, safe/unsafe, deterministic/order-dependent, canonical path/bypass 같은 선택을 사용자가 떠안는 Setting으로 만들지 않는다. 제공하는 선택지는 모두 핵심 invariant를 만족해야 한다.
- **Why:** 구현 결함을 제품 옵션으로 숨기지 않는다.
- **Applies when:** all non-trivial software projects
- **Does not apply when:** —
- **Enforcement:** product-review

### R-DEC-010 — Current code practice is not architecture authority
- **Portability:** CORE
- **Strength:** MUST
- **Rule:** 현재 코드가 반복해서 사용하는 우회나 관행을 원래 설계 의도로 사후 합리화하지 않는다. owner docs와 다르면 implementation violation인지 owner defect인지 root-cause를 다시 판정한다.
- **Why:** 현상과 규범을 뒤집지 않는다.
- **Applies when:** all non-trivial software projects
- **Does not apply when:** —
- **Enforcement:** review

### R-DEC-011 — Spec defects are normal self-correction signals
- **Portability:** CORE
- **Strength:** MUST
- **Rule:** 구현 중 반례가 드러나면 잘못된 abstraction을 보존하지 않고 owner와 Probe를 수정한 뒤 계속한다. spec defect 발견 자체를 실패로 취급하지 않는다.
- **Why:** 설계를 지킨다는 것을 하위 구조를 영원히 보존하는 것으로 오해하지 않는다.
- **Applies when:** all non-trivial software projects
- **Does not apply when:** —
- **Enforcement:** review

