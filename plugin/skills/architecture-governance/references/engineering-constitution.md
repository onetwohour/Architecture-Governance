# Engineering Constitution v2.2

이 문서는 `registry/canonical-rules.json`의 사람이 읽는 projection이다. **규칙의 정본은 registry 하나뿐이며 이 문서는 새 규범을 만들지 않는다.**

Portability는 **CORE / CONDITIONAL / PROFILE**, 규범 강도는 **MUST / SHOULD / DEFAULT**로 서로 독립적으로 표현한다.

## Work Protocol

### R-WORK-001 — Owner-first reconnaissance
**Portability:** CORE  
**Strength:** MUST  
사소하지 않은 변경은 요구의 semantic owner와 dependency를 확인하고, 기존 canonical model·producer/consumer·lifecycle·failure path·extension point를 조사한 뒤 구현한다.

**Why:** 이름이 다르다는 이유로 같은 책임의 두 번째 구조를 만들거나 기존 계약을 우회하는 것을 막는다.
**Applies when:** all non-trivial software projects
**Enforcement:** review/checklist
**Sources:** `CLAUDE.md:58-77`; `CLAUDE.md:81-140`; `CLAUDE.md:813-827`; `CLAUDE.md:833-843`

### R-WORK-002 — Semantic changes update every affected representation
**Portability:** CORE  
**Strength:** MUST  
공개 semantic field나 contract를 바꾸면 owner 문서뿐 아니라 해당 의미를 직렬화·digest·compile·read·validate·test하는 representation과 evidence를 함께 확인한다. 정확한 영향 표면은 프로젝트가 소유한 dependency graph로 결정한다.

**Why:** 한 representation만 바뀌면 문서·wire·runtime·검증이 서로 다른 의미를 구현하게 된다.
**Applies when:** all non-trivial software projects
**Enforcement:** change-impact-checklist/dependency-graph
**Sources:** `docs/development/document-system.md:102-113`

## Ownership

### R-OWN-001 — Single semantic authority
**Portability:** CORE  
**Strength:** MUST  
같은 semantic responsibility의 규범적 의미는 한 authoritative owner가 소유한다. 다른 문서와 모듈은 그 의미를 참조하거나 projection으로 소비하며, 충돌 시 임의 precedence를 만들지 않고 ownership/spec defect로 처리한다.

**Why:** 중복 정본은 시간이 지나면 서로 다른 의미를 만들고 소비자가 다시 precedence를 결정하게 만든다.
**Applies when:** all non-trivial software projects
**Enforcement:** manifest-lint/review
**Sources:** `CLAUDE.md:737-766`; `CLAUDE.md:813-827`; `docs/ARCHITECTURE.md:137-137`; `docs/development/document-system.md:3-7`; `docs/development/document-system.md:74-84`; `docs/development/document-system.md:203-215`; `docs/principles/constitution.md:113-124`

### R-OWN-002 — Architecture as an owner graph
**Portability:** CONDITIONAL  
**Strength:** MUST  
아키텍처는 하나의 전역 override 문서가 아니라 semantic owner와 dependency의 graph로 구성한다. 최상위 문서는 입구와 지도를 제공하되 세부 owner를 덮어쓰지 않는다.

**Why:** 전역 문서에 세부 의미를 집중시키면 ownership과 변경 경계가 흐려진다.
**Applies when:** architecture/specification이 여러 semantic owner나 문서/subsystem으로 나뉘는 경우
**Enforcement:** manifest-lint/review
**Sources:** `docs/ARCHITECTURE.md:3-3`; `docs/ARCHITECTURE.md:41-41`; `docs/ARCHITECTURE.md:116-140`; `docs/development/document-system.md:3-20`

### R-OWN-003 — Reuse before create
**Portability:** CORE  
**Strength:** MUST  
새 Manager·Registry·Store·Dispatcher·Service·UI primitive·persistence representation을 만들기 전에 동일 semantic responsibility의 기존 owner를 찾는다. 기존 abstraction이 좁으면 병렬 계층 대신 canonical owner를 일반화하거나 재설계한다.

**Why:** feature마다 작은 local subsystem이 생기는 것을 막는다.
**Applies when:** all non-trivial software projects
**Enforcement:** review/repository-search
**Sources:** `CLAUDE.md:144-188`; `CLAUDE.md:737-766`; `docs/principles/constitution.md:202-223`

### R-OWN-004 — No parallel authority; patch budget defaults to zero
**Portability:** CORE  
**Strength:** MUST  
같은 의미의 두 번째 권위 경로를 만들지 않는다. 임시 Adapter/Bridge/Manager는 서로 본질적으로 다른 계약을 연결할 때만 정당하며, 기존 모델 결함을 숨기기 위한 patch budget의 기본값은 0이다.

**Why:** 두 권위의 reconciliation은 그 자체로 새 semantic 문제이며 임시 우회는 구조 결함을 고착시킨다.
**Applies when:** all non-trivial software projects
**Enforcement:** review/lint
**Parameters:** `{"patch_budget_default": 0}`
**Sources:** `CLAUDE.md:267-305`; `CLAUDE.md:655-681`; `CLAUDE.md:737-766`; `CLAUDE.md:948-961`; `docs/principles/change-and-self-correction.md:103-121`; `docs/principles/change-and-self-correction.md:123-149`; `docs/principles/change-and-self-correction.md:197-206`; `docs/principles/constitution.md:210-223`; `docs/quality/security-gates.md:256-268`

### R-OWN-005 — Change locality is a robustness signal
**Portability:** CORE  
**Strength:** SHOULD  
한 semantic 의미를 바꿀 때 그 의미를 소유한 경계에 변경이 국소화되는 구조를 선호한다. 관계없는 계층까지 연쇄 수정이 필요하면 구현량보다 boundary/ownership defect를 먼저 의심한다.

**Why:** 변경 locality는 책임 경계가 실제로 의미를 캡슐화하는지 보여 주는 강한 신호다.
**Applies when:** all non-trivial software projects
**Enforcement:** review
**Sources:** `CLAUDE.md:731-731`; `CLAUDE.md:948-961`; `docs/principles/constitution.md:196-200`

### R-OWN-006 — Contract-mediated coupling
**Portability:** CONDITIONAL  
**Strength:** MUST  
서로 독립적으로 확장되어야 하는 구성요소는 상대 구현을 직접 호출하거나 내부 상태에 의존하지 않고 canonical contract·service·action·resource 등 공개된 semantic edge를 통해 연결한다.

**Why:** 구현 직접 의존은 교체·제거·조합 가능성을 깨고 숨은 권위 경로를 만든다.
**Applies when:** plugin/module/component architecture 또는 독립 교체·제거를 목표로 할 때
**Enforcement:** dependency-lint/review
**Sources:** `docs/principles/constitution.md:74-111`; `docs/principles/constitution.md:174-178`

