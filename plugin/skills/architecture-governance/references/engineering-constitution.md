# Engineering Constitution

이 문서는 Architecture Governance의 읽기용 정본입니다. 기계가 읽는 규칙의 정본은 `plugin/skills/architecture-governance/references/rule-registry.json`이며, 이 문서는 같은 내용을 사람이 검토하기 쉬운 형태로 펼쳐 놓습니다.

문서가 한국어라면 문장도 자연스러운 한국어로 씁니다. 정확한 기술 용어와 코드 식별자는 필요할 때 원문을 유지하되, 영어 문장 구조를 그대로 옮긴 듯한 표현이나 불필요한 영어 명사 나열은 피합니다. 또한 시스템이나 코드에 모델로 정의되지 않은 의도·지식·감정을 부여하지 않습니다.

# 작업 절차

## R-WORK-001 — 먼저 책임 경계를 찾는다

**강도:** MUST · **범용성:** CORE

사소하지 않은 변경은 먼저 요구의 의미를 누가 정의하는지와 어떤 의존성이 있는지 확인한다. 그다음 정본 모델, 생산자와 소비자, 수명주기, 실패 경로, 확장 지점을 조사하고 구현한다.

**이유:** 이름이 다르다는 이유만으로 같은 책임을 맡는 구조를 하나 더 만들거나 기존 계약을 우회하는 일을 막는다.

**적용 조건:** all non-trivial software projects

**검증:** review/checklist

## R-WORK-002 — 의미를 바꾸면 관련 표현을 함께 점검한다

**강도:** MUST · **범용성:** CORE

공개 의미 필드나 계약을 바꾸면 정본 문서뿐 아니라 그 의미를 직렬화하고 digest를 만들고 compile하고 읽고 검증하고 테스트하는 모든 표현을 함께 확인한다. 정확한 영향 범위는 프로젝트의 의존 관계를 따라 결정한다.

**이유:** 한 표현만 바꾸면 문서, wire format, 런타임, 검증이 서로 다른 의미를 구현할 수 있다.

**적용 조건:** all non-trivial software projects

**검증:** change-impact-checklist/dependency-graph

# 소유권과 책임 경계

## R-OWN-001 — 하나의 의미에는 하나의 정본 책임자가 있다

**강도:** MUST · **범용성:** CORE

같은 의미를 정의하는 규범적 책임은 한 `owner`가 맡는다. 다른 문서와 모듈은 그 정의를 참조하거나 파생 표현으로 사용한다. 정의가 충돌하면 임의의 우선순위를 만들지 말고 소유권 또는 명세 결함으로 처리한다.

**이유:** 정본이 둘 이상이면 시간이 지나며 의미가 갈라지고, 결국 소비자가 어느 쪽을 따를지 다시 결정해야 한다.

**적용 조건:** all non-trivial software projects

**검증:** manifest-lint/review

## R-OWN-002 — 아키텍처는 책임 그래프로 구성한다

**강도:** MUST · **범용성:** CONDITIONAL

아키텍처는 하나의 전역 문서가 모든 세부 규칙을 덮어쓰는 구조가 아니라, 의미별 `owner`와 의존 관계의 그래프로 구성한다. 최상위 문서는 진입점과 지도를 제공하되 세부 정의를 다시 쓰지 않는다.

**이유:** 세부 의미를 전역 문서에 몰아넣으면 책임 경계와 변경 범위가 흐려진다.

**적용 조건:** architecture/specification이 여러 semantic owner나 문서/subsystem으로 나뉘는 경우

**검증:** manifest-lint/review

## R-OWN-003 — 새로 만들기 전에 기존 책임자를 찾는다

**강도:** MUST · **범용성:** CORE

새 Manager·Registry·Store·Dispatcher·Service·UI primitive·저장 표현을 만들기 전에 같은 책임을 이미 맡고 있는 `owner`가 있는지 찾는다. 기존 추상화가 좁다면 병렬 계층을 추가하기보다 정본 `owner`를 일반화하거나 재설계한다.

**이유:** 기능마다 서로 닮은 작은 하위 시스템이 생기는 것을 막는다.

**적용 조건:** all non-trivial software projects

**검증:** review/repository-search

## R-OWN-004 — 병렬 권위를 만들지 않는다

**강도:** MUST · **범용성:** CORE

같은 의미를 결정하는 두 번째 권위 경로를 만들지 않는다. 임시 Adapter·Bridge·Manager는 서로 본질적으로 다른 계약을 연결할 때만 정당하다. 기존 모델의 결함을 가리기 위한 patch budget의 기본값은 0이다.

**이유:** 두 권위를 맞춰 두는 문제는 그 자체로 새로운 의미 문제가 되며, 임시 우회는 구조 결함을 굳힌다.

**적용 조건:** all non-trivial software projects

**검증:** review/lint

## R-OWN-005 — 변경이 국소적일수록 경계가 건강하다

**강도:** SHOULD · **범용성:** CORE

하나의 의미를 바꿀 때 그 의미를 맡은 경계 안에서 대부분의 수정이 끝나는 구조를 선호한다. 관계없는 계층까지 연쇄적으로 손봐야 한다면 수정량보다 책임 경계의 결함을 먼저 의심한다.

**이유:** 변경이 얼마나 국소적인지는 책임 경계가 실제로 의미를 캡슐화하고 있는지 보여 주는 강한 신호다.

**적용 조건:** all non-trivial software projects

**검증:** review

## R-OWN-006 — 구성요소는 계약을 통해 결합한다

**강도:** MUST · **범용성:** CONDITIONAL

서로 독립적으로 확장되어야 하는 구성요소는 상대 구현이나 내부 상태에 직접 기대지 않는다. 정본 계약, 서비스, 액션, 리소스처럼 공개된 의미 경계를 통해 연결한다.

**이유:** 구현에 직접 결합하면 교체·제거·조합이 어려워지고, 보이지 않는 권위 경로가 생긴다.

**적용 조건:** plugin/module/component architecture 또는 독립 교체·제거를 목표로 할 때

**검증:** dependency-lint/review

## R-OWN-007 — 최소 구성도 정상 동작해야 한다

**강도:** MUST · **범용성:** CONDITIONAL

모듈식 또는 선택적 구성을 표방하는 시스템은 선택 기능을 모두 뺀 최소 구성에서도 정상적인 수명주기를 가져야 한다.

