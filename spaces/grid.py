# spaces/grid.py
from typing import Dict, Tuple, Optional
from spaces.cells import BaseCell, WorkerCell, DroneCell, QueenCell

class HexGrid:
    """육각형 그리드 기반 공간 정의 및 관리를 담당하는 시스템입니다."""
    def __init__(self, radius: int):
        self.radius = radius
        # (x, y, z) 큐브 좌표계를 키로 사용하여 셀 객체를 저장합니다.
        self.cells: Dict[Tuple[int, int, int], BaseCell] = {}
        self._initialize_grid()

    def _initialize_grid(self) -> None:
        """초기 육각형 벌집 공간을 생성합니다."""
        # MVP 모델에서는 중앙을 일벌방, 외곽 일부를 수컷방으로 할당합니다.
        for q in range(-self.radius, self.radius + 1):
            for r in range(max(-self.radius, -q - self.radius), min(self.radius, -q + self.radius) + 1):
                s = -q - r
                coordinate = (q, r, s)
                
                # 테스트 환경을 위한 임의의 샌드박스(수컷방) 구역 할당
                if abs(q) == self.radius or abs(r) == self.radius:
                    self.cells[coordinate] = DroneCell(q, r, s)
                else:
                    self.cells[coordinate] = WorkerCell(q, r, s)

    def get_cell(self, x: int, y: int, z: int) -> Optional[BaseCell]:
        """특정 좌표의 셀 객체를 반환합니다."""
        return self.cells.get((x, y, z))

    def attempt_storage(self, x: int, y: int, z: int, amount: float) -> bool:
        """
        에이전트가 자원을 적재하려 할 때, 해당 셀의 권한(샌드박스 여부)을 검증하고 처리합니다.
        """
        target_cell = self.get_cell(x, y, z)
        if target_cell:
            return target_cell.store_resource(amount)
        return False