### R-OWN-007 — Minimal configuration must conform
**Portability:** CONDITIONAL  
**Strength:** MUST  
모듈식·선택적 구성을 주장하는 시스템은 optional feature를 모두 제거한 최소/빈 구성도 정상 lifecycle을 가져야 한다.

**Why:** 최소 구성이 깨지면 optional layer가 사실상 hidden mandatory dependency임을 뜻한다.
**Applies when:** optional modules/plugins/features를 지원한다고 주장할 때
**Enforcement:** conformance-test
**Sources:** `docs/principles/constitution.md:16-20`; `docs/principles/constitution.md:33-33`; `docs/quality/security-gates.md:375-404`

### R-OWN-008 — Open extensions, closed system laws
**Portability:** CONDITIONAL  
**Strength:** MUST  
확장 가능한 surface와 모든 확장이 따라야 하는 identity·ordering·authority·commit·failure 같은 system-wide law를 구분한다. 새 기능 때문에 closed law를 임의로 열지 않는다.

**Why:** 확장성과 전 시스템 의미 일관성을 동시에 유지한다.
**Applies when:** 확장/플러그인/다중 구현 생태계를 제공할 때
**Enforcement:** architecture-review
**Sources:** `docs/principles/constitution.md:37-70`

### R-OWN-009 — Extend before escape
**Portability:** CONDITIONAL  
**Strength:** MUST  
표준 extension surface가 요구를 표현하지 못하면 feature-local bypass나 foreign path로 탈출하기 전에 canonical surface를 보강할 수 있는지 먼저 검토한다.

**Why:** escape hatch가 일반 기능의 기본 경로가 되면 표준 owner가 무력화되고 기능별 parallel system이 생긴다.
**Applies when:** 표준 framework/extension surface와 escape hatch가 함께 존재할 때
**Enforcement:** review
**Sources:** `CLAUDE.md:521-531`; `CLAUDE.md:737-766`; `docs/principles/constitution.md:423-432`; `docs/principles/product-and-decision-policy.md:161-161`; `docs/quality/security-gates.md:206-208`; `docs/quality/security-gates.md:435-450`; `docs/ui/ui-framework.md:860-879`; `docs/ui/ui-framework.md:957-959`

### R-OWN-010 — Extensibility means add, remove, replace, and compose
**Portability:** CONDITIONAL  
**Strength:** MUST  
확장성을 주장하려면 기능 추가뿐 아니라 제거, 동등 계약 구현으로의 교체, 서로를 모르는 구성요소의 조합이 모두 가능한지 검증한다.

**Why:** 추가만 가능한 구조는 실제로는 결합도가 높은 기능 누적일 수 있다.
**Applies when:** extensible/modular architecture를 주장할 때
**Enforcement:** conformance-test/review
**Sources:** `docs/principles/constitution.md:72-86`

### R-OWN-011 — Prefer composable primitives over feature silos
**Portability:** CORE  
**Strength:** SHOULD  
서로 다른 기능군을 독립 global subsystem의 단순 합으로 늘리기보다 공통 semantic primitive와 composition으로 표현할 수 있는지 먼저 검토한다. 새 기능이 기존 primitive로 표현되지 않으면 곧바로 새 subsystem을 만들지 말고 canonical owner 모델의 부족을 먼저 점검한다.

**Why:** 기능별 silo가 늘어날수록 identity, state, action, search, persistence 같은 공통 의미가 중복되고 상호운용 비용이 커진다.
**Applies when:** 여러 기능이 공통 domain/runtime 개념을 공유하는 제품이나 플랫폼
**Does not apply when:** 기능들이 실제로 독립된 배포·보안·수명·데이터 경계를 가져 분리된 subsystem이 정당한 경우
**Enforcement:** architecture-review
**Sources:** `docs/principles/constitution.md:293-309`

### R-OWN-012 — Package boundaries require real independence
**Portability:** CORE  
**Strength:** SHOULD  
crate/package/service 같은 물리 코드 경계는 개념 수가 많다는 이유가 아니라 독립 consumer, public API, 보안/unsafe 경계, 무거운 dependency 격리, process/deploy 경계처럼 실제 독립성이 있을 때 둔다. 책임이 없는 common/shared/utils/misc 저장소를 기본 해법으로 삼지 않는다.

**Why:** 물리 경계를 과도하게 만들면 ownership이 선명해지는 대신 책임 없는 공유 계층과 dependency churn이 생길 수 있다.
**Applies when:** repository/module/package 경계를 설계하거나 재구성할 때
**Enforcement:** architecture-review
**Sources:** `docs/ARCHITECTURE.md:150-163`

## Abstraction

### R-ABS-001 — Abstraction requires independent evidence
**Portability:** CORE  
**Strength:** MUST  
공통 abstraction은 서로 다른 두 consumer/상황이 동일 semantic contract로 우회 없이 사용할 수 있거나, 하나의 consumer라도 명확한 closed domain law를 구현할 때만 승격한다. 첫 feature의 private shape에 generic 이름을 붙인 것만으로 일반화하지 않는다.

**Why:** 두 번째 사례는 feature-shaped abstraction과 실제 공통 law를 구분한다.
**Applies when:** all non-trivial software projects
**Enforcement:** second-case-review/conformance-test
**Sources:** `CLAUDE.md:60-74`; `CLAUDE.md:685-697`; `docs/principles/change-and-self-correction.md:169-182`; `docs/principles/change-and-self-correction.md:208-212`; `docs/quality/architecture-probes.md:1410-1442`

## Runtime Semantics

### R-SEM-001 — Semantic dependencies and ordering are explicit
**Portability:** CORE  
**Strength:** MUST  
실행·resolution·ownership·observation 결과에 영향을 주는 dependency와 order를 registration order, source order, container iteration, thread completion, hidden mutable wiring에 숨기지 않고 canonical edge/data로 표현한다.

**Why:** 우연한 실행 순서가 의미를 바꾸면 재현성과 검증 가능성이 사라진다.
**Applies when:** all non-trivial software projects
**Enforcement:** lint/probe/review
**Sources:** `CLAUDE.md:394-422`; `CLAUDE.md:737-766`; `CLAUDE.md:948-961`; `docs/development/document-system.md:72-72`; `docs/principles/constitution.md:154-166`; `docs/principles/constitution.md:311-369`

### R-SEM-002 — Declared access equals runtime access
**Portability:** CONDITIONAL  
**Strength:** MUST  
compile/bind 단계에서 선언한 dependency·read/write·service·authority 범위를 runtime이 몰래 확대하지 못하게 한다.

**Why:** declared graph와 실제 graph가 다르면 정적 검증과 권한 모델이 거짓이 된다.
**Applies when:** access/dependency/capability를 사전에 선언하는 architecture일 때
**Enforcement:** compile/bind validation + runtime probe
**Sources:** `CLAUDE.md:440-444`; `docs/principles/constitution.md:138-144`

