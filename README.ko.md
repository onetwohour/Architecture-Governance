# Architecture Governance

[English](README.md) · **한국어**

아키텍처 문제는 보통 클래스나 함수가 하나 부족해서 생기지 않습니다. 누가 어떤 의미를 책임지는지 불분명하거나, 같은 사실을 여러 곳에서 결정하거나, 순서가 암묵적으로 정해지거나, 실패와 재시도 의미가 닫혀 있지 않거나, 아직 필요하지도 않은 추상화를 먼저 만드는 데서 문제가 생깁니다.

Architecture Governance는 이런 문제를 임시 우회책으로 덮지 않고 설계 자체에서 찾아내기 위한 Claude Code 스킬입니다.

새 서브시스템을 설계할 때, 명세를 정리할 때, 큰 리팩터링을 준비할 때, 영속성·동시성·플러그인 경계를 정의할 때, 혹은 지금 보고 있는 문제가 구현 결함인지 아키텍처 결함인지 판단해야 할 때 사용할 수 있습니다.

## 설치

```bash
claude plugin marketplace add onetwohour/claude-plugins
claude plugin install architecture-governance@onetwohour
```

설치 후 새 Claude Code 세션을 시작하면 됩니다.

## 무엇을 확인하나

이 스킬은 아키텍처 작업에서 다음과 같은 질문을 끝까지 확인하도록 합니다.

- 이 의미를 최종적으로 책임지는 곳은 어디인가?
- 같은 사실을 둘 이상의 위치에서 저장하거나 결정하고 있지는 않은가?
- 의존성과 순서가 명시되어 있는가, 아니면 등록 순서·컨테이너 순서·콜백 타이밍·스레드 타이밍에 새고 있는가?
- 동일성, 동등성, 권한, 상태 전이, 실패, 재시도, 영속성, 재구성의 의미가 실제로 정의되어 있는가?
- 새 추상화가 정말 필요한 근거가 있는가, 아니면 계층만 하나 더 늘어난 것인가?
- 중요한 보장을 실패 사례나 Probe로 반증해 볼 수 있는가?
- 구현이 잘못된 책임 경계를 고치는 대신 우회하고 있지는 않은가?

특정 아키텍처 스타일을 강요하는 것이 목적은 아닙니다. 프로젝트가 이미 가진 도메인 모델을 기준으로, 그 안의 규칙을 더 명시적이고 작고 검증 가능하게 만드는 것이 목적입니다.

## 구성

`SKILL.md`에는 기본 작업 순서와 가장 강한 원칙만 들어 있습니다. 세부 규칙은 성격에 따라 나뉘어 있고 필요한 경우에만 읽습니다.

- `system.md` — 소유권, 추상화, 런타임 의미, 상태, 영속성, 보안
- `decisions.md` — 애매한 요구와 엔지니어링/제품 결정 구분
- `writing.md` — 명세, 용어, 주석, 규범 문장
- `evidence.md` — Probe, readiness, 동시성, 보안, 성능 증거
- `delivery.md` — 변경 절차, 완료 기준, greenfield 호환성

위 다섯 reference 파일이 현재 정책입니다.

## 검증

```bash
python plugin/skills/architecture-governance/scripts/validate.py
python tests/validate_repository.py
```

validator는 저장소 구조와 현재 규칙 집합의 일관성을 검사합니다. 통과했다고 해서 특정 설계의 의미적 정당성까지 자동으로 증명되는 것은 아닙니다.

## 정책 인덱스

[Engineering Constitution](doctrine/ENGINEERING_CONSTITUTION.md)

## 라이선스

[Apache-2.0](LICENSE)
