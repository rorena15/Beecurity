# 디렉토리 구조
---
hive_mind_engine/ [cite: 22]
│
├── configs/ [cite: 22]
│   ├── constants.py            # 모든 수치(온도, 확률 등) 상수 중앙 관리 [cite: 22, 91]
│   └── config.py               # 환경 및 디버그 설정, 동적 환경 변수 토글 [cite: 28, 40, 92]
│
├── core/ [cite: 22]
│   ├── engine.py               # 시뮬레이션 메인 루프 (NumPy 벡터화 엔진) [cite: 22, 97]
│   ├── environment.py          # 온습도 및 외부 환경 
│   └── security_interfaces.py  # IDataIntegrity, IHeartbeat 등 보안 인터페이스 [cite: 30, 43, 93]
│
├── entities/ 
│   ├── base_bee.py             # 최상위 벌 클래스 (상태 전이 및 FSM 뼈대) [cite: 23, 95]
│   ├── components.py           # 조립식 아키텍처를 위한 Health, Foraging 등 컴포넌트 [cite: 31, 46, 94]
│   ├── queen.py                # 분산 리더 노드 및 중앙 정책 서버 [cite: 23, 96]
│   ├── worker.py               # 일벌 에이전트 
│   └── larvae.py               # 육아 및 애벌레 객체 
│
├── spaces/ 
│   ├── grid.py                 # 벌집 그리드(육각형) 로직 
│   └── cells.py                # 일벌방, 수컷방, 왕대 등 공간 모델링 
│
├── managers/ 
│   ├── beekeeper.py            # 관리자 개입 액션 (내검, 사양, 훈증 등) 
│   └── policy_manager.py       # 보안 및 운영 정책 제어 엔진 
│
├── utils/ 
│   └── logger.py               # 데이터 수집 및 보안 감사(Audit) 로그 
│
└── scripts/
    └── generate_entity.py      # 보일러플레이트 자동 생성을 위한 스캐폴딩 스크립트 [cite: 39, 159]
---