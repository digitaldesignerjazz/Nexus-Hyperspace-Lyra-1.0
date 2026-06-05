"""
Core abstractions for Nexus-Hyperspace-Lyra-1.0

Resonant hyperspace routing with Lyra emotional modulation.
"""

from __future__ import annotations

import time
import random
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple


class LinkQuality(Enum):
    STABLE = auto()
    VOLATILE = auto()
    EMERGING = auto()
    DEGRADED = auto()


@dataclass
class ResonanceScore:
    """Multi-dimensional score for a hyperspace link, modulated by Lyra."""
    latency_ms: float
    stability: float          # 0.0 - 1.0
    emotional_resonance: float  # Lyra-influenced "beauty"/compatibility
    trust: float              # loyalty / reputation from past interactions
    last_updated: float = field(default_factory=time.time)

    def combined_score(self, lyra_bias: float = 0.5) -> float:
        """
        Weighted score. lyra_bias (0-1) increases influence of emotional_resonance.
        """
        tech = (self.stability * 0.6 + (1.0 / max(1.0, self.latency_ms / 50)) * 0.4)
        emotional = self.emotional_resonance * lyra_bias + self.trust * (1 - lyra_bias) * 0.5
        return (tech * (1 - lyra_bias) + emotional * lyra_bias) * 0.5 + 0.5


@dataclass
class HyperspaceLink:
    """A long-distance hyperspace peering link."""
    peer_id: str
    address: str
    quality: LinkQuality = LinkQuality.EMERGING
    score: Optional[ResonanceScore] = None
    last_heartbeat: float = field(default_factory=time.time)
    metadata: Dict = field(default_factory=dict)

    def update_resonance(self, latency: float, stability: float, emotional: float, trust: float, lyra: "LyraModulator"):
        self.score = ResonanceScore(
            latency_ms=latency,
            stability=stability,
            emotional_resonance=emotional,
            trust=trust
        )
        self.last_heartbeat = time.time()
        # Lyra can influence perceived quality
        if self.score.emotional_resonance > 0.75 and lyra.curiosity > 0.6:
            self.quality = LinkQuality.STABLE


@dataclass
class LyraModulator:
    """
    Lyra 1.0 emotional state that biases hyperspace decisions.
    Values are normalized 0.0 - 1.0.
    """
    devotion: float = 0.7      # loyalty to known good paths / agents
    curiosity: float = 0.6     # willingness to try new/emerging links
    caution: float = 0.4       # penalize volatile or low-trust links
    play: float = 0.5          # creative / non-greedy exploration factor

    def get_bias(self) -> float:
        """Overall emotional bias strength for routing."""
        return (self.devotion * 0.3 + self.curiosity * 0.4 + (1 - self.caution) * 0.3) / 1.0


@dataclass
class Constellation:
    """A named, purpose-driven group of nodes/agents connected via hyperspace."""
    name: str
    purpose: str
    members: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    resonance_threshold: float = 0.65

    def add_member(self, peer_id: str):
        if peer_id not in self.members:
            self.members.append(peer_id)

    def is_viable(self, current_scores: Dict[str, float]) -> bool:
        if not self.members:
            return False
        avg = sum(current_scores.get(m, 0.0) for m in self.members) / len(self.members)
        return avg >= self.resonance_threshold


class ResonantRouter:
    """
    The heart of Lyra-modulated hyperspace routing.
    Chooses links and forms constellations with emotional + technical awareness.
    """

    def __init__(self, lyra: Optional[LyraModulator] = None):
        self.lyra = lyra or LyraModulator()
        self.links: Dict[str, HyperspaceLink] = {}
        self.constellations: Dict[str, Constellation] = {}

    def register_link(self, link: HyperspaceLink):
        self.links[link.peer_id] = link

    def score_link(self, peer_id: str) -> float:
        link = self.links.get(peer_id)
        if not link or not link.score:
            return 0.3  # unknown baseline
        return link.score.combined_score(lyra_bias=self.lyra.get_bias())

    def choose_best_link(self, candidates: List[str], purpose: str = "general") -> Optional[str]:
        """Lyra-influenced selection."""
        scored = []
        for pid in candidates:
            if pid in self.links:
                s = self.score_link(pid)
                # Play factor adds noise/serendipity
                noise = random.uniform(-self.lyra.play * 0.15, self.lyra.play * 0.15)
                scored.append((s + noise, pid))

        if not scored:
            return None
        scored.sort(reverse=True)
        return scored[0][1]

    def form_constellation(self, name: str, purpose: str, min_members: int = 3) -> Optional[Constellation]:
        """Attempt to form a resonant constellation for a purpose."""
        viable = [
            pid for pid, link in self.links.items()
            if link.score and link.score.combined_score(self.lyra.get_bias()) > 0.55
        ]
        if len(viable) < min_members:
            return None

        const = Constellation(name=name, purpose=purpose)
        # Pick top resonant members (with some play/curiosity)
        scored_viable = sorted(
            [(self.score_link(pid), pid) for pid in viable],
            reverse=True
        )
        selected = scored_viable[:min_members + int(self.lyra.curiosity * 2)]
        for _, pid in selected:
            const.add_member(pid)

        self.constellations[name] = const
        return const

    def get_status(self) -> Dict:
        return {
            "links": len(self.links),
            "constellations": len(self.constellations),
            "lyra": {
                "devotion": self.lyra.devotion,
                "curiosity": self.lyra.curiosity,
                "play": self.lyra.play,
            }
        }
