# managers/threat_manager.py
from typing import List

class ThreatManager:
    """외부 위협(Hornet-DDoS, Mite-APT)의 발생과 침입 탐지를 통제하는 보안 매니저입니다."""
    def __init__(self):
        self.active_threats: List[dict] = []
        self.global_blacklist: set = set()

    def trigger_hornet_attack(self, hornet_signature: str, intensity: int) -> dict:
        """말벌 침입(DDoS) 트래픽을 발생시킵니다."""
        threat_data = {
            "type": "HORNET_DDOS",
            "signature": hornet_signature,
            "intensity": intensity,
            "status": "ACTIVE"
        }
        self.active_threats.append(threat_data)
        
        # 공격 시그니처가 확인된 소스에 대해서 블랙리스트 등재 
        self.global_blacklist.add(hornet_signature)
        return threat_data

    def get_active_alerts(self) -> List[dict]:
        return self.active_threats