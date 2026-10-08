# Architecture Governance

[English](README.md) · **한국어**

**기존 아키텍처를 지키면서 코드를 변경하기 위한 Claude Code 플러그인입니다.**

Architecture Governance는 설계 조사부터 변경 계획, 구현, 리뷰, 검증까지 하나의 Skill로 연결합니다. 작업을 시작하기 전에 해당 동작의 책임이 어디에 있는지 확인하고, 변경 후에는 실제 코드와 검증 결과가 기존 계약을 만족하는지 검토하도록 돕습니다.

새로운 아키텍처를 강요하지 않습니다. 설계의 기준은 언제나 대상 프로젝트의 정본 문서와 계약입니다.

## 왜 필요한가요?

코드가 컴파일되고 테스트 몇 개를 통과해도 설계를 위반할 수 있습니다. 기존 상태 관리자를 우회하는 두 번째 저장소를 만들거나, 공개 계약을 건너뛰거나, 정의되지 않은 오류 처리 규칙을 임의로 추가하는 경우가 그렇습니다.

Architecture Governance는 이런 문제를 개발 과정에서 확인하도록 돕습니다.

- **기존 책임 확인:** 새 추상화를 만들기 전에 해당 동작을 소유하는 구성 요소와 계약을 찾습니다.
- **동작의 의미 분석:** 필요한 범위에서 상태, 식별자, 실행 순서, 실패·복구, 의존성 경계를 살펴봅니다.
- **변경 규모에 맞는 계획:** 단순 수정에는 가벼운 절차를, 공개 계약이나 핵심 설계 변경에는 더 엄격한 검토를 적용합니다.
- **변경 결과 검토:** 계획뿐 아니라 실제 Git diff와 실패·예외 경로를 확인합니다.
- **검증 근거 구분:** 명세의 존재, 구현, 테스트 실행, 실제로 입증한 범위를 혼동하지 않습니다.

## 설치

Claude Code에서 다음 명령을 실행합니다.

```bash
claude plugin marketplace add onetwohour/claude-plugins
claude plugin install architecture-governance@onetwohour
```

설치 후 Claude Code 세션을 새로 시작합니다.

## 시작하기

작업 내용을 Skill에 전달합니다.

```text
/architecture-governance:architecture-governance plan 저장 실패 후 복구 동작 설계
```

기존 설계를 확인하면서 구현하려면:

```text
/architecture-governance:architecture-governance implement 에디터 재구성 후 오래된 응답 처리 수정
```

설계와 변경 내역을 검토하려면:

```text
/architecture-governance:architecture-governance audit 설계 문서와 실제 구현의 위반 사항 조사
/architecture-governance:architecture-governance review 현재 Git diff 검토
```

관련 작업에서 Skill이 자동 선택될 수도 있습니다. 특정 절차를 요청할 때는 명시적으로 호출하면 됩니다.

## 지원하는 작업

| 모드 | 수행하는 작업 |
| --- | --- |
| `plan` | 책임 주체와 계약을 찾고 변경 범위, 대안, 영향, 검증 계획을 정리합니다. |
| `implement` | 기존 설계를 조사한 뒤 구현하고 실제 변경 내용과 관련 검증을 확인합니다. |
| `audit` | 구현의 설계 위반뿐 아니라 정본 문서 간 모순도 조사합니다. |
| `review` | 변경하려는 내용 또는 Git diff를 기존 설계 계약과 비교합니다. |
| `verify` | 적용 가능한 검사를 실행하고 확인된 결과와 남은 공백을 구분합니다. |
| `project` | 기존 정본을 바탕으로 프로젝트 상태와 미완료 작업의 파생 뷰를 구성합니다. |
| `adopt` | 기존 프로젝트의 규칙, 테스트, CI에 이 작업 방식을 도입하도록 돕습니다. |

모두 **하나의 Skill**에서 제공됩니다. 모드를 지정하지 않으면 기본적으로 `plan`을 사용하되, 요청의 목적이 명확하면 그에 맞는 작업을 선택합니다.

## 보장하지 않는 것

Architecture Governance는 Claude의 개발 작업을 안내하는 도구입니다. 프로젝트 고유의 아키텍처 검사기, 테스트, 보안 강제 장치나 CI를 대체하지 않습니다. Skill이 모든 변경에서 반드시 호출되는 것도 아니며, 문서 검토만으로 모든 설계 불변식을 입증할 수도 없습니다.

테스트 파일을 발견하거나 명령 실행에 성공한 사실과 해당 계약의 정확성이 검증된 사실은 다릅니다. 검증하지 못한 부분은 완료로 간주하지 않고 명시적으로 남겨야 합니다.

실제로 변경을 차단해야 하는 규칙은 **대상 프로젝트의 CI와 검증 도구**에서 강제해야 합니다.

## 문서

- [선택형 도구와 고급 사용법](docs/TOOLS.md)
- [엔지니어링 원칙](doctrine/ENGINEERING_CONSTITUTION.md)
- [기여 및 개발 안내](CONTRIBUTING.md)

## 라이선스

[Apache-2.0](LICENSE)