**이유:** 최소 구성이 깨진다면 선택 기능 가운데 일부가 사실상 숨은 필수 의존성이라는 뜻이다.

**적용 조건:** optional modules/plugins/features를 지원한다고 주장할 때

**검증:** conformance-test

## R-OWN-008 — 확장 지점과 전역 불변 규칙을 구분한다

**강도:** MUST · **범용성:** CONDITIONAL

확장 가능한 지점과 모든 확장이 따라야 하는 식별자·순서·권한·커밋·실패 규칙을 구분한다. 새 기능을 넣기 위해 전역 불변 규칙을 임의로 열지 않는다.

**이유:** 확장 가능성과 시스템 전체의 의미 일관성을 동시에 지키기 위해서다.

**적용 조건:** 확장/플러그인/다중 구현 생태계를 제공할 때

**검증:** architecture-review

## R-OWN-009 — 우회하기 전에 확장 지점을 넓힌다

**강도:** MUST · **범용성:** CONDITIONAL

표준 확장 지점이 요구를 표현하지 못하면 기능 전용 우회 경로나 별도 경로를 만들기 전에 정본 확장 지점을 보강할 수 있는지 먼저 검토한다.

**이유:** 우회 경로가 일반 기능의 기본 수단이 되면 정본 책임자가 무력화되고 기능별 병렬 시스템이 생긴다.

**적용 조건:** 표준 framework/extension surface와 escape hatch가 함께 존재할 때

**검증:** review

## R-OWN-010 — 확장성은 추가·제거·교체·조합을 모두 포함한다

**강도:** MUST · **범용성:** CONDITIONAL

확장성을 주장하려면 기능을 추가할 수 있는지만 보지 않는다. 제거할 수 있는지, 같은 계약을 만족하는 다른 구현으로 교체할 수 있는지, 서로를 모르는 구성요소를 조합할 수 있는지도 검증한다.

**이유:** 추가만 가능한 구조는 실제로는 결합도가 높은 기능 누적일 수 있다.

**적용 조건:** extensible/modular architecture를 주장할 때

**검증:** conformance-test/review

## R-OWN-011 — 기능별 하위 시스템보다 조합 가능한 기본 요소를 우선한다

**강도:** SHOULD · **범용성:** CORE

서로 다른 기능군을 독립적인 전역 subsystem으로 하나씩 늘리기 전에 공통 의미 요소와 조합으로 표현할 수 있는지 확인한다. 새 기능이 기존 요소로 표현되지 않는다면 곧바로 새 subsystem을 만들기보다 정본 모델에 빠진 개념이 없는지 먼저 점검한다.

**이유:** 기능별 silo가 늘어날수록 식별자, 상태, 액션, 검색, 영속성 같은 공통 의미가 중복되고 상호 운용 비용이 커진다.

**적용 조건:** 여러 기능이 공통 domain/runtime 개념을 공유하는 제품이나 플랫폼

**예외:** 기능들이 실제로 독립된 배포·보안·수명·데이터 경계를 가져 분리된 subsystem이 정당한 경우

**검증:** architecture-review

## R-OWN-012 — 패키지 경계에는 실제 독립성이 필요하다

**강도:** SHOULD · **범용성:** CORE

crate, package, service 같은 물리 경계는 개념 수가 많다는 이유만으로 만들지 않는다. 독립 소비자, 공개 API, 보안 또는 unsafe 경계, 무거운 의존성 격리, process·deploy 경계처럼 실제 독립성이 있을 때 둔다. 책임이 분명하지 않은 common/shared/utils/misc 저장소를 기본 해법으로 삼지 않는다.

**이유:** 물리 경계를 지나치게 늘리면 책임이 선명해지기보다 책임 없는 공유 계층과 의존성 변동만 커질 수 있다.

**적용 조건:** repository/module/package 경계를 설계하거나 재구성할 때

**검증:** architecture-review

# 추상화

## R-ABS-001 — 공통 추상화에는 독립된 근거가 필요하다

**강도:** MUST · **범용성:** CORE

공통 추상화로 승격하려면 서로 다른 두 소비자나 상황이 같은 계약을 우회 없이 사용할 수 있어야 한다. 예외적으로 한 소비자뿐이더라도 명확한 폐쇄형 도메인 법칙을 구현한다면 공통 추상화가 될 수 있다. 첫 기능의 내부 구조에 일반적인 이름을 붙인 것만으로는 충분하지 않다.

**이유:** 두 번째 사례는 기능에 맞춘 추상화와 실제 공통 규칙을 가르는 가장 간단한 검증 수단이다.

**적용 조건:** all non-trivial software projects

**검증:** second-case-review/conformance-test

# 런타임 의미

## R-SEM-001 — 의존성과 순서를 명시적으로 표현한다

**강도:** MUST · **범용성:** CORE

실행·해석·소유권·관측 결과에 영향을 주는 의존성과 순서는 등록 순서, 소스 순서, 컨테이너 순회, 스레드 완료 시점, 숨은 가변 연결에 맡기지 않는다. 정본 그래프나 데이터로 명시한다.

**이유:** 우연한 실행 순서가 의미를 바꾸면 재현성과 검증 가능성이 사라진다.

**적용 조건:** all non-trivial software projects

**검증:** lint/probe/review

## R-SEM-002 — 선언한 접근 범위와 실제 접근 범위를 맞춘다

**강도:** MUST · **범용성:** CONDITIONAL

컴파일 또는 바인딩 단계에서 선언한 의존성, 읽기·쓰기 범위, 서비스, 권한을 런타임이 몰래 넓히지 못하게 한다.

**이유:** 선언 그래프와 실제 그래프가 다르면 정적 검증과 권한 모델이 믿을 수 없게 된다.

**적용 조건:** access/dependency/capability를 사전에 선언하는 architecture일 때

**검증:** compile/bind validation + runtime probe

## R-SEM-003 — 정본과 파생 표현을 구분한다

**강도:** MUST · **범용성:** CONDITIONAL

중앙 권위 모델에서는 같은 의미의 정본을 여러 곳에 복제한 뒤 동기화로 정합성을 유지하려 하지 않는다. 정본과 다시 만들 수 있는 projection·cache·index를 구분한다. 분산 또는 multi-master 모델이라면 단일 물리 정본 대신 replica 식별자, 병합·충돌 규칙, 인과적 권한을 명시한다.

