# 대표적인 안티패턴

자주 반복되는 구조적 실수를 빠르게 찾기 위한 관점입니다. 이름 자체를 금지하는 목록이 아니라, 아래 정본 규칙을 어기는 상황을 찾기 위한 보조 문서입니다.

> 이 문서는 정본 규칙의 읽기용 묶음입니다. 규칙 자체의 정본은 `rule-registry.json`입니다.

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

## R-OWN-009 — 우회하기 전에 확장 지점을 넓힌다

**강도:** MUST · **범용성:** CONDITIONAL

표준 확장 지점이 요구를 표현하지 못하면 기능 전용 우회 경로나 별도 경로를 만들기 전에 정본 확장 지점을 보강할 수 있는지 먼저 검토한다.

**이유:** 우회 경로가 일반 기능의 기본 수단이 되면 정본 책임자가 무력화되고 기능별 병렬 시스템이 생긴다.

**적용 조건:** 표준 framework/extension surface와 escape hatch가 함께 존재할 때

**검증:** review

## R-OWN-011 — 기능별 하위 시스템보다 조합 가능한 기본 요소를 우선한다

**강도:** SHOULD · **범용성:** CORE

서로 다른 기능군을 독립적인 전역 subsystem으로 하나씩 늘리기 전에 공통 의미 요소와 조합으로 표현할 수 있는지 확인한다. 새 기능이 기존 요소로 표현되지 않는다면 곧바로 새 subsystem을 만들기보다 정본 모델에 빠진 개념이 없는지 먼저 점검한다.

**이유:** 기능별 silo가 늘어날수록 식별자, 상태, 액션, 검색, 영속성 같은 공통 의미가 중복되고 상호 운용 비용이 커진다.

**적용 조건:** 여러 기능이 공통 domain/runtime 개념을 공유하는 제품이나 플랫폼

**예외:** 기능들이 실제로 독립된 배포·보안·수명·데이터 경계를 가져 분리된 subsystem이 정당한 경우

**검증:** architecture-review

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

## R-SEM-012 — 성능을 이유로 의미 경계를 우회하지 않는다

**강도:** MUST · **범용성:** CORE

성능 목표는 정본 경계 안에서 달성한다. hot path 최적화가 소유권, 권한, 커밋, 격리, 검증 경계를 건너뛰는 근거가 되어서는 안 된다.

**이유:** 빠른 우회 경로도 잘못된 경로라면 구조적 부채만 더 빠르게 쌓는다.

**적용 조건:** all non-trivial software projects

**검증:** review/performance-probe

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

## R-COM-003 — 주석에 불안정한 참조·변경 이력·코드 재서술을 남기지 않는다

**강도:** DEFAULT · **범용성:** PROFILE

코드 주석에는 절 번호 같은 위치 기반 참조, 변경 이력, 코드만 읽어도 알 수 있는 내용을 다시 풀어쓴 설명을 남기지 않는다.

**이유:** 쉽게 낡거나 중복되는 주석을 줄이기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** lint/review

## R-EV-004 — 중요 Probe에는 반례와 금지 상태를 함께 둔다

**강도:** MUST · **범용성:** CORE

중요한 불변 규칙을 검증하는 Probe는 정상 경로와 반례를 함께 둔다. precondition, stimulus·interleaving·crash point, expected state뿐 아니라 절대로 관측되면 안 되는 forbidden state도 정의한다.

**이유:** 무엇이 일어나야 하는지만 검사하면 잘못된 추가 상태를 놓칠 수 있다.

**적용 조건:** all non-trivial software projects

**검증:** probe-schema-lint

## R-EV-008 — 우회 경로로 통과한 Probe는 PASS가 아니다

**강도:** MUST · **범용성:** CORE

test-only branch, raw state mutation, special host path, parallel owner처럼 검증 대상 불변 규칙을 우회해 fixture를 통과한 결과는 PASS로 인정하지 않는다.

**이유:** Probe가 실제 제품 경로를 검증하도록 하기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** probe-review

## R-COMP-002 — 알려진 아키텍처 위반을 임시 부채로 닫지 않는다

**강도:** MUST · **범용성:** CORE

완료 범위 안에 남아 있는 architecture 또는 spec 위반을 `임시`, `나중에 정리`라는 이유로 완료 처리하지 않는다. 범위 밖으로 남긴다면 책임자와 상태 문서에 명시한다.

**이유:** 숨은 부채를 완료 상태로 포장하지 않기 위해서다.

**적용 조건:** all non-trivial software projects

**검증:** completion-review

## R-GREEN-001 — 출시 전 greenfield 코드에 가상의 과거를 보존하지 않는다

**강도:** MUST · **범용성:** CONDITIONAL

외부 사용자, 저장 데이터, 공개 API 같은 호환 의무가 아직 없는 greenfield 단계에서는 잘못된 내부 API를 보존하기 위한 legacy, migration, compatibility layer를 기본적으로 남기지 않는다.

**이유:** 존재하지 않는 과거와의 호환성을 위해 현재 설계를 왜곡하지 않기 위해서다.

**적용 조건:** pre-release greenfield이며 외부 compatibility/data obligation이 없을 때

**예외:** 이미 외부 사용자, 공개 API, 저장 데이터, 배포된 schema의 호환 의무가 있을 때

**검증:** review

