# Architecture Governance

[English](README.md) · **한국어**

프로젝트의 기존 설계를 보존하면서 코드를 변경하기 위한 **Claude Code 통합 스킬**입니다. 설계 분석, 구현, 아키텍처 감사, 변경 리뷰, 실제 검증을 하나의 스킬에서 처리합니다.

범용 아키텍처 프레임워크를 강요하지 않습니다. 프로젝트의 정본 문서와 계약을 먼저 확인하고, 이미 존재하는 책임을 중복하지 않도록 변경을 검토하며, 테스트 실행 결과와 실제로 증명된 범위를 구별합니다.

## 설치

```bash
claude plugin marketplace add onetwohour/claude-plugins
claude plugin install architecture-governance@onetwohour
```

설치 후 Claude Code 세션을 새로 시작하세요. 배포는 기존 플러그인 마켓플레이스를 통해 이루어지며, 이 저장소의 `plugin/` 디렉터리가 소스입니다.

## 사용법

`/architecture-governance:architecture-governance` 뒤에 모드와 작업을 입력합니다. 하나의 스킬에서 다음 작업을 지원합니다.

| 모드 | 역할 |
| --- | --- |
| `plan` | 정본·의존성·기존 추상화 조사, 변경 범위와 검증 계획 |
| `implement` | 계획에 따른 구현, 실제 diff 감사, 검증 |
| `audit` | 코드뿐 아니라 **설계 문서 자체의 자기모순**까지 감사 |
| `review` | Git 변경 내용과 아키텍처 계약 비교 |
| `verify` | 실제 테스트 실행과 증거·한계 확인 |
| `adopt` | 프로젝트의 기존 CI·규칙·검증 도구와 통합 |

예시:

```text
/architecture-governance:architecture-governance implement 에디터 재구성 이후 대기 요청 고착 문제 수정
/architecture-governance:architecture-governance audit 설계 문서와 구현의 위반 사항 조사
/architecture-governance:architecture-governance verify persistence 관련 Probe
```

모드를 생략하면 기본적으로 `plan`을 사용하되, 요청 의도가 명백히 다른 경우 해당 작업에 맞춥니다.

## 설계 원칙

1. **정본 우선:** 구현 코드, STATUS/TODO, 스킬 자체가 설계의 최종 권위가 되지 않습니다.
2. **기존 소유자 재사용:** 새로운 Manager·Store·Registry를 추가하기 전에 현재 책임과 확장 지점을 조사합니다.
3. **위험도에 비례한 절차:** 단순 수정은 가볍게, 공개 계약이나 영속 상태·보안 경계 변경은 엄격하게 다룹니다.
4. **반례 중심 검증:** 정상 동작뿐 아니라 실패, 취소, 재시도, 재구성, 오래된 응답 및 금지 상태를 검토합니다.
5. **실제 변경 감사:** 계획한 파일과 Git diff의 차이를 확인합니다.
6. **증거 없는 완료 금지:** 구현 파일 존재, 테스트 등록, 실행 성공, 아키텍처 적합성을 서로 다른 주장으로 취급합니다.

기존 101개 세부 규칙을 즉시 폐기하지 않고, 5개 참조 파일로 유지했습니다. 새로 추가한 5개 워크플로가 이 규칙들을 **언제 어떻게 적용할지** 안내합니다.

## 선택형 검사 도구

Python 3.10 이상과 Git이 필요합니다. 외부 Python 패키지는 필요하지 않습니다. 도구는 자동으로 실행되지 않으며 파일을 수정하지 않습니다.

**변경 범위 비교:**

```bash
python plugin/skills/architecture-governance/scripts/change_scope.py \
  --repo /path/to/project --plan /tmp/change-scope.json
```

계획 JSON의 `allowed_paths`에 들어 있지 않은 파일이 변경되면 검토 대상으로 표시합니다. `protected_paths`에 포함된 파일 변경은 실패로 처리합니다. Staged·unstaged·untracked 파일을 함께 검사합니다. 단, 파일 경로 검사만으로 의미적 설계 위반을 판정할 수는 없습니다.

**실제 실행 증거 기록:**

```bash
python plugin/skills/architecture-governance/scripts/run_validation.py \
  --repo /path/to/project --label test --output /tmp/test-evidence.json \
  -- python -m unittest discover -s tests
```

명령을 셸 없이 실행하고 결과·Git revision·플랫폼·작업 트리 상태를 JSON으로 기록합니다. 테스트가 성공해도 해당 테스트의 주장만 검증되며, 자동으로 전체 설계 적합성이 보장되지는 않습니다. 더티 작업 트리에서 생성된 결과는 깨끗한 커밋의 재사용 가능한 검증서가 아닙니다.

## CI와 Skill의 책임

이 스킬은 설계를 **조사하고, 변경을 검토하고, 검증 범위를 설명하는 절차**입니다. 자동으로 불리지 않을 수 있으므로 스킬의 지시문만으로 변경 금지를 강제할 수 없습니다.

프로젝트의 실제 아키텍처 Gate, Conformance Test, Probe를 프로젝트 CI와 브랜치 보호 규칙에 연결해야 합니다. 스킬 안에 프로젝트의 정본이나 검증 결과를 복제해서는 안 됩니다.

[프로젝트 도입 절차](plugin/skills/architecture-governance/workflows/adopt.md) · [Engineering Constitution](doctrine/ENGINEERING_CONSTITUTION.md)

## 저장소 검증

```bash
python plugin/skills/architecture-governance/scripts/validate.py
python tests/validate_repository.py
python -m unittest discover -s tests -p 'test_*.py' -v
```

이는 플러그인 파일·규칙·도구 동작 검증입니다. 특정 프로젝트의 설계가 올바르다는 증거로 사용해서는 안 됩니다.

## 라이선스

[Apache-2.0](LICENSE)