**이유:** 중요한 것은 복제본 수가 아니라 누가 의미를 결정하고 충돌을 어떻게 해결하는지가 하나의 계약으로 정리되어 있는지다.

**적용 조건:** state를 여러 representation/replica로 유지할 때

**검증:** architecture-review/probe

## R-SEM-004 — 중요 계약은 의미의 빈칸을 남기지 않는다

**강도:** MUST · **범용성:** CORE

중요한 계약은 해당되는 범위에서 식별자, 소유권, 상태, 전이, 권한, 순서, 가시성·원자성, 실패, 취소, 재시도·멱등성, 재생, 영속성, 재구성, 동시성, 알 수 없는 상태의 처리, 관측 가능성을 모두 다룬다. 해당하지 않는 항목은 `N/A`로 명시한다.

**이유:** 이름만 있는 계약은 비어 있는 의미를 구현자가 각자 채우게 만든다.

**적용 조건:** all non-trivial software projects

**검증:** document-lint/review

## R-SEM-005 — 실행 전에 알 수 있는 결함은 일찍 거부한다

**강도:** MUST · **범용성:** CONDITIONAL

누락되거나 모호한 의존성, 잘못된 범위, 호환되지 않는 스키마처럼 실행 전에 판별할 수 있는 오류는 가능한 한 컴파일·바인딩·검증 단계에서 거부한다. 런타임의 first-match, 조용한 fallback, 재시도로 숨기지 않는다.

**이유:** 결정적인 결함을 런타임의 비결정성으로 미루지 않기 위해서다.

**적용 조건:** 사전 구조 검증이 가능한 시스템일 때

**검증:** compile/bind validation

## R-SEM-006 — 관측 가능한 변경에는 커밋 경계가 있다

**강도:** MUST · **범용성:** CONDITIONAL

외부에서 관측할 수 있는 상태 변화에는 명시적인 commit 또는 publish 경계가 있어야 한다. 서로 다른 의미의 커밋 경계를 같은 것으로 간주하지 않는다.

**이유:** 부분적으로만 보이는 상태, 크래시 시점의 의미, 부수 효과의 순서를 명확히 하기 위해서다.

**적용 조건:** transaction/publish/durable commit 등 관측 경계가 존재할 때

**검증:** contract/probe

## R-SEM-007 — 외부·비동기 결과는 정본 진입점을 거친다

**강도:** MUST · **범용성:** CONDITIONAL

callback·worker·provider가 정본 상태를 직접 바꾸지 않는다. 외부 또는 비동기 결과는 해당 `owner`가 정한 ingress, result, transaction 경계로 변환한 뒤 반영한다.

**이유:** 완료 순서가 보이지 않는 변경 권한으로 변하는 것을 막는다.

**적용 조건:** 비동기 작업이나 외부 provider 결과가 authoritative state에 영향을 줄 때

**검증:** dependency-lint/probe

## R-SEM-008 — 로컬 취소를 외부 작업의 종료 상태로 간주하지 않는다

**강도:** MUST · **범용성:** CONDITIONAL

로컬 task를 취소했다는 사실만으로 이미 외부에 제출된 부수 효과가 성공·실패·취소되었다고 판단하지 않는다. 실제 상태를 알 수 없으면 `indeterminate` 또는 `unknown`을 표현한다.

**이유:** 외부 세계의 상태를 근거 없이 추측하지 않기 위해서다.

**적용 조건:** 외부 side effect 또는 remote operation이 있을 때

**검증:** contract/probe

## R-SEM-009 — 재생은 기록된 의미 증거를 재현한다

**강도:** MUST · **범용성:** CONDITIONAL

replay와 recovery는 기록된 입력, 결정, generation 증거를 재현한다. 이미 publish된 외부 부수 효과를 다시 실행해 새로운 결과를 만들지 않는다. 기록과 현재 증거가 맞지 않으면 비슷해 보이는 상태를 추측해 이어 가지 않는다.

**이유:** 재생이 새로운 실행으로 바뀌면 동일성과 감사 가능성이 깨진다.

**적용 조건:** replay, recovery, event sourcing, deterministic reproduction을 제공할 때

**검증:** replay-probe

## R-SEM-010 — 증분 처리는 처음부터 모델에 포함한다

**강도:** MUST · **범용성:** CONDITIONAL

증분 처리가 필요한 시스템은 변화 단위, 의존성, 무효화, 재사용 경계를 처음부터 의미 모델에 포함한다. 전체를 매번 다시 계산한 뒤 나중에 최적화하는 구조를 기본값으로 삼지 않는다.

**이유:** 정확성과 성능이 같은 의존성 모델을 공유하게 하기 위해서다.

**적용 조건:** 큰 데이터셋/interactive latency 때문에 증분성이 요구될 때

**검증:** architecture-review/performance-probe

## R-SEM-011 — 모르는 상태는 추측하지 않는다

**강도:** MUST · **범용성:** CONDITIONAL

알 수 없는 schema, variant, owner, evidence를 임의의 기본값이나 가장 가까워 보이는 사례로 해석하지 않는다. 보존 가능한 opaque data와 금지해야 할 동작을 명시한다.

**이유:** 정보가 없다는 사실을 임의의 의미로 채우면 데이터 손실과 비결정성이 생긴다.

**적용 조건:** versioning, opaque extension, partial knowledge가 가능한 시스템일 때

**검증:** contract/probe

## R-SEM-012 — 성능을 이유로 의미 경계를 우회하지 않는다

**강도:** MUST · **범용성:** CORE

성능 목표는 정본 경계 안에서 달성한다. hot path 최적화가 소유권, 권한, 커밋, 격리, 검증 경계를 건너뛰는 근거가 되어서는 안 된다.

**이유:** 빠른 우회 경로도 잘못된 경로라면 구조적 부채만 더 빠르게 쌓는다.

**적용 조건:** all non-trivial software projects

**검증:** review/performance-probe

## R-SEM-013 — 편의 기능도 같은 정본 모델로 내려간다

**강도:** MUST · **범용성:** CONDITIONAL

DSL, visual editor, helper SDK, high-level API 같은 편의 기능은 별도의 의미 체계를 만들지 않는다. 모두 같은 정본 선언과 계약으로 변환되도록 한다.

**이유:** 쉬운 사용 경로와 강한 사용 경로의 의미가 갈라지는 것을 막는다.

**적용 조건:** 여러 authoring/frontend/API surface가 동일 시스템을 생성할 때

