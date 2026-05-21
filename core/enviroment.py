# core/environment.py
from configs.constants import MIN_SAFE_TEMP, MAX_SAFE_TEMP

class EnvironmentManager:
    """온습도 및 외부 환경을 제어하며 Fuzzing 공격을 방어하는 모듈입니다."""
    
    def __init__(self):
        self.temperature: float = 25.0
        self.humidity: float = 50.0
        self.is_hibernating: bool = False
        
    def update_environment(self, new_temp: float, new_humidity: float) -> None:
        """외부에서 주입되는 환경 데이터를 검증(Sanitization)합니다."""
        if self._is_fuzzing_attack(new_temp, new_humidity):
            self._trigger_fail_safe()
            return
            
        self.temperature = new_temp
        self.humidity = new_humidity
        
    def _is_fuzzing_attack(self, temp: float, humidity: float) -> bool:
        """말도 안 되는 값이 유입되는지 확인합니다 (예: 10,000°C)."""
        if temp < MIN_SAFE_TEMP or temp > MAX_SAFE_TEMP:
            return True
        if humidity < 0.0 or humidity > 100.0:
            return True
        return False
        
    def _trigger_fail_safe(self) -> None:
        """예상치 못한 환경 값 유입 시 군집 전체를 안전하게 동면 모드로 전환합니다."""
        self.is_hibernating = True
        # TODO: Engine에 동면 상태 브로드캐스팅 로직 추가