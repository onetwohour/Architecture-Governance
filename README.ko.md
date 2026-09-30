# Architecture Governance

[English](README.md) · **한국어**

**Architecture Governance**는 규모가 있는 소프트웨어 설계와 명세를 만들고 검토할 때 쓰는 Claude Code 플러그인입니다.

핵심 목표는 단순합니다. 의미를 누가 정의하는지 분명히 하고, 계약의 빈칸을 닫고, 구현 현황과 설계 규범을 섞지 않으며, 중요한 불변 규칙을 실제 검증과 연결합니다. 기능을 추가할 때마다 새로운 Manager·Store·Dispatcher 같은 병렬 구조가 생기는 것도 경계합니다.

## 설치

```bash
claude plugin marketplace add onetwohour/claude-plugins
claude plugin install architecture-governance@onetwohour
```

설치한 뒤에는 새 Claude Code 세션을 시작합니다.

## 사용법

별도 명령은 필요하지 않습니다. 평소처럼 설계나 구현 작업을 요청하면 됩니다.

```text
이 서브시스템을 수정하기 전에 책임 경계, 수명주기, 계약 결함부터 검토해 줘.
```

```text
이 설계 메모를 정본 명세로 정리하고, 중요한 불변 규칙에는 Probe를 정의해 줘.
```

```text
두 번째 Manager나 Store를 만들지 않는 방향으로 이 기능을 리팩터링해 줘.
```

사소한 코드 수정에는 과도한 절차를 요구하지 않습니다. 대신 소유권, 영속성, 동시성, 실패·재시도, 외부 부수 효과, 아키텍처 변경, 명세 권위, 공통 추상화가 걸린 작업에서는 더 엄격하게 적용됩니다.

## 핵심 원칙

- 하나의 의미에는 하나의 규범적 정본 책임자가 있습니다.
- 새 구조를 만들기 전에 기존 책임자를 찾습니다.
- 현재 코드가 존재한다는 사실만으로 그 코드가 아키텍처의 정본이 되지는 않습니다.
- 규범 문서, 구현 현황, 계획, 조사 기록은 역할을 분리합니다.
- 문서의 의미 참조에는 절 번호가 아니라 경로와 안정적인 개념명 또는 규칙 ID를 사용합니다.
- 정확성에 영향을 주는 의존성과 순서는 등록 순서나 스레드 타이밍 같은 우연에 맡기지 않습니다.
- 중요한 계약은 식별자, 상태, 권한, 실패, 재시도, 영속성, 동시성 등 필요한 의미를 빠뜨리지 않습니다.
- 중요한 검증에는 정상 경로뿐 아니라 반례와 금지 상태가 포함됩니다.
- readiness와 완료는 문서의 존재가 아니라 실제 증거로 주장합니다.
- 시스템이나 코드에 모델로 정의되지 않은 의도·지식·감정을 부여하지 않습니다.
- 한국어 문서는 불필요한 영어 명사 나열과 직역투를 피하고 자연스러운 한국어 문장으로 씁니다.

## 전체 규약

읽기용 전체 규약은 [doctrine/ENGINEERING_CONSTITUTION.md](doctrine/ENGINEERING_CONSTITUTION.md)에 있습니다. 기계가 읽는 규칙의 정본은 [`plugin/skills/architecture-governance/references/rule-registry.json`](plugin/skills/architecture-governance/references/rule-registry.json)입니다.

문서와 주석의 어투 기준은 [편집·문체 정책](plugin/skills/architecture-governance/references/editorial-policy.md)에 따로 모아 두었습니다.

## 저장소에서 바로 실행

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