### R-SEM-003 — Canonical truth and rebuildable projections
**Portability:** CONDITIONAL  
**Strength:** MUST  
중앙 권위 모델에서는 같은 semantic truth를 복제해 synchronization으로 correctness를 유지하지 않고 canonical truth와 rebuildable projection/cache/index를 구분한다. 분산·multi-master 모델에서는 단일 물리 정본 대신 replica identity, merge/conflict law, causal authority를 명시적으로 소유한다.

**Why:** 핵심은 물리 복제 수가 아니라 semantic authority와 conflict law가 하나의 계약으로 닫히는 것이다.
**Applies when:** state를 여러 representation/replica로 유지할 때
**Enforcement:** architecture-review/probe
**Sources:** `CLAUDE.md:737-766`; `docs/principles/constitution.md:113-124`; `docs/quality/security-gates.md:326-373`

### R-SEM-004 — Contracts close a semantic completeness matrix
**Portability:** CORE  
**Strength:** MUST  
중요 semantic contract는 적용 가능한 identity, ownership, state, transition, authority, ordering, visibility/atomicity, failure, cancellation, retry/idempotency, replay, persistence, reconfiguration, concurrency, unknown/opaque, observability를 답하고 해당하지 않는 항목은 명시적으로 N/A로 닫는다.

**Why:** 이름만 존재하는 계약은 구현자가 빈 의미를 각자 발명하게 만든다.
**Applies when:** all non-trivial software projects
**Enforcement:** document-lint/review
**Sources:** `CLAUDE.md:737-766`; `docs/principles/constitution.md:225-285`; `docs/quality/security-gates.md:422-432`

### R-SEM-005 — Reject structurally knowable defects early
**Portability:** CONDITIONAL  
**Strength:** MUST  
missing/ambiguous dependency, illegal scope, incompatible schema처럼 실행 전에 결정 가능한 구조적 오류는 가능한 한 compile/bind/validation 단계에서 거부하고 runtime first-match, silent fallback, retry로 숨기지 않는다.

**Why:** deterministic한 결함을 runtime nondeterminism으로 미루지 않는다.
**Applies when:** 사전 구조 검증이 가능한 시스템일 때
**Enforcement:** compile/bind validation
**Sources:** `CLAUDE.md:440-442`; `docs/principles/constitution.md:371-385`

### R-SEM-006 — Observable changes have explicit commit boundaries
**Portability:** CONDITIONAL  
**Strength:** MUST  
관측 가능한 상태 전이는 explicit commit/publish boundary를 가지며 서로 다른 의미의 commit 경계를 같은 것으로 가정하지 않는다.

**Why:** 부분 visibility, crash semantics, side-effect ordering을 명확하게 한다.
**Applies when:** transaction/publish/durable commit 등 관측 경계가 존재할 때
**Enforcement:** contract/probe
**Sources:** `CLAUDE.md:556-574`; `CLAUDE.md:737-766`; `docs/principles/constitution.md:400-412`

### R-SEM-007 — External and async results return through canonical ingress
**Portability:** CONDITIONAL  
**Strength:** MUST  
callback·worker·provider가 authoritative state를 직접 변경하지 않고 외부/비동기 결과를 owner가 정한 ingress/result/transaction 경계로 변환해 반영한다.

**Why:** completion order가 hidden mutation authority가 되는 것을 막는다.
**Applies when:** 비동기 작업이나 외부 provider 결과가 authoritative state에 영향을 줄 때
**Enforcement:** dependency-lint/probe
**Sources:** `CLAUDE.md:450-468`; `CLAUDE.md:737-766`; `docs/principles/constitution.md:146-152`

### R-SEM-008 — Local cancellation is not an external terminal
**Portability:** CONDITIONAL  
**Strength:** MUST  
로컬 task 취소를 이미 외부에 제출된 side effect의 성공·실패·취소 증거로 취급하지 않는다. 실제 상태를 모르면 indeterminate/unknown terminal을 표현한다.

**Why:** 외부 세계의 상태를 근거 없이 추측하지 않는다.
**Applies when:** 외부 side effect 또는 remote operation이 있을 때
**Enforcement:** contract/probe
**Sources:** `CLAUDE.md:468-468`; `CLAUDE.md:737-766`; `docs/core/authority-platform.md:194-220`; `docs/core/authority-platform.md:346-360`; `docs/principles/constitution.md:229-279`

### R-SEM-009 — Replay reproduces recorded semantic evidence
**Portability:** CONDITIONAL  
**Strength:** MUST  
replay/recovery는 기록된 semantic input·decision·generation evidence를 재현하고 이미 publish된 외부 side effect를 새로 실행해 다른 결과를 만들지 않는다. evidence가 맞지 않으면 비슷한 상태를 추측해 이어 가지 않는다.

**Why:** replay가 새로운 실행으로 변질되면 동일성과 감사 가능성이 깨진다.
**Applies when:** replay, recovery, event sourcing, deterministic reproduction을 제공할 때
**Enforcement:** replay-probe
**Sources:** `CLAUDE.md:470-487`; `CLAUDE.md:737-766`; `docs/principles/constitution.md:262-263`

### R-SEM-010 — Incremental by construction
**Portability:** CONDITIONAL  
**Strength:** MUST  
증분 처리가 요구되는 시스템은 변화 단위, dependency, invalidation, reuse 경계를 처음부터 semantic model에 포함하고 전체 재계산 후 나중 최적화를 기본 구조로 삼지 않는다.

**Why:** correctness와 performance가 같은 dependency model을 공유하게 한다.
**Applies when:** 큰 데이터셋/interactive latency 때문에 증분성이 요구될 때
**Enforcement:** architecture-review/performance-probe
**Sources:** `docs/principles/constitution.md:387-398`

### R-SEM-011 — Unknown and opaque states are preserved, not guessed
**Portability:** CONDITIONAL  
**Strength:** MUST  
모르는 schema/variant/owner/evidence를 guessed default나 가장 가까운 known case로 해석하지 않는다. 보존 가능한 opaque data와 금지해야 할 operation을 명시한다.

**Why:** 정보 부재를 임의 의미로 채우면 데이터 손실과 비결정성이 발생한다.
**Applies when:** versioning, opaque extension, partial knowledge가 가능한 시스템일 때
**Enforcement:** contract/probe
**Sources:** `docs/development/document-system.md:137-137`; `docs/principles/constitution.md:274-275`; `docs/quality/architecture-probes.md:23-44`

### R-SEM-012 — Performance does not justify semantic bypass
**Portability:** CORE  
**Strength:** MUST  
성능 목표는 canonical boundary 안에서 달성한다. hot path 최적화가 owner, authority, commit, isolation, validation 경계를 우회하는 근거가 되지 않는다.

**Why:** 빠른 잘못된 경로는 correctness debt를 구조화할 뿐이다.
**Applies when:** all non-trivial software projects
**Enforcement:** review/performance-probe
**Sources:** `CLAUDE.md:737-766`; `docs/principles/constitution.md:423-432`; `docs/quality/security-gates.md:206-241`; `docs/quality/security-gates.md:435-450`

