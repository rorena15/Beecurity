# entities/worker.py
from entities.base_bee import BaseBee
from entities.components import ForagingComponent, LayingWorkerComponent,CombatComponent
from configs.constants import PHEROMONE_AUTH_THRESHOLD
class WorkerBee(BaseBee):
    def __init__(self):
        super().__init__()
        self.role: str = "CLEANER"
        self._network_access: str = "INTERNAL_ONLY"
        self.local_pheromone_level: float = 100.0  # 캐싱된 로컬 보안 토큰
        
    def update(self, tick: int) -> None:
        super().update(tick)
        self._verify_pheromone_auth()
        
        # 권한 드리프트 상태일 경우 산란 로직 실행
        if self._state == "LAYING_WORKER" and "laying_worker" in self.components:
            self.components["laying_worker"].produce_dummy_node()

    def _verify_pheromone_auth(self) -> None:
        """
        페로몬 농도가 임계치(Threshold) 이하로 떨어지면 에이전트들은 
        '동봉산란' 모드로 진입하며 로컬 정책을 임의 변경합니다.
        """
        if self.local_pheromone_level < PHEROMONE_AUTH_THRESHOLD:
            if self._state != "LAYING_WORKER":
                self.change_state("LAYING_WORKER")
                self.role = "LAYING_WORKER"
                # 권한 우회 컴포넌트 강제 주입
                if "laying_worker" not in self.components:
                    self.add_component("laying_worker", LayingWorkerComponent())

    def _execute_role_action(self) -> None:
        if self._network_access == "EXTERNAL_ACCESS" and self.role == "FORAGER":
            # 외부 환경 자원 탐색 및 수집 로직
            pass
        elif self.role == "NURSE" or self.role == "BUILDER":
            # 내부망 자원 가공 및 육아 로직 실행
            pass
        
    def receive_intrusion_alert(self, threat_type: str, signature: str) -> None:
        """
        외부 공격 감지 시, 에이전트의 상태를 즉시 방어 모드로 강제 전환합니다.
        """
        if threat_type == "HORNET_DDOS":
            # 외부 공격 감지 시, 모든 외역봉은 즉시 복귀하여 입구(Gateway) 방어 모드로 전환 
            if self.role in ["FORAGER", "SCOUT"]:
                self.change_state("DEFENSE_RETURN")
            
            # 방어 역할을 수행하기 위해 전투 컴포넌트를 동적으로 주입
            if "combat" not in self.components:
                self.add_component("combat", CombatComponent())
            
            self.role = "GUARD" # 현재 역할을 문지기벌로 변경 [cite: 137]
            self._update_blacklist(signature)

    def _update_blacklist(self, signature: str) -> None:
        """공격 시그니처가 확인된 소스를 전체 노드가 공유받아 로컬 블랙리스트에 업데이트합니다."""
        if not hasattr(self, "threat_blacklist"):
            self.threat_blacklist = set()
        self.threat_blacklist.add(signature)