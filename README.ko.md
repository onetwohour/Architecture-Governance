# Architecture Governance

[English](README.md) · **한국어**

소프트웨어 아키텍처와 명세를 설계·검토할 때 쓰는 Claude Code 스킬입니다. 의미의 정본 책임, 명시적인 계약과 순서, 검증 가능한 증거, 완료 기준을 중심으로 동작합니다.

## 설치

```bash
claude plugin marketplace add onetwohour/claude-plugins
claude plugin install architecture-governance@onetwohour
```

## 토큰 사용 방식

실행용 `SKILL.md`에는 기본 작업 순서와 강한 불변식만 둡니다. 세부 규칙은 작업에 필요한 묶음만 읽습니다.

- `system.md` — 소유권, 추상화, 런타임 의미, 상태, 영속성, 보안
- `decisions.md` — 애매한 요구와 제품 결정 판정
- `writing.md` — 명세, 주석, 용어
- `evidence.md` — Probe, readiness, 보안·성능 증거
- `delivery.md` — 변경 절차, 완료, greenfield 호환성

위 다섯 reference 파일이 현재 정책의 전부입니다.

## 검증

```bash
python plugin/skills/architecture-governance/scripts/validate.py
python tests/validate_repository.py
```

## 정책 인덱스

[Engineering Constitution](doctrine/ENGINEERING_CONSTITUTION.md)

## 라이선스

[Apache-2.0](LICENSE)
