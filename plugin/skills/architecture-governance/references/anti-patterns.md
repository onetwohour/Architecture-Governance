# Anti-patterns

> 이 문서는 canonical 규칙의 위반 형태를 빠르게 찾기 위한 projection입니다. 새 규칙을 정의하지 않습니다.

- **Parallel owner:** 같은 semantic responsibility를 Manager/Store/Dispatcher/Resolver 등으로 두 번 소유한다. → `R-OWN-001`, `R-OWN-004`
- **Feature-local subsystem:** 기존 canonical primitive로 표현 가능한 기능 아래에 작은 framework를 새로 만든다. → `R-OWN-003`, `R-OWN-011`
- **Escape hatch before extension:** 표준 extension surface가 좁다는 이유로 raw Core/Platform access나 bypass를 만든다. → `R-OWN-009`
- **Hidden semantic ordering:** registration/source/container/thread timing이 결과를 결정한다. → `R-SEM-001`
- **Declared/runtime drift:** 선언한 dependency/access와 실제 runtime access가 다르다. → `R-SEM-002`
- **Truth duplication:** authoritative state를 하나 더 저장하고 synchronization을 correctness 전제로 만든다. → `R-SEM-003`
- **Section-number citation:** `§12`, `3장 2절` 등을 semantic reference로 사용한다. → `R-DOC-001`
- **Status in spec / roadmap as capability:** 현재 구현 사실과 normative truth를 섞는다. → `R-DOC-002`, `R-DOC-009`
- **Comment as archive:** 설계 의미, 결정 이력, 상태, 변경 이력을 코드 주석에 보관한다. → `R-COM-001`, `R-COM-003`
- **Happy-path-only validation:** 해야 할 일만 검사하고 forbidden state를 정의하지 않는다. → `R-EV-004`
- **Probe bypass:** test-only branch나 parallel mutation path로 probe를 통과시킨다. → `R-EV-008`
- **Structure-as-readiness:** type/module/document가 존재한다는 이유로 stage/readiness를 완료 처리한다. → `R-EV-006`, `R-EV-013`
- **Performance excuse:** 빠르다는 이유로 ownership/commit/ingress law를 우회한다. → `R-SEM-012`
- **Temporary architecture debt closure:** 알려진 architecture violation을 “나중에 정리”로 닫는다. → `R-COMP-002`
- **Speculative compatibility in greenfield:** 외부 호환 의무가 없는 미출시 시스템에 legacy/migration layer를 남긴다. → `R-GREEN-001`
