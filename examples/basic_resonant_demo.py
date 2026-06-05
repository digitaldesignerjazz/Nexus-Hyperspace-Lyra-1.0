"""
Nexus-Hyperspace-Lyra-1.0 — Basic Resonant Demo with Emotional State Machine

Demonstrates dynamic Lyra emotional state evolution over time,
impact on resonance scoring, link selection, and constellation formation.

Run with:
    python -m examples.basic_resonant_demo
"""

import asyncio
import random
from nexus_hyperspace_lyra import (
    HyperspaceLink,
    LyraModulator,
    ResonantRouter,
    LinkQuality,
    LyraEmotionalStateMachine,
    PersonalityTraits,
)


async def main():
    print("=== Nexus-Hyperspace-Lyra-1.0 Emotional State Machine Demo ===\n")

    # Create a Lyra emotional state machine (the new core)
    lyra_sm = LyraEmotionalStateMachine(
        agent_id="router-lyra-prime",
        personality=PersonalityTraits(
            energy_baseline=0.82,
            curiosity_factor=0.68,
            devotion_factor=0.72,
        ),
        initial_energy=0.85,
    )

    # The modulator can still be used for static bias, but we drive dynamically
    lyra_static = LyraModulator(devotion=0.72, curiosity=0.68, caution=0.32, play=0.58)
    router = ResonantRouter(lyra=lyra_static)

    # Simulate discovery of distant hyperspace peers
    peers = [
        ("alpha-distant", "2001:db8::1:alpha", 145, 0.82, 0.91, 0.78),
        ("beta-resonant", "2001:db8::1:beta",  312, 0.71, 0.95, 0.88),
        ("gamma-volatile", "2001:db8::1:gamma", 89, 0.55, 0.62, 0.41),
        ("delta-creative", "2001:db8::1:delta",  201, 0.79, 0.88, 0.69),
        ("epsilon-trusted", "2001:db8::1:eps",  167, 0.88, 0.79, 0.92),
    ]

    print("Registering hyperspace links...")
    for pid, addr, lat, stab, emo, trust in peers:
        link = HyperspaceLink(peer_id=pid, address=addr, quality=LinkQuality.EMERGING)
        link.update_resonance(lat, stab, emo, trust, lyra_static)
        router.register_link(link)

    print("\n--- Initial state --- ")
    print(lyra_sm.get_state_report())

    # Simulate a series of experiences over "time"
    print("\n--- Simulating experiences (time steps + events) --- ")
    for step in range(1, 7):
        print(f"\nStep {step}:")

        # Random experiences
        if random.random() < 0.7:
            peer = random.choice([p[0] for p in peers])
            success = random.random() > 0.25
            intensity = random.uniform(0.6, 1.3)
            lyra_sm.process_event("collaboration" if success else "task_failure", 
                                  peer_id=peer, success=success, intensity=intensity)
            print(f"  Event: collaboration with {peer} (success={success}, intensity={intensity:.2f})")

        # Natural decay + time
        lyra_sm.decay(time_delta=1.8)

        # Recompute current params from the state machine
        current_params = lyra_sm.get_current_lyra_params()
        print(f"  Current mood: { {k: round(v,3) for k,v in lyra_sm.state.get_mood_vector().items()} }")

        # Show modulated scores for a few links
        modulated = {}
        for p in peers[:3]:
            pid = p[0]
            base = router.score_link(pid) if pid in router.links else 0.5
            mod = lyra_sm.modulate_resonance(base, peer_id=pid)
            modulated[pid] = round(mod, 3)
        print(f"  Modulated resonances: {modulated}")

        # Occasionally form constellation with current state
        if step % 2 == 0:
            const = router.form_constellation(
                name=f"lyra-constellation-step{step}",
                purpose="adaptive resonant group",
                min_members=3
            )
            if const:
                print(f"  Formed constellation: {const.name} with {len(const.members)} members")

    print("\n--- Final emotional state --- ")
    print(lyra_sm.get_state_report())

    print("\n=== Demo complete. The Lyra emotional state machine is now driving resonance. ===")


if __name__ == "__main__":
    asyncio.run(main())
