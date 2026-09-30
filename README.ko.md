# Architecture Governance

[English](README.md) · **한국어**

**Architecture Governance**는 비사소한 소프트웨어 아키텍처를 설계·검토·변경할 때 semantic ownership, contract 경계, 문서 권위, 검증 근거가 흐려지지 않도록 작업 방식을 규율하는 Claude Code 플러그인입니다.

아키텍처 작업을 추적 가능한 절차로 바꿉니다. semantic owner를 찾고, 설계 truth와 구현 truth를 분리하고, 병렬 시스템을 만들기 전에 기존 owner를 재사용·일반화하며, contract를 닫고, 숨은 ordering을 명시화하고, negative path를 검증하며, readiness와 완료 주장에는 evidence를 요구합니다.

## 설치

```bash
claude plugin marketplace add onetwohour/claude-plugins
claude plugin install architecture-governance@onetwohour
```

설치 후 새 Claude Code 세션을 시작합니다.

## 사용

별도 명령은 필요하지 않습니다. 평소처럼 설계나 구현 작업을 요청하면 됩니다.

```text
이 subsystem을 수정하기 전에 ownership, lifecycle, contract 결함을 검토해줘.
```

```text
이 설계 메모를 authoritative specification으로 정리하고 중요한 invariant의 Probe를 정의해줘.
```

```text
두 번째 manager/store/dispatcher/source of truth를 만들지 않는 방향으로 이 기능을 리팩터링해줘.
```

일반 작업에는 가볍게 적용되고, semantic ownership, persistence, concurrency, failure/retry, external effect, architecture change, specification authority, shared abstraction이 관련될수록 더 엄격하게 적용됩니다.

## 핵심 원칙

- 하나의 semantic responsibility에는 하나의 normative authority가 있습니다.
- Reuse Before Create. 새 indirection에는 입증 책임이 있습니다.
- 현재 코드는 구현의 증거이지 architecture authority 그 자체가 아닝니다.
- normative architecture, implementation status, roadmap, research를 분리합니다.
- semantic reference는 `§12` 같은 위치 번호가 아니라 문서 경로 + 안정적인 concept/rule identity를 사용합니다.
- correctness에 영향을 주는 dependency와 ordering을 registration order, container iteration, thread timing, callback order에 숨기지 않습니다.
- 중요한 contract는 적용 가능한 identity, ownership, state, lifecycle, authority, failure, retry, persistence, concurrency, observability를 닫습니다.
- 중요한 검증에는 negative path와 forbidden observable state가 포함됩니다.
- readiness와 완료는 evidence가 있는 주장이어야 합니다.

## 전체 Constitution

읽기용 전체 Constitution은 [doctrine/ENGINEERING_CONSTITUTION.md](doctrine/ENGINEERING_CONSTITUTION.md)에 있습니다. 스킬이 사용하는 machine-readable 정본 rule registry는 [`plugin/skills/architecture-governance/references/rule-registry.json`](plugin/skills/architecture-governance/references/rule-registry.json)입니다.

## 로컬 사용

```bash
git clone https://github.com/onetwohour/Architecture-Governance.git
claude --plugin-dir ./Architecture-Governance/plugin
```

`--plugin-dir`은 해당 세션에만 적용됩니다.

## 검증

```bash
python plugin/skills/architecture-governance/scripts/validate.py
python tests/validate_repository.py
```

## 라이선스

[Apache-2.0](LICENSE)