**검증:** equivalence-probe

## R-SEM-014 — 의미 식별자와 실행 식별자를 구분한다

**강도:** MUST · **범용성:** CONDITIONAL

process·thread·connection·handle 같은 물리적 실행 식별자와 logical operation·object·principal·generation 같은 의미 식별자를 같은 것으로 취급하지 않는다.

**이유:** 재시작, 분산 실행, helper process 때문에 물리적 수명이 바뀌더라도 의미 식별자가 잘못 바뀌지 않게 하기 위해서다.

**적용 조건:** 물리 실행체가 재시작/복수화될 수 있을 때

**검증:** contract/probe

## R-SEM-015 — 이름만으로 동일성이나 상태 승계를 추정하지 않는다

**강도:** MUST · **범용성:** CONDITIONAL

이름, key, provider label이 같다는 이유만으로 같은 instance, authority, generation이거나 상태를 이어받는다고 판단하지 않는다. 동일성과 상태 승계 조건은 별도의 계약으로 정의한다.

**이유:** 이름 재사용이 오래된 별칭이나 잘못된 연속성을 만드는 것을 막는다.

**적용 조건:** reconfigure/restart/provider replacement가 있을 때

**검증:** contract/probe

## R-SEM-016 — 확정한 실행 토폴로지는 명시적 재구성 없이 바꾸지 않는다

**강도:** MUST · **범용성:** CONDITIONAL

컴파일 또는 바인딩 단계에서 topology를 확정하는 구조라면 실행 중에 manifest·catalog·name lookup을 다시 사용해 숨은 연결을 추가하지 않는다. topology 변경은 별도의 reconfiguration 계약을 거친다.

**이유:** 컴파일 시점의 그래프와 런타임 그래프가 조용히 달라지는 것을 막는다.

**적용 조건:** topology를 compile/bind 단계에서 확정하는 architecture일 때

**검증:** runtime-probe/lint

# 데이터 내구성

## R-DATA-001 — 사용자 데이터는 제품 전용 메타데이터보다 오래 살아남아야 한다

**강도:** SHOULD · **범용성:** CONDITIONAL

일반 형식으로 표현할 수 있는 사용자 콘텐츠는 애플리케이션 전용 metadata나 해당 제품 자체가 없어져도 가능한 범위에서 읽고 보존할 수 있어야 한다.

**이유:** 사용자 데이터의 소유권과 장기 보존성을 제품 전용 환경에 종속시키지 않기 위해서다.

**적용 조건:** 사용자가 장기 보존하거나 다른 도구로 다룰 수 있는 artifact/content를 소유할 때

**검증:** format/recovery-probe

## R-DATA-002 — 외부 저장은 충돌을 감지해야 한다

**강도:** MUST · **범용성:** CONDITIONAL

다른 주체가 동시에 바꿀 수 있는 artifact를 저장할 때는 예상 identity·revision·digest와 현재 상태를 비교하고 불일치를 충돌로 처리한다. 조용히 덮어쓰는 동작을 기본값으로 삼지 않는다.

**이유:** 다른 writer의 변경을 아무 경고 없이 파괴하지 않기 위해서다.

**적용 조건:** 공유 파일/외부 artifact/다중 writer가 존재할 때

**검증:** CAS/conflict-probe

# 보안

## R-SEC-001 — 보안 용어는 실제 보장 수준과 맞아야 한다

**강도:** MUST · **범용성:** CONDITIONAL

실제로 격리되지 않은 in-process 또는 native 실행을 `sandbox`나 `isolated security boundary`라고 부르지 않는다. 보안 관련 표현은 실제 권한 통제와 격리 수준을 정확히 반영해야 한다.

**이유:** 이름이 실제 보장을 과장하면 위협 모델과 사용자의 판단이 틀어진다.

**적용 조건:** sandbox/isolation/trust tier를 주장할 때

**검증:** security-review/adversarial-probe

# 판단 기준

## R-DEC-001 — 결정을 묻기 전에 애매함의 종류를 나눈다

**강도:** MUST · **범용성:** CORE

애매한 상황은 먼저 `Specified Architecture`, `Implementation Freedom`, `Spec/Local Design Defect`, `Unspecified Product Policy`로 분류한다. 실제 제품 결정을 사용자에게 물어야 하는 경우는 마지막 범주뿐이다.

**이유:** 기술적 책임을 제품 선택 문제로 떠넘기지 않기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** review

## R-DEC-002 — 제품 결정을 요구하는 문턱은 높게 둔다

**강도:** MUST · **범용성:** CORE

제품 또는 사용자 결정을 요구하기 전에 관련 `owner`와 의존성을 확인하고 정본 확장 지점을 조사한다. 기존 불변 규칙만으로 우열을 정할 수 없고 모든 후보가 정확성·보안·결정성·확장성을 만족하면서 실제 사용자 경험의 차이가 남을 때만 제품 결정으로 올린다.

**이유:** 질문을 충분한 조사 대신 사용하는 일을 막는다.

**적용 조건:** all non-trivial software projects

**검증:** decision-checklist

## R-DEC-003 — 구현이 어렵다는 이유만으로 제품 결정을 요구하지 않는다

**강도:** MUST · **범용성:** CORE

새 type이나 field가 필요하거나, refactor가 크거나, 많은 파일을 바꾸거나, 기존 내부 API를 폐기해야 한다는 이유만으로 제품 결정을 요구하지 않는다.

**이유:** 구현 비용과 제품 의미는 서로 다른 문제다.

**적용 조건:** all non-trivial software projects

**검증:** review

## R-DEC-004 — 아키텍처 변경은 의미 규칙이 바뀌는 변경이다

**강도:** MUST · **범용성:** CORE

diff 크기가 아니라 시스템 전반의 불변 규칙, 의존성 방향, 영속 정본의 책임자, 공개 계약의 기본 의미, 식별자·순서·권한·실패 규칙이 바뀌는지로 아키텍처 변경 여부를 판단한다.

**이유:** 큰 refactor를 아키텍처 변경으로 과대분류하거나 실제 의미 규칙의 변화를 놓치는 일을 막는다.

**적용 조건:** all non-trivial software projects

**검증:** change-classification

## R-DEC-005 — 현재 문서에 없다는 사실만으로 아키텍처 변경이라고 보지 않는다

**강도:** MUST · **범용성:** CORE

