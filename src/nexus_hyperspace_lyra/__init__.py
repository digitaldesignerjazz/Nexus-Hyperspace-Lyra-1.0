"""
Nexus-Hyperspace-Lyra-1.0

Decentralized, intelligent, resonant hyperspace networking
with emotional AI swarm modulation (Lyra) for the Nexus ecosystem.
"""

__version__ = "1.0.0"
__author__ = "Sven Normen Esslinger / Esslinger & Co."

from .core import (
    HyperspaceLink,
    ResonanceScore,
    LyraModulator,
    Constellation,
    ResonantRouter,
    LinkQuality,
)
from .emotional_state_machine import (
    LyraEmotionalStateMachine,
    EmotionalState,
    PersonalityTraits,
)

__all__ = [
    "HyperspaceLink",
    "ResonanceScore",
    "LyraModulator",
    "Constellation",
    "ResonantRouter",
    "LinkQuality",
    # Emotional State Machine
    "LyraEmotionalStateMachine",
    "EmotionalState",
    "PersonalityTraits",
    "__version__",
]