### R-SEM-013 — Convenience surfaces lower to the canonical model
**Portability:** CONDITIONAL  
**Strength:** MUST  
DSL, visual editor, helper SDK, high-level API 같은 편의 surface는 독립 semantic runtime을 만들지 않고 동일한 canonical declarations/contracts로 lowering된다.

**Why:** 쉬운 길과 강한 길의 의미가 갈라지는 것을 막는다.
**Applies when:** 여러 authoring/frontend/API surface가 동일 시스템을 생성할 때
**Enforcement:** equivalence-probe
**Sources:** `docs/authoring/authoring-model.md:5-60`; `docs/authoring/language-frontends.md:5-20`; `docs/principles/constitution.md:434-458`

### R-SEM-014 — Semantic identity is distinct from execution identity
**Portability:** CONDITIONAL  
**Strength:** MUST  
process, thread, connection, handle 같은 물리 execution identity와 logical operation/object/principal/generation 같은 semantic identity를 합치지 않는다.

**Why:** 재시작·분산·helper process에서 물리 lifetime 변화가 semantic identity를 잘못 바꾸는 것을 막는다.
**Applies when:** 물리 실행체가 재시작/복수화될 수 있을 때
**Enforcement:** contract/probe
**Sources:** `docs/ARCHITECTURE.md:63-78`; `docs/system/system-boundary.md:152-169`

### R-SEM-015 — Names do not prove identity or state carry
**Portability:** CONDITIONAL  
**Strength:** MUST  
같은 이름·key·provider label이 같은 instance, authority, generation, state carry를 의미한다고 추정하지 않는다. identity와 carry 조건은 별도 계약으로 정의한다.

**Why:** 이름 재사용이 stale alias와 잘못된 continuation을 만드는 것을 막는다.
**Applies when:** reconfigure/restart/provider replacement가 있을 때
**Enforcement:** contract/probe
**Sources:** `CLAUDE.md:580-604`; `CLAUDE.md:737-766`

### R-SEM-016 — Compiled topology is frozen unless reconfiguration is explicit
**Portability:** CONDITIONAL  
**Strength:** MUST  
compile/bind로 topology를 확정한 architecture에서는 running phase가 manifest/catalog/name lookup을 다시 수행해 숨은 wiring을 추가하지 않는다. topology 변화는 별도 reconfiguration contract를 거친다.

**Why:** compile-time graph와 runtime graph가 달라지는 것을 막는다.
**Applies when:** topology를 compile/bind 단계에서 확정하는 architecture일 때
**Enforcement:** runtime-probe/lint
**Sources:** `docs/principles/constitution.md:168-172`

## Data Durability

### R-DATA-001 — User-owned content survives application metadata loss
**Portability:** CONDITIONAL  
**Strength:** SHOULD  
일반 형식으로 표현 가능한 사용자 콘텐츠는 애플리케이션 전용 metadata나 해당 제품 자체가 없어져도 가능한 범위에서 읽고 보존할 수 있어야 한다.

**Why:** 사용자 데이터 소유권과 장기 보존성을 제품 전용 환경 metadata에 종속시키지 않는다.
**Applies when:** 사용자가 장기 보존하거나 다른 도구로 다룰 수 있는 artifact/content를 소유할 때
**Enforcement:** format/recovery-probe
**Sources:** `docs/principles/constitution.md:180-184`

### R-DATA-002 — External writes are conflict-aware
**Portability:** CONDITIONAL  
**Strength:** MUST  
외부에서 동시에 변경될 수 있는 artifact를 저장할 때 예상 identity/revision/digest와 현재 상태를 비교하고 mismatch를 conflict로 처리한다. 조용한 overwrite를 기본 동작으로 삼지 않는다.

**Why:** 다른 writer의 변경을 무음으로 파괴하지 않는다.
**Applies when:** 공유 파일/외부 artifact/다중 writer가 존재할 때
**Enforcement:** CAS/conflict-probe
**Sources:** `CLAUDE.md:556-574`; `docs/domain/persistence.md:312-355`; `docs/principles/constitution.md:186-188`

## Security

### R-SEC-001 — Trust and isolation terminology must match enforcement
**Portability:** CONDITIONAL  
**Strength:** MUST  
실제로 격리되지 않은 in-process/native 실행을 sandbox나 isolated security boundary로 부르지 않는다. security claim은 실제 권한 enforcement 수준을 정확히 반영한다.

**Why:** 이름이 실제 보안 보장을 과장하면 threat model과 사용자 판단이 거짓이 된다.
**Applies when:** sandbox/isolation/trust tier를 주장할 때
**Enforcement:** security-review/adversarial-probe
**Sources:** `docs/principles/constitution.md:190-194`; `docs/system/system-boundary.md:146-150`

## Decision Policy

### R-DEC-001 — Classify ambiguity before asking for a decision
**Portability:** CORE  
**Strength:** MUST  
애매함은 먼저 Specified Architecture, Implementation Freedom, Spec/Local Design Defect, Unspecified Product Policy로 분류한다. 실제 제품 결정 후보는 마지막 경우뿐이다.

**Why:** 기술적 책임을 제품 선택으로 외부화하지 않는다.
**Applies when:** all non-trivial software projects
**Enforcement:** review
**Sources:** `CLAUDE.md:221-266`; `docs/principles/product-and-decision-policy.md:57-76`

### R-DEC-002 — Product-decision threshold is high
**Portability:** CORE  
**Strength:** MUST  
제품/사용자 결정을 요구하기 전에 owner와 dependency를 읽고 canonical extension point를 조사하며, 기존 invariant로 우열을 연역할 수 없고 모든 후보가 correctness/security/determinism/extensibility를 만족하며 실제 사용자 경험 차이가 남는지 확인한다.

**Why:** 질문을 보수성의 대체물로 사용하지 않는다.
**Applies when:** all non-trivial software projects
**Enforcement:** decision-checklist
**Sources:** `docs/ARCHITECTURE.md:144-146`; `docs/principles/change-and-self-correction.md:186-186`; `docs/principles/product-and-decision-policy.md:78-91`

### R-DEC-003 — Implementation difficulty is not product policy
**Portability:** CORE  
**Strength:** MUST  
새 type/field가 필요하거나 refactor가 크고 파일이 많이 바뀌거나 기존 internal API를 폐기해야 한다는 이유만으로 제품 결정을 요구하지 않는다.

**Why:** 구현 비용과 제품 의미는 다른 축이다.
**Applies when:** all non-trivial software projects
**Enforcement:** review
**Sources:** `CLAUDE.md:241-252`; `docs/ARCHITECTURE.md:144-144`; `docs/principles/product-and-decision-policy.md:93-107`

