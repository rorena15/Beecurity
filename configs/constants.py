# configs/constants.py
"""시뮬레이터 내 모든 수치 상수를 중앙 집중 관리합니다."""

BASE_TEMPERATURE = 25.0
MAX_HONEY_CAPACITY = 100.0
PHEROMONE_CHECK_INTERVAL = 10
MAX_AGE_DAYS = 45
QUEEN_DAILY_EGG_LIMIT = 2000
ENERGY_CONSUMPTION_RATE = 0.05
# 환경 퍼징 방어 임계치
MIN_SAFE_TEMP = -50.0
MAX_SAFE_TEMP = 100.0

# 훈증기(Smoker) 효과 수치
SMOKER_AGGRESSION_REDUCTION = 0.80  # 공격성 80% 감소
SMOKER_HONEY_CONSUMPTION_INC = 1.15 # 꿀 소비량 15% 증가
SMOKER_FORAGING_PENALTY = 0.90      # 채집 효율 10% 감소

# 내검(Inspection) 오버헤드
MAX_SAFE_INSPECTION_TIME = 15       # 15분 초과 시 스트레스
INSPECTION_STRESS_RATE = 2.0        # 분당 스트레스 증가량
MAX_AUDIT_CPU_LIMIT = 0.20          # 보안 감사 최대 자원 한도 (20%)

# 동봉산란 (Laying Worker) 및 페로몬 인증 상수
QUEEN_ABSENCE_LIMIT_DAYS = 14          # 동봉산란 트리거: 여왕 부재 지속 기간 (일)
PHEROMONE_AUTH_THRESHOLD = 20.0        # 페로몬 인증 최소 임계치

# 채밀 타격 (Harvesting Impact) 상수
SAFE_HARVEST_RATIO = 0.30              # 총 꿀 보유량 대비 안전 회수 비율 (30%)
STARVATION_RISK_MULTIPLIER = 1.5       # 기아 위험 증가 가중치
ROBBING_RISK_MULTIPLIER = 2.0          # 도봉(외부 침입) 위험 증가 가중치

# 방어 및 전투 인스턴스 상수
HEAT_BALLING_TEMP_THRESHOLD = 47.0    # 말벌을 무력화할 수 있는 열구 임계 온도
HEAT_BALLING_ENERGY_COST = 5.0        # 열구 형성 시 초당 에너지 소모 오버헤드
HORNET_DDOS_THRESHOLD = 50            # DDoS 탐지 임계치 (위협 객체 수)
MITE_APT_DAMAGE_RATE = 0.5            # 응애(APT)에 의한 틱당 체력 감소율