요구가 현재 문서에 적혀 있지 않다는 이유만으로 아키텍처 변경을 선언하지 않는다. 기존 확장 지점이나 계약 확장으로 자연스럽게 표현할 수 있는지 먼저 확인한다.

**이유:** 문서의 공백과 구조적으로 표현할 수 없는 상태를 구분하기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** review

## R-DEC-006 — 지역 설계 결함은 그 책임 경계에서 고친다

**강도:** MUST · **범용성:** CORE

전역 불변 규칙을 바꿀 필요 없이 특정 `owner`의 추상화가 좁거나 잘못되었다면 하위 계층에 우회책을 추가하지 말고 해당 `owner`를 재설계한다.

**이유:** 잘못된 지역 API를 보존하려고 전체 아키텍처를 왜곡하지 않기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** review

## R-DEC-007 — 아키텍처 결함 주장에는 근거가 필요하다

**강도:** MUST · **범용성:** CORE

아키텍처 결함이라고 판단하려면 현재 `owner`, 검토한 확장 지점, 현재 구조로 표현할 수 없는 정확한 이유, 깨지는 불변 규칙, 단순 구현 또는 계약 확장으로 해결할 수 없는 이유, 필요한 최소 규칙 변경과 최소 반례를 제시한다.

**이유:** 익숙한 API가 없다는 사실과 구조적으로 표현할 수 없다는 사실을 구분하기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** decision-record

## R-DEC-008 — 내부 선택에는 일관된 기본 판단 순서를 사용한다

**강도:** MUST · **범용성:** CORE

명시적인 제품 결정을 기다릴 필요가 없다면 다음 순서로 선택지를 좁힌다. 불변 규칙을 더 강하게 보존하고, 정본 `owner`를 재사용하고, 더 일반적이고 조합 가능한 추상화를 택하고, 새 정본보다 파생 상태를 선호하고, 런타임 fallback보다 사전 검증을 선호하고, 암묵 규칙보다 명시적인 식별자·순서·실패 규칙을 택한다.

**이유:** 겉보기에 동등한 내부 선택을 같은 engineering 기준으로 다루기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** review

## R-DEC-009 — 설정으로 정확성 문제를 떠넘기지 않는다

**강도:** MUST · **범용성:** CORE

correct/incorrect, safe/unsafe, deterministic/order-dependent, canonical path/bypass처럼 정확성에 직접 영향을 주는 선택을 사용자 설정으로 넘기지 않는다. 제공하는 모든 선택지는 핵심 불변 규칙을 만족해야 한다.

**이유:** 구현 결함을 제품 옵션처럼 보이게 만들지 않기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** product-review

## R-DEC-010 — 현재 코드의 관행을 아키텍처 권위로 삼지 않는다

**강도:** MUST · **범용성:** CORE

현재 코드에서 반복되는 우회나 관행을 원래 설계 의도로 사후 정당화하지 않는다. 정본 문서와 다르다면 구현 위반인지 정본 설계의 결함인지 원인을 다시 판단한다.

**이유:** 현재 상태와 규범을 뒤집지 않기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** review

## R-DEC-011 — 명세 결함 발견은 정상적인 자기 교정 신호다

**강도:** MUST · **범용성:** CORE

구현 과정에서 반례가 드러나면 잘못된 추상화를 억지로 보존하지 않는다. 정본 `owner`와 Probe를 수정한 뒤 작업을 계속한다. 명세 결함을 발견했다는 사실 자체를 실패로 간주하지 않는다.

**이유:** 설계를 지킨다는 말을 하위 구조를 영원히 고정한다는 뜻으로 오해하지 않기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** review

# 문서

## R-DOC-001 — 위치가 아니라 안정적인 의미를 참조한다

**강도:** MUST · **범용성:** CORE

`§12`, `3장 2절`처럼 문서에서의 위치를 의미 참조로 사용하지 않는다. 다른 문서를 가리킬 때는 문서 경로와 안정적인 개념명 또는 규칙 ID를 함께 쓴다.

**이유:** 절을 추가하거나 삭제해도 참조가 조용히 틀어지지 않게 하기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** doc-lint

## R-DOC-002 — 규범·구현 현황·계획·조사를 섞지 않는다

**강도:** MUST · **범용성:** CORE

현재의 규범 문서에는 현재 유효한 규칙만 둔다. 구현 현황, roadmap, benchmark, bug diary, research note는 각각 맞는 역할의 문서로 분리한다.

**이유:** 설계가 미정인 상태와 구현이 아직 끝나지 않은 상태를 혼동하지 않기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** doc-structure-lint/review

## R-DOC-003 — 아키텍처 명세와 작업 절차를 분리한다

**강도:** MUST · **범용성:** CORE

아키텍처 문서는 무엇이 참이어야 하는지와 누가 그 의미를 책임지는지를 정의한다. 구현 가이드는 무엇을 읽고 조사하고 실행하고 보고할지를 정의한다. 구현 가이드가 시스템 의미를 새로 정하지 않는다.

**이유:** 도구 사용법과 작업 습관이 시스템의 규범적 의미를 덮어쓰지 않게 하기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** doc-review

## R-DOC-004 — 프로젝트가 책임지는 의미는 프로젝트 안에서 닫는다

**강도:** MUST · **범용성:** CORE

프로젝트가 책임지는 type, lifecycle, derivation, failure 의미는 해당 정본 문서에서 충분히 정의한다. 외부 RFC, 표준, 언어 명세를 따를 때는 그 의존성을 명시하되, 외부 이름을 이유로 프로젝트가 정해야 할 의미를 생략하지 않는다.

**이유:** 외부 자료에 대한 암묵적 의존성과 프로젝트 내부 의미의 누락을 구분하기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** doc-lint/review

## R-DOC-005 — 규범적으로 쓰기 전에 정의한다

**강도:** MUST · **범용성:** CORE

실행 의미를 바꾸는 정본 개념은 규범 문서에서 사용하기 전에 책임 문서와 구현 가능한 정의를 갖춰야 한다.

**이유:** 정의되지 않은 이름을 각 소비자가 서로 다르게 해석하는 일을 막는다.

**적용 조건:** all non-trivial software projects

**검증:** doc-lint

## R-DOC-006 — 이름을 언급했다고 정의가 된 것은 아니다

**강도:** MUST · **범용성:** CORE