### R-DEC-004 — Architecture change means a semantic-law change
**Portability:** CORE  
**Strength:** MUST  
변경 규모가 아니라 system-wide closed law, dependency direction, durable truth owner, public contract의 기본 의미, identity/ordering/authority/failure law가 바뀌는지로 architecture change를 판정한다.

**Why:** 큰 refactor를 architecture change로 과대분류하거나 실제 law 변화를 놓치는 것을 막는다.
**Applies when:** all non-trivial software projects
**Enforcement:** change-classification
**Sources:** `CLAUDE.md:190-217`; `CLAUDE.md:737-766`; `docs/principles/change-and-self-correction.md:5-60`

### R-DEC-005 — Absence from the current document is not proof of an architecture change
**Portability:** CORE  
**Strength:** MUST  
요구가 문서에 없다는 사실만으로 architecture 변경을 선언하지 않는다. 기존 extension point나 contract extension으로 자연스럽게 표현 가능한지 먼저 검증한다.

**Why:** 문서 공백과 구조적 표현 불가능성을 구분한다.
**Applies when:** all non-trivial software projects
**Enforcement:** review
**Sources:** `docs/principles/change-and-self-correction.md:62-72`

### R-DEC-006 — Fix local design defects at their owner
**Portability:** CORE  
**Strength:** MUST  
closed law를 바꿀 필요 없이 owner-local abstraction이 좁거나 잘못되었다면 하위 workaround를 추가하지 않고 해당 owner를 재설계한다.

**Why:** 잘못된 local API의 호환성을 보존하기 위해 전역 architecture를 왜곡하지 않는다.
**Applies when:** all non-trivial software projects
**Enforcement:** review
**Sources:** `docs/principles/change-and-self-correction.md:74-87`

### R-DEC-007 — Architecture-defect claims carry a proof burden
**Portability:** CORE  
**Strength:** MUST  
architecture defect를 주장하려면 현재 owner, 시도한 extension point, 표현 불가능한 정확한 이유, 깨지는 invariant, implementation/contract extension으로 해결 불가능한 이유, 필요한 최소 law change와 최소 반례를 제시한다.

**Why:** 익숙한 API가 없다는 사실과 구조적으로 표현 불가능한 사실을 분리한다.
**Applies when:** all non-trivial software projects
**Enforcement:** decision-record
**Sources:** `CLAUDE.md:629-651`; `docs/principles/change-and-self-correction.md:91-101`; `docs/principles/change-and-self-correction.md:151-167`

### R-DEC-008 — Use a deterministic default reasoning order
**Portability:** CORE  
**Strength:** MUST  
명시적 제품 결정을 기다릴 필요가 없으면 invariant를 더 강하게 보존하고, canonical owner 재사용, 더 일반적·조합 가능한 abstraction, truth 추가보다 derived state, runtime fallback보다 사전 검증, 암묵 규칙보다 explicit identity/order/failure를 순서대로 선호한다.

**Why:** 동등해 보이는 내부 선택을 일관된 engineering 기준으로 좁힌다.
**Applies when:** all non-trivial software projects
**Enforcement:** review
**Sources:** `docs/principles/product-and-decision-policy.md:125-138`

### R-DEC-009 — Settings are not correctness escape hatches
**Portability:** CORE  
**Strength:** MUST  
correct/incorrect, safe/unsafe, deterministic/order-dependent, canonical path/bypass 같은 선택을 사용자가 떠안는 Setting으로 만들지 않는다. 제공하는 선택지는 모두 핵심 invariant를 만족해야 한다.

**Why:** 구현 결함을 제품 옵션으로 숨기지 않는다.
**Applies when:** all non-trivial software projects
**Enforcement:** product-review
**Sources:** `docs/principles/product-and-decision-policy.md:109-123`

### R-DEC-010 — Current code practice is not architecture authority
**Portability:** CORE  
**Strength:** MUST  
현재 코드가 반복해서 사용하는 우회나 관행을 원래 설계 의도로 사후 합리화하지 않는다. owner docs와 다르면 implementation violation인지 owner defect인지 root-cause를 다시 판정한다.

**Why:** 현상과 규범을 뒤집지 않는다.
**Applies when:** all non-trivial software projects
**Enforcement:** review
**Sources:** `CLAUDE.md:13-13`; `CLAUDE.md:813-827`

### R-DEC-011 — Spec defects are normal self-correction signals
**Portability:** CORE  
**Strength:** MUST  
구현 중 반례가 드러나면 잘못된 abstraction을 보존하지 않고 owner와 Probe를 수정한 뒤 계속한다. spec defect 발견 자체를 실패로 취급하지 않는다.

**Why:** 설계를 지킨다는 것을 하위 구조를 영원히 보존하는 것으로 오해하지 않는다.
**Applies when:** all non-trivial software projects
**Enforcement:** review
**Sources:** `CLAUDE.md:307-340`; `docs/principles/change-and-self-correction.md:3-3`; `docs/quality/architecture-probes.md:1446-1459`

## Documentation

### R-DOC-001 — Use stable semantic references, not section positions
**Portability:** CORE  
**Strength:** MUST  
§12, “3장 2절”처럼 문서 구조 위치에 의존한 cross-reference를 사용하지 않고 문서 경로 + 안정적인 concept/rule id로 참조한다.

**Why:** 중간 절을 삽입·삭제하면 위치 참조는 조용히 거짓이 된다.
**Applies when:** all non-trivial software projects
**Enforcement:** doc-lint
**Sources:** `CLAUDE.md:17-17`; `CLAUDE.md:786-786`; `CLAUDE.md:794-799`

### R-DOC-002 — Separate normative truth from status, roadmap, and research
**Portability:** CORE  
**Strength:** MUST  
현재 normative specification에는 현재 규칙만 두고 implementation status, roadmap, benchmark, bug diary, research note를 별도 역할 문서로 분리한다.

**Why:** 설계 미정과 구현 미완료를 혼동하지 않는다.
**Applies when:** all non-trivial software projects
**Enforcement:** doc-structure-lint/review
**Sources:** `docs/development/document-system.md:86-100`; `docs/development/document-system.md:248-262`

### R-DOC-003 — Separate architecture specification from implementation protocol
**Portability:** CORE  
**Strength:** MUST  
architecture docs는 무엇이 참이어야 하는지와 owner/contract를 소유하고, implementation guide는 무엇을 읽고 조사하고 실행·보고할지를 소유한다. implementation guide가 architecture 의미를 새로 만들지 못한다.

**Why:** 도구/작업 습관과 시스템 의미의 권위를 분리한다.
**Applies when:** all non-trivial software projects
**Enforcement:** doc-review
**Sources:** `CLAUDE.md:3-15`; `docs/development/document-system.md:264-276`

