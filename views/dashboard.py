# views/dashboard.py
from typing import Dict, Any

class CLIDashboard:
    """
    (View Layer) 시뮬레이션 상태를 터미널에 시각화하는 읽기 전용 대시보드입니다.
    어떠한 경우에도 엔진의 내부 데이터를 직접 수정할 수 없습니다.
    """
    @staticmethod
    def render(tick: int, swarm_data: Dict[str, Any], threat_data: Dict[str, Any]) -> None:
        print("\n" + "="*50)
        print(f"🐝 [Hive Mind Engine Status] - Tick: {tick:06d}")
        print("="*50)
        
        # 1. 분산 리더십 및 군집 상태
        queen_status = swarm_data.get('queen_status', 'UNKNOWN')
        print(f"[+] Policy Server (Queen) Status : {queen_status}")
        print(f"[+] Active Agents (Workers)    : {swarm_data.get('active_agents', 0)} nodes")
        
        # 2. 자원 및 가용성 지표
        honey = swarm_data.get('total_honey', 0.0)
        stress = swarm_data.get('colony_stress', 0.0)
        print(f"[+] System Resource (Honey)    : {honey:.2f} units")
        print(f"[+] Audit Overhead (Stress)    : {stress:.2f}%")
        
        # 3. 침입 탐지 시스템 (IDS) 상태
        active_threats = threat_data.get('active_alerts', 0)
        if active_threats > 0:
            print(f"⚠️  [CRITICAL] Active Threats Detected: {active_threats}")
            print(f"🛡️  Defense Protocol: Heat-balling Instance ACTIVE")
        else:
            print(f"[+] Network Security           : SECURE")
            
        print("="*50 + "\n")