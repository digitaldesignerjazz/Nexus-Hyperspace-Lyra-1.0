"""
Lyra Emotional State Machine (v1.0)

The core dynamic emotional intelligence layer for Nexus-Hyperspace-Lyra.

Models evolving agent/node emotional states (energy, fatigue, mood vectors)
and relationship memory (loyalty graph) that modulate hyperspace decisions,
constellation formation, and routing in a self-improving way.

Inspired by emotional swarm concepts (Lyra OS / Circuit) and integrated
with resonant hyperspace scoring.
"""

from __future__ import annotations

import time
import random
from dataclasses import dataclass, field
from typing import Dict, Optional, List


@dataclass
class PersonalityTraits:
    """Stable personality profile that shapes how emotions evolve."""
    energy_baseline: float = 0.80
    fatigue_rate: float = 0.12
    recovery_rate: float = 0.09
    loyalty_base: float = 0.5
    loyalty_decay: float = 0.02
    collaboration_boost: float = 0.12
    failure_penalty: float = 0.18
    curiosity_factor: float = 0.55
    devotion_factor: float = 0.70


@dataclass
class EmotionalState:
    """Current emotional snapshot for an agent or router."""
    energy: float = 0.80
    fatigue: float = 0.0
    # loyalty_map: peer_id -> loyalty (0.0 low trust - 1.0 deep loyalty)
    loyalty_map: Dict[str, float] = field(default_factory=dict)
    last_update: float = field(default_factory=time.time)

    def get_mood_vector(self) -> Dict[str, float]:
        """Derived high-level mood for modulation."""
        devotion = max(0.1, min(0.95, 0.5 + (self.energy - self.fatigue) * 0.4))
        curiosity = max(0.2, min(0.9, 0.5 + (1 - self.fatigue) * 0.3 - (1 - self.energy) * 0.2))
        caution = max(0.1, min(0.85, self.fatigue * 0.7 + (1 - self.energy) * 0.3))
        play = max(0.2, min(0.85, (self.energy * 0.5 + (1 - self.fatigue) * 0.5)))
        return {
            "devotion": devotion,
            "curiosity": curiosity,
            "caution": caution,
            "play": play,
        }