### R-DOC-004 — Normative closure owns local semantics and declares external dependencies
**Portability:** CORE  
**Strength:** MUST  
normative package는 프로젝트가 소유하는 type/lifecycle/derivation/failure 의미를 자체 owner에서 닫고, 외부 RFC·표준·언어 spec을 사용하면 그 dependency를 명시한다. external 이름을 핑계로 프로젝트가 소유해야 할 semantics를 생략하지 않는다.

**Why:** “다른 자료를 보면 안다”는 암묵 dependency와 local semantic 누락을 구분한다.
**Applies when:** all non-trivial software projects
**Enforcement:** doc-lint/review
**Sources:** `docs/development/document-system.md:72-72`; `docs/development/document-system.md:121-137`

### R-DOC-005 — Define before normative use
**Portability:** CORE  
**Strength:** MUST  
실행 의미를 좌우하는 canonical named concept는 normative use 전에 정확한 owner와 구현 가능한 definition closure가 있어야 한다.

**Why:** undefined name은 consumer마다 다른 의미를 발명하게 한다.
**Applies when:** all non-trivial software projects
**Enforcement:** doc-lint
**Sources:** `docs/development/document-system.md:139-191`

### R-DOC-006 — A name mention is not a definition
**Portability:** CORE  
**Strength:** MUST  
Record/Variant/Protocol/Derivation 등 canonical concept의 owner는 필요한 field/payload/invariant/state/failure law를 닫아야 하며 예시 label이나 smell 용어를 defines 목록에 올리지 않는다.

**Why:** 이름만 등록하면 downstream 문서가 사실상 shape를 재정의하게 된다.
**Applies when:** all non-trivial software projects
**Enforcement:** definition-closure-lint
**Sources:** `docs/development/document-system.md:156-201`

### R-DOC-007 — Normative vocabulary has fixed strength
**Portability:** CORE  
**Strength:** MUST  
MUST/MUST NOT/SHOULD/MAY/DEFAULT/EXAMPLE의 의미를 문서 집합 전체에서 고정하고 “초기”, “기본”, “예” 같은 모호한 자연어만으로 규범 강도를 대신하지 않는다.

**Why:** 같은 문장이 reader마다 다른 강도로 해석되는 것을 막는다.
**Applies when:** all non-trivial software projects
**Enforcement:** doc-lint/review
**Sources:** `docs/development/document-system.md:233-246`

### R-DOC-008 — Rewriting does not silently weaken invariants
**Portability:** CORE  
**Strength:** MUST  
분할·요약·이름 변경·재작성 시 기존의 더 강한 invariant를 조용히 삭제하지 않는다. 약화에는 명시적 owner change, 이유, 반례/회귀 검증이 필요하다.

**Why:** 편집 작업이 의미 변경을 은폐하지 않게 한다.
**Applies when:** all non-trivial software projects
**Enforcement:** diff-review/probe
**Sources:** `docs/principles/constitution.md:287-291`

### R-DOC-009 — Implementation status has a dedicated owner
**Portability:** CONDITIONAL  
**Strength:** MUST  
무엇이 구현되었고 무엇이 아직 없는지는 status inventory가 소유하며 normative contract나 implementation guide 여러 곳에 중복 누적하지 않는다.

**Why:** 현재 사실의 정본을 하나로 유지한다.
**Applies when:** 구현 현황/status를 문서로 추적하는 경우
**Enforcement:** doc-review
**Sources:** `CLAUDE.md:37-37`; `docs/development/document-system.md:248-289`

### R-DOC-010 — Non-normative documents identify themselves
**Portability:** PROFILE  
**Strength:** DEFAULT  
비규범 문서는 normative owner와 혼동되지 않도록 명시적 marker/metadata를 가진다. 정확한 marker 문법은 프로젝트 profile이 정한다.

**Why:** 문서가 어느 권위를 갖는지 reader와 tooling이 즉시 알 수 있게 한다.
**Applies when:** all non-trivial software projects
**Enforcement:** doc-lint
**Parameters:** `{"default_marker": "> **NON-NORMATIVE.**"}`
**Sources:** `docs/development/document-system.md:248-262`

### R-DOC-011 — Explain problem, responsibility boundary, and forbidden result before jargon
**Portability:** PROFILE  
**Strength:** DEFAULT  
개념 이름과 영어식 정의를 연속 나열하기보다 문제가 무엇인지, 어느 경계가 책임지는지, 어떤 결과가 금지되는지를 먼저 설명하고 코드 이름은 필요한 곳에 붙인다.

**Why:** 문서를 glossary가 아니라 구현 가능한 reasoning artifact로 만든다.
**Applies when:** all non-trivial software projects
**Enforcement:** editorial-review
**Sources:** `docs/development/document-system.md:115-120`

### R-DOC-012 — Dependency edges are semantic, not lexical
**Portability:** CONDITIONAL  
**Strength:** MUST  
문서/contract dependency graph를 관리할 때 다른 owner의 이름을 언급했다는 이유만으로 dependency edge를 만들지 않는다. 그 owner의 canonical type, derivation, lifecycle, result가 없으면 자기 규칙을 구현할 수 없는 실제 semantic dependency만 edge로 기록한다.

**Why:** token reference와 semantic dependency를 섞으면 graph가 과연결되고, 반대로 실제 shape 재정의를 단순 언급으로 오인할 수 있다.
**Applies when:** normative document/contract dependency graph를 machine-readable하게 관리할 때
**Enforcement:** semantic-dependency-lint/review
**Sources:** `docs/development/document-system.md:22-35`; `docs/development/document-system.md:24-35`

## Comments

### R-COM-001 — Code comments are not architecture or history storage
**Portability:** PROFILE  
**Strength:** DEFAULT  
설계 의미는 owner docs, 도구 사용법은 README, 결정 근거는 ADR/decision record, 작업 상태는 status/report, 변경 이력은 VCS가 소유한다. 코드 주석을 이 정보의 장기 저장소로 사용하지 않는다.

**Why:** 코드 옆 설명은 architecture closure/gate와 독립적으로 낡기 쉽다.
**Applies when:** all non-trivial software projects
**Enforcement:** review
**Sources:** `CLAUDE.md:770-809`

### R-COM-002 — Comments exist to prevent local misreading
**Portability:** PROFILE  
**Strength:** DEFAULT  
주석은 비직관적 제약, 외부 contract가 강제하는 형태, 안전성 설명, 의도적으로 하지 않은 일처럼 그 자리에서 코드를 잘못 읽는 것을 막을 때 사용한다. 이름·타입·구조로 표현 가능하면 코드를 고친다.

**Why:** 설명으로 불명확한 코드를 보상하기보다 코드 자체의 semantic clarity를 높인다.
**Applies when:** all non-trivial software projects
**Enforcement:** review
**Sources:** `CLAUDE.md:801-809`

### R-COM-003 — Comments avoid unstable references, history, and code restatement
**Portability:** PROFILE  
**Strength:** DEFAULT  
코드 주석에 절 번호 같은 불안정한 위치 참조, 변경 이력, 코드가 이미 말하는 재서술을 남기지 않는다.

