# main.py
import time
from core.engine import SwarmEngine
from entities.queen import QueenBee
from entities.worker import WorkerBee

def main():
    print("🐝 하이브 마인드 엔진(Hive Mind Engine) 초기화 중...")
    
    # 1. 엔진 코어 생성 (최대 에이전트 100마리 수용 가능한 벡터 공간)
    engine = SwarmEngine(agent_count=100)
    
    # 2. 중앙 정책 서버(여왕벌 마스터 노드) 등록
    queen = QueenBee()
    engine.register_queen(queen)
    
    # 3. 초기 워커 노드(일벌) 생성 및 네트워크 등록
    for _ in range(50):
        worker = WorkerBee()
        # 테스트를 위해 일부 워커의 나이를 조작하여 외부망(Forager) 권한을 부여합니다.
        worker.age_days = 25 
        engine.agents.append(worker)
        
    print("✅ 초기화 완료. 시뮬레이션 메인 루프를 가동합니다!\n")
    time.sleep(1)
    
    # 4. 시뮬레이션 루프 실행 (예: 200 틱 동안 가동)
    for tick in range(1, 201):
        
        # 테스트용 시나리오: 50틱 쯤에 말벌(DDoS) 위협 강제 발생
        if tick == 50:
            print("\n🚨 [SYSTEM EVENT] 외부 위협 탐지: 말벌(Hornet DDoS) 트래픽 발생!")
            engine.threat_manager.trigger_hornet_attack(hornet_signature="APT_HORNET_001", intensity=10)
            
        # 가상의 꿀 수집 (테스트용 자원 증가)
        engine.total_honey_stock += 0.5
        
        # 엔진 상태 업데이트 (이 안에서 자동으로 Dashboard 렌더링이 호출됨)
        engine.run_tick()
        
        # 터미널에서 진행 상황을 볼 수 있도록 약간의 딜레이
        time.sleep(0.1)
        
    print("\n🏁 시뮬레이션이 안전하게 종료되었습니다. (Audit Log를 확인하세요)")

if __name__ == "__main__":
    main()