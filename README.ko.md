# Architecture Governance

[English](README.md) · **한국어**

소프트웨어 아키텍처와 명세를 설계·검토할 때 쓰는 Claude Code 스킬입니다. 의미의 정본 책임, 명시적인 계약과 순서, 검증 가능한 증거, 완료 기준을 중심으로 동작합니다.

## 설치

```bash
claude plugin marketplace add onetwohour/claude-plugins
claude plugin install architecture-governance@onetwohour
```

## 토큰 사용 방식

실행용 `SKILL.md`에는 핵심 작업 순서와 강한 기본 규칙만 둡니다. 세부 규칙은 작업에 필요한 묶음만 읽습니다.

- `system.md` — 소유권, 추상화, 런타임 의미, 상태, 영속성, 보안
- `decisions.md` — 애매한 요구와 제품 결정 판정
- `writing.md` — 명세, 주석, 용어, 의인화 금지
- `evidence.md` — Probe, readiness, 보안·성능 증거
- `delivery.md` — 변경 절차, 완료, greenfield 호환성

실행 문서에서는 `R-OWN-003` 대신 `O3` 같은 짧은 ID를 사용합니다. 기존 ID, 원본 출처, v1.1 전체 문구는 `aliases.json`과 `archive/v1.1/`에 그대로 보존하며 평상시에는 읽지 않습니다.

즉 토큰을 줄이기 위해 **내용을 삭제한 것이 아니라 기본 컨텍스트에서 분리**했습니다.

## 검증

```bash
python plugin/skills/architecture-governance/scripts/validate.py
python tests/validate_repository.py
```

## 전체 규약

[Engineering Constitution](doctrine/ENGINEERING_CONSTITUTION.md)

## 라이선스

[Apache-2.0](LICENSE)
