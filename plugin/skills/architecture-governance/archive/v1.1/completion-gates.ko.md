# 완료 기준

기능이 단순히 동작하는 것과, 설계·검증까지 포함해 완료되었다고 말할 수 있는 상태를 구분합니다.

> 이 문서는 정본 규칙의 읽기용 묶음입니다. 규칙 자체의 정본은 `rule-registry.json`입니다.

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

## R-EV-004 — 중요 Probe에는 반례와 금지 상태를 함께 둔다

**강도:** MUST · **범용성:** CORE

중요한 불변 규칙을 검증하는 Probe는 정상 경로와 반례를 함께 둔다. precondition, stimulus·interleaving·crash point, expected state뿐 아니라 절대로 관측되면 안 되는 forbidden state도 정의한다.

**이유:** 무엇이 일어나야 하는지만 검사하면 잘못된 추가 상태를 놓칠 수 있다.

**적용 조건:** all non-trivial software projects

**검증:** probe-schema-lint

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

