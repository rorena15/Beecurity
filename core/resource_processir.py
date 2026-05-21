# core/resource_processor.py
from entities.worker import WorkerBee

class ResourceProcessor:
    """Nectar를 Honey로 가공하여 시스템 자원을 최적화하는 보안/자원 매니저입니다."""
    
    def __init__(self):
        self.conversion_efficiency: float = 0.85  # Nectar -> Honey 전환 효율
        
    def process_transfer(self, forager: WorkerBee, receiver: WorkerBee, nectar_amount: float) -> float:
        """
        외부에서 유입된 자원을 내부 에이전트가 가공합니다.
        권한(RBAC) 검증 실패 시 데이터 조작으로 간주하고 처리를 거부합니다.
        """
        # 1. 권한 검증: 수신자는 반드시 내부망 접근 권한을 가진 내역봉이어야 함
        if receiver._network_access != "INTERNAL_ONLY":
            return 0.0
            
        # 2. 권한 검증: 전달자는 외부망 접근 권한을 가진 외역봉이어야 함
        if forager._network_access != "EXTERNAL_ACCESS":
            return 0.0
            
        # 3. 데이터 변환(가공) 연산 수행
        produced_honey = nectar_amount * self.conversion_efficiency
        
        # 4. 숙련도(Experience) 증가: 성공적인 자원 전송 시 숙련도 부여
        receiver.experience += 1
        forager.experience += 1
        
        return produced_honey