Record·Variant·Protocol·Derivation 같은 정본 개념은 필요한 field, payload, invariant, state, failure 규칙을 책임 문서에서 충분히 정의한다. 예시나 smell을 정본 개념 목록에 섞지 않는다.

**이유:** 이름만 등록해 두면 하위 문서가 실제 구조를 제각각 다시 정의하게 된다.

**적용 조건:** all non-trivial software projects

**검증:** definition-closure-lint

## R-DOC-007 — 규범어의 강도를 고정한다

**강도:** MUST · **범용성:** CORE

`MUST`, `MUST NOT`, `SHOULD`, `MAY`, `DEFAULT`, `EXAMPLE`의 의미를 문서 집합 전체에서 일관되게 사용한다. `초기`, `기본`, `예` 같은 모호한 표현만으로 규범의 강도를 대신하지 않는다.

**이유:** 같은 문장이 읽는 사람마다 다른 강도로 해석되는 것을 막는다.

**적용 조건:** all non-trivial software projects

**검증:** doc-lint/review

## R-DOC-008 — 편집 과정에서 불변 규칙을 몰래 약화하지 않는다

**강도:** MUST · **범용성:** CORE

문서를 분할·요약·개명·재작성할 때 기존의 더 강한 불변 규칙을 조용히 없애지 않는다. 규칙을 약화하려면 정본의 명시적 변경, 이유, 반례 또는 회귀 검증이 필요하다.

**이유:** 편집 작업이 의미 변경을 숨기지 못하게 하기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** diff-review/probe

## R-DOC-009 — 구현 현황에는 별도의 정본을 둔다

**강도:** MUST · **범용성:** CONDITIONAL

무엇이 구현되었고 무엇이 아직 없는지는 하나의 상태 문서나 상태 인벤토리가 맡는다. 같은 현황을 규범 계약과 여러 구현 가이드에 중복해서 쌓지 않는다.

**이유:** 현재 사실의 정본을 하나로 유지하기 위해서다.

**적용 조건:** 구현 현황/status를 문서로 추적하는 경우

**검증:** doc-review

## R-DOC-010 — 비규범 문서는 자신이 비규범임을 드러낸다

**강도:** DEFAULT · **범용성:** PROFILE

비규범 문서는 규범 문서와 혼동되지 않도록 명시적인 marker 또는 metadata를 둔다. 정확한 표기 방식은 프로젝트 profile에서 정한다.

**이유:** 사람과 도구가 문서의 권위 수준을 바로 구분할 수 있게 하기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** doc-lint

## R-DOC-011 — 용어보다 문제와 책임 경계를 먼저 설명한다

**강도:** DEFAULT · **범용성:** PROFILE

개념 이름과 정의 문장을 연달아 늘어놓기보다 먼저 어떤 문제가 있는지, 어느 경계가 책임지는지, 어떤 결과가 허용되지 않는지를 설명한다. 코드 이름은 필요한 곳에서만 쓴다.

**이유:** 문서를 용어집이 아니라 실제 설계와 구현에 사용할 수 있는 설명으로 만들기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** editorial-review

## R-DOC-012 — 문서 의존성은 단어가 아니라 의미를 따라간다

**강도:** MUST · **범용성:** CONDITIONAL

다른 `owner`의 이름을 언급했다는 이유만으로 문서나 계약 사이에 의존 관계를 만들지 않는다. 그 `owner`의 정본 type, derivation, lifecycle, result가 없으면 자기 규칙을 구현할 수 없는 경우에만 실제 의미 의존성으로 기록한다.

**이유:** 단어 언급과 의미 의존성을 섞으면 그래프가 불필요하게 촘촘해지고, 반대로 실제 구조 재정의를 단순 언급으로 놓칠 수 있다.

**적용 조건:** normative document/contract dependency graph를 machine-readable하게 관리할 때

**검증:** semantic-dependency-lint/review

## R-DOC-013 — 소프트웨어에 모델에 없는 의도나 지식을 부여하지 않는다

**강도:** MUST · **범용성:** CORE

문서와 주석에서 시스템·코드·문서·캐시·런타임 같은 소프트웨어 산출물에 모델로 정의되지 않은 의도, 욕구, 지식, 기억, 판단, 책임을 부여하지 않는다. `캐시가 안다`, `시스템이 원한다`처럼 사람의 정신 상태를 빌린 표현 대신 실제 조건, 상태, 정책, 권한, 관측 결과, 저장된 사실을 적는다. 다만 `parser가 입력을 거부한다`처럼 정의된 동작을 정확히 가리키는 능동형 표현은 허용한다.

**이유:** 의인화는 실제로 어떤 상태를 읽고 어떤 규칙이 결정을 내리는지 숨기기 쉽다. 행위 주체와 근거를 모델에 존재하는 요소로 써야 설계와 구현을 검증할 수 있다.

**적용 조건:** all non-trivial software documentation and code comments

**예외:** ordinary active-voice verbs that directly name a defined operation or contract

**검증:** review/lint where practical

## R-DOC-014 — 문서의 언어에 맞는 자연스러운 기술 문장을 쓴다

**강도:** SHOULD · **범용성:** CORE

문서가 한국어라면 문장 구조도 자연스러운 한국어로 쓴다. 영어 명사를 조사와 함께 줄줄이 끼워 넣거나 영어 관용구를 직역한 동사를 반복하지 않는다. 표준 기술 용어와 코드 식별자는 정확성을 위해 필요할 때만 원문을 유지하고, 처음 의미를 정한 뒤 일관되게 사용한다. 명사 나열보다 누가 무엇을 어떤 조건에서 하는지 드러나는 문장을 우선한다.

**이유:** 기술 용어가 많아도 문장 뼈대까지 번역투가 될 필요는 없다. 자연스러운 문장은 책임, 조건, 원인과 결과를 더 빨리 파악하게 하고 잘못된 해석도 줄인다.

**적용 조건:** human-facing prose in a chosen natural language

**예외:** machine-readable schemas, code identifiers, wire names, quotations, or standardized external terminology whose exact spelling matters

**검증:** editorial review

# 코드 주석

## R-COM-001 — 코드 주석을 아키텍처나 변경 이력의 저장소로 쓰지 않는다

**강도:** DEFAULT · **범용성:** PROFILE

설계 의미는 정본 문서, 도구 사용법은 README, 결정 근거는 ADR 또는 decision record, 작업 상태는 status/report, 변경 이력은 VCS가 맡는다. 코드 주석에 이 정보를 장기 보관하지 않는다.

