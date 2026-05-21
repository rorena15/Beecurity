# managers/beekeeper.py
from typing import Optional
from configs.constants import (
    MAX_SAFE_INSPECTION_TIME,
    INSPECTION_STRESS_RATE,
    SMOKER_AGGRESSION_REDUCTION,
    SMOKER_HONEY_CONSUMPTION_INC,
    SMOKER_FORAGING_PENALTY,
    SAFE_HARVEST_RATIO,
    STARVATION_RISK_MULTIPLIER,
    ROBBING_RISK_MULTIPLIER
)

class BeekeeperManager:
    """내검(Inspection) 및 훈증(Smoker) 등 관리자 개입을 제어하는 객체입니다."""
    
    def __init__(self, valid_access_key: str):
        self._valid_access_key = valid_access_key
        self.colony_stress: float = 0.0
        self.audit_cpu_usage: float = 0.0
        
    def _authenticate(self, access_key: str) -> bool:
        """관리자 개입 전 토큰 대조를 통한 권한을 검증합니다."""
        return self._valid_access_key == access_key

    def inspect_colony(self, access_key: str, time_spent: int, current_temp: float) -> bool:
        """
        내검(보안 감사)을 수행합니다. 
        빈번하거나 긴 내검은 Anti-Audit Fatigue 정책에 의해 시스템 효율을 강제 하락시킵니다.
        """
        if not self._authenticate(access_key):
            self._log_audit("Unauthorized inspection attempt blocked.")
            return False
            
        # 내검 오버헤드 계산 (15분 초과 시 분당 스트레스 +2.0)
        if time_spent > MAX_SAFE_INSPECTION_TIME:
            excess_time = time_spent - MAX_SAFE_INSPECTION_TIME
            self.colony_stress += excess_time * INSPECTION_STRESS_RATE
            
        # 18°C 이하 내검 시 유충 사망 확률 트리거 (구현은 Engine에서 처리)
        if current_temp <= 18.0:
            self._log_audit("Warning: Cold inspection triggered Larva_Death_Probability.")

        self._log_audit(f"Inspection completed. Current stress: {self.colony_stress}")
        return True

    def use_smoker(self, access_key: str) -> bool:
        """
        훈증기를 사용합니다. 공격성은 낮아지지만 자원 소모가 급증합니다.
        """
        if not self._authenticate(access_key):
            return False
            
        # TODO: SwarmEngine에 훈증 상태 브로드캐스팅
        # 브로드캐스트 내용: Aggression -80%, Honey_Consumption +15%, Foraging -10%
        self._log_audit("Smoker deployed: Aggression suppressed, consumption increased.")
        return True

    def calculate_efficiency_impact(self) -> float:
        """
        관리자의 잦은 내검(오버헤드)이 군집 효율 지수에 미치는 타격을 계산합니다.
        """
        # 스트레스를 기반으로 한 가용성 저하 산출
        stress_penalty = max(0.0, 1.0 - (self.colony_stress / 100.0))
        return stress_penalty

    def harvest_honey(self, access_key: str, total_honey_stock: float, request_amount: float) -> float:
        """
        채밀(Data Extraction)을 시도합니다. 대량 회수 시 군집 방어력과 생존력이 급감합니다.
        """
        if self._valid_access_key != access_key:
            return 0.0
            
        # Setter Validation: 음수 및 최대량 초과 요청 방지 (Anti-Cheating)
        if request_amount <= 0 or request_amount > total_honey_stock:
            return 0.0

        harvest_ratio = request_amount / total_honey_stock
        
        # 안전 회수 비율(30%)을 초과하여 채밀할 경우 패널티(취약점) 부과
        if harvest_ratio > SAFE_HARVEST_RATIO:
            excess_ratio = harvest_ratio - SAFE_HARVEST_RATIO
            self.starvation_risk += excess_ratio * STARVATION_RISK_MULTIPLIER
            self.robbing_risk += excess_ratio * ROBBING_RISK_MULTIPLIER
            self._log_audit("WARNING: Over-harvesting detected. System vulnerability increased.")

        # 채밀 후 남은 자원을 계산하여 반환
        extracted_amount = request_amount
        return extracted_amount

    def _log_audit(self, message: str) -> None:
        pass