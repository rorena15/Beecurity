# configs/config.py
from dataclasses import dataclass

@dataclass
class EnvironmentConfig:
    """환경 및 디버그 설정을 관리하는 설정 클래스입니다."""
    enable_dynamic_weather: bool = False
    verbose_mode: bool = True  # 개발 단계 디버깅을 위한 출력 플래그
    
env_config = EnvironmentConfig()