**이유:** 코드 옆 설명은 정본 문서와 별개로 낡기 쉽다.

**적용 조건:** all non-trivial software projects

**검증:** review

## R-COM-002 — 주석은 그 자리의 오해를 막을 때 쓴다

**강도:** DEFAULT · **범용성:** PROFILE

주석은 비직관적인 제약, 외부 계약이 강제하는 형태, 안전성의 근거, 의도적으로 하지 않은 일처럼 코드를 그 자리에서 잘못 읽을 가능성을 줄일 때 사용한다. 이름·타입·구조로 같은 사실을 표현할 수 있다면 주석보다 코드를 고친다.

**이유:** 설명으로 불명확한 코드를 보상하기보다 코드 자체를 더 명확하게 만들기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** review

## R-COM-003 — 주석에 불안정한 참조·변경 이력·코드 재서술을 남기지 않는다

**강도:** DEFAULT · **범용성:** PROFILE

코드 주석에는 절 번호 같은 위치 기반 참조, 변경 이력, 코드만 읽어도 알 수 있는 내용을 다시 풀어쓴 설명을 남기지 않는다.

**이유:** 쉽게 낡거나 중복되는 주석을 줄이기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** lint/review

## R-COM-004 — 코드 주석의 기본 언어는 프로젝트가 정한다

**강도:** DEFAULT · **범용성:** PROFILE

코드 주석의 자연어는 저장소가 정한 하나의 기본 언어를 따른다.

**이유:** 혼합 언어 때문에 검색과 리뷰가 어려워지는 일을 줄이기 위한 팀 규칙이다.

**적용 조건:** all non-trivial software projects

**검증:** lint/profile

## R-COM-005 — 코드 주석의 장문 Markdown 사용 여부는 프로젝트가 정한다

**강도:** DEFAULT · **범용성:** PROFILE

코드 주석 안에서 제목, 목록, 코드 펜스, 강조 같은 장문 Markdown 구조를 허용할지는 프로젝트 profile에서 정한다.

**이유:** 주석이 별도의 문서처럼 커지는 것을 막기 위한 팀 규칙이다.

**적용 조건:** all non-trivial software projects

**검증:** lint/profile

# 프로젝트 관례

## R-CONV-001 — formatter 설정은 프로젝트 규칙이다

**강도:** DEFAULT · **범용성:** PROFILE

formatter의 기본 설정과 저장소 전용 override 사용 여부는 프로젝트 profile에서 정하며 아키텍처 불변 규칙으로 취급하지 않는다.

**이유:** 도구 취향과 의미적 정확성을 분리하기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** profile/CI

## R-CONV-002 — 문서 ID 문법은 프로젝트 규칙이다

**강도:** DEFAULT · **범용성:** PROFILE

문서와 계약 ID의 문법은 도구가 안정적으로 검증할 수 있는 형태로 프로젝트 profile에서 고정한다.

**이유:** 안정적인 참조에는 ID가 필요하지만 특정 kebab/ascii 형식 자체는 팀 규칙이기 때문이다.

**적용 조건:** all non-trivial software projects

**검증:** manifest-lint/profile

# 검증과 증거

## R-EV-001 — 주장에는 그에 맞는 검증이나 증거가 필요하다

**강도:** MUST · **범용성:** CORE

문서에 `금지`라고 쓰는 것으로 끝내지 않는다. 가능한 불변 규칙은 lint, compile/bind check, negative test, adversarial fixture, runtime probe로 기계적으로 검증한다. 자동화가 어렵다면 최소한 명시적인 review trigger와 필요한 증거를 남긴다.

**이유:** 문서의 강한 표현보다 실제 gate가 약하면 문서와 동작이 쉽게 갈라진다.

**적용 조건:** all non-trivial software projects

**검증:** meta-review

## R-EV-002 — Probe는 성공 사례를 보여 주는 데서 끝나지 않는다

**강도:** MUST · **범용성:** CORE

architecture Probe는 구현자가 새 규칙을 임의로 만들어 내지 않고도 계약을 구현할 수 있는지를 반증하려는 최소 reference harness로 설계한다.

**이유:** 성공 사례만 보여 주어서는 명세가 충분히 닫혔는지 알 수 없다.

**적용 조건:** all non-trivial software projects

**검증:** probe-design-review

## R-EV-003 — 검증 실패는 실패한 층위를 구분한다

**강도:** MUST · **범용성:** CORE

검증 결과는 implementation defect, owner-local design defect, specification defect처럼 원인이 생긴 층위를 구분한다. 해결 가능한 기술 문제를 막연한 `NEEDS_DECISION`으로 남기지 않는다.

**이유:** 수정 책임과 다음 행동을 분명히 하기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** probe-result-schema

## R-EV-004 — 중요 Probe에는 반례와 금지 상태를 함께 둔다

**강도:** MUST · **범용성:** CORE

중요한 불변 규칙을 검증하는 Probe는 정상 경로와 반례를 함께 둔다. precondition, stimulus·interleaving·crash point, expected state뿐 아니라 절대로 관측되면 안 되는 forbidden state도 정의한다.

**이유:** 무엇이 일어나야 하는지만 검사하면 잘못된 추가 상태를 놓칠 수 있다.

**적용 조건:** all non-trivial software projects

**검증:** probe-schema-lint

## R-EV-005 — 동시성 검증의 interleaving을 명시적으로 통제한다

**강도:** MUST · **범용성:** CONDITIONAL

동시성이나 순서 검증에 필요한 interleaving을 실제 thread timing의 운에 맡기지 않는다. fixture 또는 scheduler data로 필요한 순서를 명시한다.

**이유:** 비결정적인 테스트가 의미 검증을 대신하지 않게 하기 위해서다.

**적용 조건:** concurrency/interleaving이 semantic result에 영향을 줄 때

**검증:** deterministic-fixture

## R-EV-006 — 준비 상태는 증거가 있을 때만 올린다

**강도:** MUST · **범용성:** CONDITIONAL

`DRAFT`, `SEMANTICALLY_CLOSED`, `PROBE_VALIDATED`, `IMPLEMENTATION_READY` 같은 readiness 상태는 장식이 아니다. 필수 Probe와 실제 결과 증거 없이 validated 또는 ready라고 주장하지 않는다.

