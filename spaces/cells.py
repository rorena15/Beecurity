# spaces/cells.py
from typing import Any, Optional

class BaseCell:
    """벌집을 구성하는 기본 육각형 셀 구조입니다."""
    def __init__(self, x: int, y: int, z: int):
        self.coordinate = (x, y, z)
        self.type: str = "BASE"
        self.content: Optional[Any] = None
        self.is_capped: bool = False
        self.can_store_resource: bool = True
        
    def store_resource(self, resource_amount: float) -> bool:
        if not self.can_store_resource or self.is_capped:
            return False
        # 자원 적재 기본 로직
        self.content = resource_amount
        return True

class WorkerCell(BaseCell):
    """일벌방 및 일반적인 자원(꿀, 화분)을 저장하는 기본 데이터 스토리지입니다."""
    def __init__(self, x: int, y: int, z: int):
        super().__init__(x, y, z)
        self.type = "WORKER_CELL"

class DroneCell(BaseCell):
    """격리된 샌드박스 역할을 하는 수컷방 객체입니다."""
    def __init__(self, x: int, y: int, z: int):
        super().__init__(x, y, z)
        self.type = "DRONE_CELL"
        # 보안 규칙: 수컷방 꿀 저장 불가 (샌드박스 데이터 격리)
        self.can_store_resource = False
        
    def execute_sandbox_process(self, external_data: Any) -> None:
        """외부 자원을 수정할 수 없고 읽기(Read-Only)만 가능한 샌드박스 실행 환경입니다."""
        pass
        
    def extract_data(self) -> None:
        """
        보안 규칙: 샌드박스에서 외부로의 물리적 데이터 이동을 차단합니다.
        해당 메서드 호출 시 보안 예외를 발생시킵니다.
        """
        raise PermissionError("Data exfiltration from Drone Cell Sandbox is strictly blocked.")

class QueenCell(BaseCell):
    """시스템 장애 시 새로운 분산 리더 선출을 위해 생성되는 비상 왕대입니다."""
    def __init__(self, x: int, y: int, z: int):
        super().__init__(x, y, z)
        self.type = "QUEEN_CELL"