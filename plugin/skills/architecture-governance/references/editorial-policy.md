# 편집·문체 정책

문서와 코드 주석을 어떻게 쓰고 참조할지 정합니다. 안정적인 참조, 문서 역할 분리, 의인화 금지, 자연스러운 기술 문장, 주석의 책임 범위를 다룹니다.

> 이 문서는 정본 규칙의 읽기용 묶음입니다. 규칙 자체의 정본은 `rule-registry.json`입니다.

## 문체 예시

### 의인화하지 않는다

좋지 않은 표현:

- 캐시가 값이 오래되었다는 것을 안다.
- 런타임이 세션을 복구하고 싶어 한다.
- 문서가 어떤 backend를 쓸지 결정한다.
- 시스템이 이전 owner를 기억한다.

더 정확한 표현:

- 캐시 항목의 revision이 현재 revision보다 작으면 stale로 판정한다.
- 복구 정책은 재시작 뒤 세션을 다시 구성한다.
- backend 선택은 `BackendSelectionPolicy`를 따른다.
- 저장된 `owner_id`가 이전 owner를 식별한다.

다만 `parser가 잘못된 token을 거부한다`, `scheduler가 다음 runnable task를 선택한다`처럼 실제 계약에 정의된 동작을 능동형으로 쓰는 것은 의인화가 아니다.

### 번역투를 줄인다

좋지 않은 표현:

- canonical owner가 semantic responsibility를 소유한다.
- contract closure를 수행한 뒤 implementation을 진행한다.
- consumer마다 다른 shape를 invent하지 않게 한다.

더 자연스러운 표현:

- 같은 의미의 정본은 한 owner가 맡는다.
- 계약의 빈칸을 먼저 정리한 뒤 구현한다.
- 소비자가 서로 다른 구조를 임의로 만들지 않게 한다.

표준 기술 용어가 더 정확하다면 억지로 번역하지 않는다. 다만 한국어 문장 안에서 영어 명사를 불필요하게 이어 붙이거나 영어 관용구를 직역하지 않는다.

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

