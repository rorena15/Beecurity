# entities/worker.py
from entities.base_bee import BaseBee
from entities.components import ForagingComponent
from typing import Optional

class WorkerBee(BaseBee):
    """
    일벌 에이전트. 연령(Age)에 따른 동적 권한 할당(Temporal RBAC)을 수행합니다.
    """
    def __init__(self):
        super().__init__()
        # 기획서 Data Dictionary 기준 속성 정의
        self.role: str = "CLEANER"
        self.experience: int = 0
        self.sting_status: bool = False
        self._network_access: str = "INTERNAL_ONLY"  # 보안 접근 권한 캡슐화
        
    def update(self, tick: int) -> None:
        """엔진 틱에 동기화되어 에이전트 상태를 갱신합니다."""
        super().update(tick)
        
        # 1. 연령 기반 보안 정책 (Temporal RBAC) 평가
        self._evaluate_rbac_policy()
        
        # 2. 역할에 따른 행동 수행
        self._execute_role_action()

    def _evaluate_rbac_policy(self) -> None:
        """
        생물학적 연령별 분업을 Role-Based Access Control로 매핑합니다.
        검증되지 않은 신규 에이전트의 외부 통신은 즉시 차단됩니다.
        """
        if self.age_days < 20:
            # 20일 이전: 내부 리소스 접근 및 클리닝 권한만 부여 (Read-Only/Internal)
            self._network_access = "INTERNAL_ONLY"
            
            if self.age_days < 10:
                if self._state != "NURSE":
                    self.change_state("NURSE")
                    self.role = "NURSE"
            else:
                if self._state != "BUILDER":
                    self.change_state("BUILDER")
                    self.role = "BUILDER"
        else:
            # 20일 이후: 외부 네트워크 인터페이스 활성화 및 데이터 수집 권한 부여 (Read-Write/External)
            self._network_access = "EXTERNAL_ACCESS"
            if self._state != "FORAGER":
                self.change_state("FORAGER")
                self.role = "FORAGER"
                # 컴포넌트 기반 아키텍처: 외부 권한 획득 시에만 채집 모듈 주입
                if "foraging" not in self.components:
                    self.add_component("foraging", ForagingComponent())

    def _execute_role_action(self) -> None:
        if self._network_access == "EXTERNAL_ACCESS" and self.role == "FORAGER":
            # 외부 환경 자원 탐색 및 수집 로직
            pass
        elif self.role == "NURSE" or self.role == "BUILDER":
            # 내부망 자원 가공 및 육아 로직 실행
            pass