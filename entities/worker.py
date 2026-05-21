# entities/worker.py
from entities.base_bee import BaseBee
from entities.components import ForagingComponent, LayingWorkerComponent
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