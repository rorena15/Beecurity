# core/engine.py
import numpy as np
from typing import List
from entities.base_bee import BaseBee
from entities.queen import QueenBee
from configs.constants import PHEROMONE_CHECK_INTERVAL, ENERGY_CONSUMPTION_RATE

class SwarmEngine:
    """수만 마리의 에이전트 연산을 위한 NumPy 기반 벡터화 엔진입니다."""
    def __init__(self, agent_count: int):
        self.tick: int = 0
        self.agents: List[BaseBee] = []
        self.queen_node: QueenBee = None
        
        # 위치 및 에너지 상태를 2D 배열로 관리 (벡터화 적용)
        self.positions = np.zeros((agent_count, 2), dtype=np.float32)
        self.energies = np.full(agent_count, 100.0, dtype=np.float32)

    def register_queen(self, queen: QueenBee) -> None:
        self.queen_node = queen

    def run_tick(self) -> None:
        self.tick += 1
        
        # 1. 벡터화 연산을 통한 물리/자원 일괄 업데이트
        self._vectorized_physics_update()

        # 2. 하트비트 체크 및 자가 치유 프로토콜 (Lazy Evaluation 적용)
        if self.tick % PHEROMONE_CHECK_INTERVAL == 0:
            self._verify_leader_heartbeat()

        # 3. 에이전트 개별 의사결정 (개별 판단시에만 제한적 루프 사용)
        for agent in self.agents:
            if agent.is_alive:
                agent.update(self.tick)

    def _vectorized_physics_update(self) -> None:
        """Python for 루프 대신 NumPy를 사용한 성능 최적화 연산입니다."""
        self.energies -= ENERGY_CONSUMPTION_RATE
        
        # 에너지 고갈에 따른 사망 처리 로직
        dead_indices = np.where(self.energies <= 0)[0]
        if len(dead_indices) > 0:
            self._handle_dead_agents(dead_indices)

    def _handle_dead_agents(self, indices: np.ndarray) -> None:
        """가비지 컬렉션이 원활하도록 죽은 에이전트의 참조를 해제합니다."""
        pass

    def _verify_leader_heartbeat(self) -> None:
        """마스터 노드의 하트비트 검증 및 자가 치유(Self-Healing) 트리거"""
        if self.queen_node and not self.queen_node.send_heartbeat(self.tick):
            self._trigger_self_healing_failover()

    def _trigger_self_healing_failover(self) -> None:
        """중앙 제어기 장애 시, 숙련도 높은 노드를 선출하여 임시 제어기로 승격시킵니다."""
        eligible_workers = [a for a in self.agents if a.is_alive and getattr(a, 'experience', 0) > 0]
        if eligible_workers:
            new_master = max(eligible_workers, key=lambda worker: worker.experience)
            new_master.promote_to_temporary_master()