**Why:** 조용히 낡거나 중복되는 주석을 줄인다.
**Applies when:** all non-trivial software projects
**Enforcement:** lint/review
**Sources:** `CLAUDE.md:783-809`

### R-COM-004 — Code comment language is profile-controlled
**Portability:** PROFILE  
**Strength:** DEFAULT  
코드 주석의 자연어는 저장소가 정한 하나의 기본 언어를 따른다.

**Why:** 혼합 언어로 인한 검색·리뷰·일관성 비용을 줄이는 팀 convention이다.
**Applies when:** all non-trivial software projects
**Enforcement:** lint/profile
**Parameters:** `{"default_language": "english"}`
**Sources:** `CLAUDE.md:783-789`

### R-COM-005 — Markdown structures in code comments are profile-controlled
**Portability:** PROFILE  
**Strength:** DEFAULT  
코드 주석 안의 제목·목록·코드펜스·강조 같은 장문 Markdown 구조 허용 여부는 profile로 정한다.

**Why:** 주석이 별도 문서로 성장하는 것을 억제하는 convention이다.
**Applies when:** all non-trivial software projects
**Enforcement:** lint/profile
**Parameters:** `{"default": "forbid"}`
**Sources:** `CLAUDE.md:783-789`

## Conventions

### R-CONV-001 — Formatter configuration is a profile convention
**Portability:** PROFILE  
**Strength:** DEFAULT  
formatter의 기본 설정과 repository-local override 사용 여부는 profile이 소유하며 architecture invariant로 취급하지 않는다.

**Why:** 도구 취향과 semantic correctness를 분리한다.
**Applies when:** all non-trivial software projects
**Enforcement:** profile/CI
**Parameters:** `{"default": "tool-default-no-local-config"}`
**Sources:** `CLAUDE.md:50-52`

### R-CONV-002 — Canonical document ID grammar is a profile convention
**Portability:** PROFILE  
**Strength:** DEFAULT  
문서/계약 ID의 문법은 tooling이 안정적으로 검증할 수 있는 형태로 profile에서 고정한다.

**Why:** ID 형식은 안정적 참조를 돕지만 특정 kebab/ascii 문법 자체는 팀 convention이다.
**Applies when:** all non-trivial software projects
**Enforcement:** manifest-lint/profile
**Parameters:** `{"default": "lowercase-ascii-kebab"}`
**Sources:** `docs/development/document-system.md:63-72`

## Evidence

### R-EV-001 — Claims require proportionate enforcement or evidence
**Portability:** CORE  
**Strength:** MUST  
문서에 “금지”라고 쓰는 데서 끝내지 않고 가능한 invariant는 lint, compile/bind check, negative test, adversarial fixture, runtime probe로 기계화한다. 자동 검증이 어려우면 최소한 명시적 review trigger와 필요한 evidence를 남긴다.

**Why:** 주장의 강도보다 gate가 약하면 문서와 실제가 쉽게 갈라진다.
**Applies when:** all non-trivial software projects
**Enforcement:** meta-review
**Sources:** `CLAUDE.md:54-54`; `CLAUDE.md:366-366`; `CLAUDE.md:737-766`; `docs/quality/security-gates.md:3-8`; `docs/quality/security-gates.md:87-100`; `docs/quality/security-gates.md:243-254`; `docs/quality/security-gates.md:256-268`

### R-EV-002 — Probes falsify specification closure, not merely demonstrate a happy path
**Portability:** CORE  
**Strength:** MUST  
architecture Probe는 구현자가 새 semantic rule을 발명하지 않고 contract를 구현할 수 있는지 반증하려는 최소 reference harness로 설계한다.

**Why:** happy path 시연만으로는 명세가 닫혔는지 알 수 없다.
**Applies when:** all non-trivial software projects
**Enforcement:** probe-design-review
**Sources:** `CLAUDE.md:737-766`; `docs/quality/architecture-probes.md:2-6`

### R-EV-003 — Validation failures identify their layer
**Portability:** CORE  
**Strength:** MUST  
검증 결과는 implementation defect, owner-local design defect, specification defect 등 실패 원인의 층위를 구분한다. 해결 가능한 기술 문제를 막연한 NEEDS_DECISION으로 남기지 않는다.

**Why:** 수정 책임과 다음 행동을 명확하게 만든다.
**Applies when:** all non-trivial software projects
**Enforcement:** probe-result-schema
**Sources:** `CLAUDE.md:368-377`; `docs/quality/architecture-probes.md:8-21`; `docs/quality/architecture-probes.md:1446-1459`

### R-EV-004 — Every critical probe has a negative path and forbidden observable state
**Portability:** CORE  
**Strength:** MUST  
중요 invariant의 Probe는 정상 path와 반례를 쌍으로 두고 precondition, stimulus/interleaving/crash point, expected state뿐 아니라 절대로 관측되면 안 되는 forbidden state를 정의한다.

**Why:** “무엇이 일어나야 하는가”만 검사하면 잘못된 추가 상태를 놓칠 수 있다.
**Applies when:** all non-trivial software projects
**Enforcement:** probe-schema-lint
**Sources:** `CLAUDE.md:379-379`; `CLAUDE.md:737-766`; `docs/quality/architecture-probes.md:46-64`; `docs/quality/architecture-probes.md:1351-1395`

### R-EV-005 — Control semantic interleavings explicitly
**Portability:** CONDITIONAL  
**Strength:** MUST  
동시성/ordering 검증에 필요한 interleaving을 실제 thread timing 운에 맡기지 않고 fixture/scheduler data로 명시한다.

**Why:** 비결정적 테스트가 의미 검증을 대신하지 않게 한다.
**Applies when:** concurrency/interleaving이 semantic result에 영향을 줄 때
**Enforcement:** deterministic-fixture
**Sources:** `docs/quality/architecture-probes.md:1395-1395`

### R-EV-006 — Readiness rises only with evidence
**Portability:** CONDITIONAL  
**Strength:** MUST  
DRAFT, SEMANTICALLY_CLOSED, PROBE_VALIDATED, IMPLEMENTATION_READY 같은 readiness 상태는 장식이 아니며 mandatory probe와 실제 result evidence 없이 validated/ready를 주장하지 않는다.

**Why:** 준비 상태를 희망이나 문서 존재 여부가 아니라 검증 가능한 증거에 연결한다.
**Applies when:** 명시적인 contract readiness 상태를 추적하는 경우
**Enforcement:** readiness-registry-lint
**Sources:** `CLAUDE.md:344-364`; `CLAUDE.md:737-766`; `docs/ARCHITECTURE.md:240-252`; `docs/development/document-system.md:278-301`; `docs/quality/architecture-probes.md:1397-1419`

### R-EV-007 — Counterexamples can downgrade readiness
**Portability:** CORE  
**Strength:** MUST  
새 반례가 현재 contract를 깨면 예외 처리로 status를 방어하지 않고 readiness를 적절히 낮춘 뒤 owner와 Probe를 보강한다.