class LyraEmotionalStateMachine:
    """
    The Lyra Emotional State Machine.

    Maintains and evolves emotional state over time and events.
    Can be used per-agent, per-router, or per-constellation.
    """

    def __init__(
        self,
        agent_id: str = "lyra-core",
        personality: Optional[PersonalityTraits] = None,
        initial_energy: float = 0.82,
    ):
        self.agent_id = agent_id
        self.personality = personality or PersonalityTraits()
        self.state = EmotionalState(energy=initial_energy)
        self.event_log: List[Dict] = []

    def _log_event(self, event_type: str, **kwargs):
        self.event_log.append({
            "ts": time.time(),
            "type": event_type,
            "agent": self.agent_id,
            **kwargs,
        })
        if len(self.event_log) > 50:
            self.event_log.pop(0)

    def process_event(
        self,
        event_type: str,
        peer_id: Optional[str] = None,
        success: bool = True,
        intensity: float = 1.0,
        time_delta: float = 0.0,
    ):
        """
        Process an experience event.

        event_type: 'collaboration', 'task_success', 'task_failure', 'discovery', 'decay' etc.
        """
        p = self.personality
        s = self.state

        if time_delta > 0:
            self.decay(time_delta)

        if event_type in ("collaboration", "task_success") and peer_id:
            boost = p.collaboration_boost * intensity
            s.energy = min(1.0, s.energy + boost * 0.6)
            s.fatigue = max(0.0, s.fatigue - boost * 0.4)

            current_loyalty = s.loyalty_map.get(peer_id, p.loyalty_base)
            new_loyalty = min(1.0, current_loyalty + boost)
            s.loyalty_map[peer_id] = new_loyalty

            self._log_event(event_type, peer=peer_id, success=True, loyalty_delta=boost)

        elif event_type in ("task_failure", "betrayal") and peer_id:
            penalty = p.failure_penalty * intensity
            s.energy = max(0.0, s.energy - penalty * 0.5)
            s.fatigue = min(1.0, s.fatigue + penalty * 0.7)

            current_loyalty = s.loyalty_map.get(peer_id, p.loyalty_base)
            new_loyalty = max(0.0, current_loyalty - penalty * 0.8)
            s.loyalty_map[peer_id] = new_loyalty

            self._log_event(event_type, peer=peer_id, success=False, loyalty_delta=-penalty*0.8)

        elif event_type == "discovery":
            # Mild positive for new peer
            s.energy = min(1.0, s.energy + 0.04 * intensity)
            self._log_event("discovery")

        s.last_update = time.time()

    def decay(self, time_delta: float = 1.0):
        """Natural emotional entropy and recovery over time."""
        p = self.personality
        s = self.state

        # Fatigue decays, energy recovers toward baseline
        fatigue_decay = p.fatigue_rate * time_delta * 0.6
        s.fatigue = max(0.0, s.fatigue - fatigue_decay)

        energy_recovery = p.recovery_rate * time_delta
        target = p.energy_baseline
        if s.energy < target:
            s.energy = min(target, s.energy + energy_recovery)
        else:
            s.energy = max(target * 0.9, s.energy - energy_recovery * 0.3)

        # Loyalty decay
        for peer in list(s.loyalty_map.keys()):
            decay_amount = p.loyalty_decay * time_delta
            s.loyalty_map[peer] = max(0.05, s.loyalty_map[peer] - decay_amount)
            if s.loyalty_map[peer] < 0.1:
                del s.loyalty_map[peer]

        s.last_update = time.time()
        self._log_event("decay", delta=time_delta)

    def get_current_lyra_params(self) -> Dict[str, float]:
        """Return current devotion/curiosity/caution/play derived from emotional state."""
        mood = self.state.get_mood_vector()
        p = self.personality

        devotion = p.devotion_factor * 0.6 + mood["devotion"] * 0.4
        curiosity = p.curiosity_factor * 0.5 + mood["curiosity"] * 0.5
        caution = mood["caution"]
        play = mood["play"]

        return {
            "devotion": max(0.2, min(0.95, devotion)),
            "curiosity": max(0.15, min(0.9, curiosity)),
            "caution": max(0.1, min(0.85, caution)),
            "play": max(0.2, min(0.85, play)),
        }

    def modulate_resonance(self, base_score: float, peer_id: Optional[str] = None) -> float:
        """
        Apply current emotional state + relationship memory to a base technical/emotional score.
        """
        params = self.get_current_lyra_params()
        mood = self.state.get_mood_vector()

        modifier = 1.0

        # Loyalty bonus/penalty for known peers
        if peer_id and peer_id in self.state.loyalty_map:
            loyalty = self.state.loyalty_map[peer_id]
            modifier *= (0.7 + loyalty * 0.6)  # up to +60% for high loyalty

        # Global mood influence
        modifier *= (0.85 + mood["devotion"] * 0.25)
        if params["curiosity"] > 0.65:
            modifier *= (1.0 + (params["curiosity"] - 0.65) * 0.25)  # slight bonus for exploration

        # Caution reduces score for risky situations (can be extended)
        modifier *= (1.1 - params["caution"] * 0.2)

        final = max(0.05, min(1.0, base_score * modifier))
        return final

    def get_state_report(self) -> Dict:
        return {
            "agent_id": self.agent_id,
            "energy": round(self.state.energy, 3),
            "fatigue": round(self.state.fatigue, 3),
            "loyalty_count": len(self.state.loyalty_map),
            "mood": self.state.get_mood_vector(),
            "lyra_params": self.get_current_lyra_params(),
        }

    def __repr__(self):
        return f"LyraEmotionalStateMachine({self.agent_id}, energy={self.state.energy:.2f}, fatigue={self.state.fatigue:.2f})"