**이유:** 준비 상태를 기대나 문서의 존재 여부가 아니라 검증 가능한 증거에 연결하기 위해서다.

**적용 조건:** 명시적인 contract readiness 상태를 추적하는 경우

**검증:** readiness-registry-lint

## R-EV-007 — 새 반례가 나오면 readiness를 낮출 수 있다

**강도:** MUST · **범용성:** CORE

새 반례가 현재 계약을 깨면 예외를 덧붙여 상태 표시를 지키려 하지 않는다. readiness를 필요한 수준으로 낮추고 정본 `owner`와 Probe를 보강한다.

**이유:** 상태 label보다 실제 반례를 우선하기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** readiness-review

## R-EV-008 — 우회 경로로 통과한 Probe는 PASS가 아니다

**강도:** MUST · **범용성:** CORE

test-only branch, raw state mutation, special host path, parallel owner처럼 검증 대상 불변 규칙을 우회해 fixture를 통과한 결과는 PASS로 인정하지 않는다.

**이유:** Probe가 실제 제품 경로를 검증하도록 하기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** probe-review

## R-EV-009 — 전수 검증기는 위반 전체를 보고해야 한다

**강도:** MUST · **범용성:** CONDITIONAL

전체 corpus의 closure를 주장하는 validator는 첫 오류에서 멈추는 spot check로 끝내지 않는다. 대상 전체의 위반 목록을 수집하고 위반이 0건일 때만 PASS한다.

**이유:** 하나를 고칠 때마다 다음 오류가 드러나는 반복을 줄이고, 전수 검증이라는 주장을 실제로 지키기 위해서다.

**적용 조건:** whole-corpus completeness/closure validator를 제공할 때

**검증:** validator-contract

## R-EV-010 — 생성한 인벤토리는 탐색 도구이지 정본이 아니다

**강도:** MUST · **범용성:** CONDITIONAL

source, manifest, schema에서 생성한 inventory는 탐색과 중복 방지에 사용하되 의미의 정본으로 승격하지 않는다.

**이유:** 생성된 index가 정본 문서나 코드와 경쟁하는 별도 권위가 되는 것을 막는다.

**적용 조건:** generated index/inventory를 제공할 때

**검증:** tooling-review

## R-EV-011 — 보안 주장은 실제 강제 수단으로 검증한다

**강도:** MUST · **범용성:** CONDITIONAL

sandbox, isolation, capability 같은 보안 주장은 정상 기능 테스트만으로 인정하지 않는다. 우회, 권한 확대, stale authority를 시도하는 adversarial fixture로 실제 enforcement를 검증한다.

**이유:** 이름뿐인 경계와 실제로 강제되는 경계를 구분하기 위해서다.

**적용 조건:** 보안/격리/capability 보장을 주장할 때

**검증:** security-probe

## R-EV-012 — 성능은 시간뿐 아니라 구조 지표도 본다

**강도:** SHOULD · **범용성:** CONDITIONAL

성능 요구는 wall-clock 수치만 보지 않는다. 가능한 범위에서 allocation 수, 복사한 byte 수, node 수, invalidation·reuse, queue depth처럼 구조를 보여 주는 지표도 기록한다.

**이유:** 환경 노이즈와 구조적 복잡성의 회귀를 구분하기 위해서다.

**적용 조건:** 성능이 architecture requirement인 경우

**검증:** benchmark/structural-metric

## R-EV-013 — 단계 완료는 구조물이 아니라 동작으로 증명한다

**강도:** MUST · **범용성:** CONDITIONAL

phase, stage, readiness의 완료 여부는 struct, module, document가 존재하는지로 판단하지 않는다. 그 단계가 약속한 계약과 필수 Probe 또는 증거가 실제로 통과했는지로 판단한다.

**이유:** placeholder 구조물의 존재를 진척으로 오인하면 실제 의미 완결성이 뒤로 밀린다.

**적용 조건:** phase/stage/readiness 기반 구현 계획을 사용하는 경우

**검증:** stage-gate/readiness-registry

## R-EV-014 — Probe harness는 작고 비권위적으로 유지한다

**강도:** MUST · **범용성:** CORE

reference probe 또는 conformance harness는 반례를 보이는 데 필요한 최소 구현으로 유지한다. 제품의 정본 경로를 대신하는 큰 대체 subsystem이나 별도 권위가 되지 않게 한다.

**이유:** 검증용 구현이 독립 제품 경로가 되면 실제 아키텍처가 아니라 테스트 전용 아키텍처를 검증하게 된다.

**적용 조건:** reference harness, probe runtime, conformance implementation을 만드는 경우

**검증:** probe-review

# 완료 기준

## R-COMP-001 — 동작한다는 사실만으로 완료라고 하지 않는다

**강도:** SHOULD · **범용성:** CORE

기능 완료는 하나의 happy path가 동작하는지만으로 판단하지 않는다. 프로젝트가 선언한 정확성, 결정성, 보안, 내구성, 접근성, 성능, 확장성 등 적용 가능한 품질 조건을 누적으로 만족하는지 확인한다.

**이유:** 기능이 존재한다는 사실과 제품 또는 시스템이 완료되었다는 주장을 구분하기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** completion-checklist

## R-COMP-002 — 알려진 아키텍처 위반을 임시 부채로 닫지 않는다

**강도:** MUST · **범용성:** CORE

완료 범위 안에 남아 있는 architecture 또는 spec 위반을 `임시`, `나중에 정리`라는 이유로 완료 처리하지 않는다. 범위 밖으로 남긴다면 책임자와 상태 문서에 명시한다.

**이유:** 숨은 부채를 완료 상태로 포장하지 않기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** completion-review

# Greenfield

## R-GREEN-001 — 출시 전 greenfield 코드에 가상의 과거를 보존하지 않는다

**강도:** MUST · **범용성:** CONDITIONAL

외부 사용자, 저장 데이터, 공개 API 같은 호환 의무가 아직 없는 greenfield 단계에서는 잘못된 내부 API를 보존하기 위한 legacy, migration, compatibility layer를 기본적으로 남기지 않는다.

**이유:** 존재하지 않는 과거와의 호환성을 위해 현재 설계를 왜곡하지 않기 위해서다.

**적용 조건:** pre-release greenfield이며 외부 compatibility/data obligation이 없을 때

**예외:** 이미 외부 사용자, 공개 API, 저장 데이터, 배포된 schema의 호환 의무가 있을 때

**검증:** review