**Why:** 상태 label보다 실제 반례를 우선한다.
**Applies when:** all non-trivial software projects
**Enforcement:** readiness-review
**Sources:** `CLAUDE.md:362-366`; `docs/quality/architecture-probes.md:1417-1419`

### R-EV-008 — A bypass cannot make a probe pass
**Portability:** CORE  
**Strength:** MUST  
test-only branch, raw state mutation, special host path, parallel owner 등 검증 대상 invariant를 우회해 fixture를 통과하면 PASS로 인정하지 않는다.

**Why:** Probe가 구현의 실제 경로를 검증하도록 한다.
**Applies when:** all non-trivial software projects
**Enforcement:** probe-review
**Sources:** `docs/quality/architecture-probes.md:1433-1445`; `docs/quality/security-gates.md:406-420`

### R-EV-009 — Whole-corpus closure validators enumerate the full violation set
**Portability:** CONDITIONAL  
**Strength:** MUST  
전수 closure를 주장하는 validator는 첫 오류에서 멈추는 spot check가 아니라 대상 corpus 전체의 violation set을 수집하고 0건일 때만 PASS한다.

**Why:** 한 오류를 고친 뒤 다음 오류가 드러나는 반복을 줄이고 closure 주장을 실제로 검증한다.
**Applies when:** whole-corpus completeness/closure validator를 제공할 때
**Enforcement:** validator-contract
**Sources:** `docs/development/document-system.md:187-191`

### R-EV-010 — Generated semantic inventories are navigation aids, not truth owners
**Portability:** CONDITIONAL  
**Strength:** MUST  
source/manifest/schema에서 생성한 inventory는 탐색과 중복 방지에 사용하되 semantic truth의 정본으로 승격하지 않는다.

**Why:** generated index가 owner docs/code와 별도 authority가 되는 것을 막는다.
**Applies when:** generated index/inventory를 제공할 때
**Enforcement:** tooling-review
**Sources:** `docs/development/document-system.md:217-231`

### R-EV-011 — Security claims are tested against actual enforcement
**Portability:** CONDITIONAL  
**Strength:** MUST  
sandbox/isolation/capability 같은 security claim은 정상 기능 테스트뿐 아니라 우회·권한 확대·stale authority를 시도하는 adversarial fixture로 실제 enforcement를 검증한다.

**Why:** 명목상 경계와 실제 경계를 구분한다.
**Applies when:** 보안/격리/capability 보장을 주장할 때
**Enforcement:** security-probe
**Sources:** `docs/quality/security-gates.md:40-71`

### R-EV-012 — Performance uses structural metrics as well as wall-clock metrics
**Portability:** CONDITIONAL  
**Strength:** SHOULD  
성능 요구는 wall-clock 숫자만 보지 않고 allocations, bytes copied, node count, invalidation/reuse, queue depth 같은 architecture-relevant structural metric도 가능한 범위에서 기록한다.

**Why:** 환경 노이즈와 semantic complexity 회귀를 분리한다.
**Applies when:** 성능이 architecture requirement인 경우
**Enforcement:** benchmark/structural-metric
**Sources:** `CLAUDE.md:15-15`; `CLAUDE.md:737-766`; `docs/quality/security-gates.md:206-241`

### R-EV-013 — Stage and readiness are proven by behavior, not structure existence
**Portability:** CONDITIONAL  
**Strength:** MUST  
phase/stage/readiness 완료는 struct, module, document가 존재한다는 사실이 아니라 그 단계가 약속한 contract와 mandatory probe/evidence가 통과했는지로 판정한다.

**Why:** placeholder 구조물의 존재를 진척으로 오인하면 실제 semantic closure가 뒤로 밀린다.
**Applies when:** phase/stage/readiness 기반 구현 계획을 사용하는 경우
**Enforcement:** stage-gate/readiness-registry
**Sources:** `docs/ARCHITECTURE.md:240-252`; `docs/quality/architecture-probes.md:1463-1463`

### R-EV-014 — Probe harnesses remain minimal and non-authoritative
**Portability:** CORE  
**Strength:** MUST  
reference probe/conformance harness는 반례를 보이는 데 필요한 최소 구현으로 유지하고 제품의 canonical path를 대신하는 거대한 대체 subsystem이나 별도 authority가 되지 않게 한다.

**Why:** 검증용 구현이 독립 제품 경로가 되면 실제 architecture 대신 test architecture를 검증하게 된다.
**Applies when:** reference harness, probe runtime, conformance implementation을 만드는 경우
**Enforcement:** probe-review
**Sources:** `docs/quality/architecture-probes.md:1465-1465`

## Completion

### R-COMP-001 — “It works” is not a complete definition of done
**Portability:** CORE  
**Strength:** SHOULD  
기능 완료는 단일 happy-path 동작이 아니라 프로젝트가 선언한 적용 가능한 correctness, determinism, security, durability, accessibility, performance, extensibility 등의 품질 조건을 누적으로 만족했는지로 판정한다.

**Why:** 기능 존재와 제품/시스템 완성도를 구분한다.
**Applies when:** all non-trivial software projects
**Enforcement:** completion-checklist
**Sources:** `docs/principles/product-and-decision-policy.md:40-55`

### R-COMP-002 — Known architecture violations cannot be closed as temporary debt
**Portability:** CORE  
**Strength:** MUST  
완료 범위 안의 알려진 architecture/spec violation을 “임시”, “나중에 정리”라는 이유로 완료 처리하지 않는다. scope에서 제외한다면 owner/status에 명시적으로 남긴다.

**Why:** 숨은 debt를 완료 상태로 포장하지 않는다.
**Applies when:** all non-trivial software projects
**Enforcement:** completion-review
**Sources:** `CLAUDE.md:737-768`; `docs/principles/change-and-self-correction.md:112-121`; `docs/principles/change-and-self-correction.md:149-149`

## Greenfield

### R-GREEN-001 — Do not preserve speculative legacy in unreleased greenfield code
**Portability:** CONDITIONAL  
**Strength:** MUST  
외부 사용자·데이터·공개 compatibility obligation이 아직 없는 greenfield 단계에서는 잘못된 internal API를 보존하기 위한 legacy, migration, compatibility layer를 기본적으로 남기지 않는다.

**Why:** 존재하지 않는 과거와의 호환성을 위해 현재 설계를 왜곡하지 않는다.
**Applies when:** pre-release greenfield이며 외부 compatibility/data obligation이 없을 때
**Does not apply when:** 이미 외부 사용자, 공개 API, 저장 데이터, 배포된 schema의 호환 의무가 있을 때
**Enforcement:** review
**Sources:** `CLAUDE.md:15-15`; `CLAUDE.md:681-681`; `docs/principles/change-and-self-correction.md:47-47`; `docs/principles/change-and-self-correction.md:87-87`