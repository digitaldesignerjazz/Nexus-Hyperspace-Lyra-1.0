"""
Nexus-Hyperspace-Lyra-1.0 — Basic Resonant Demo

Demonstrates Lyra-modulated hyperspace link selection and constellation formation.
Run with:
    python -m examples.basic_resonant_demo
    or
    python examples/basic_resonant_demo.py
"""

import asyncio
import random
from nexus_hyperspace_lyra import (
    HyperspaceLink,
    LyraModulator,
    ResonantRouter,
    LinkQuality,
)


async def main():
    print("=== Nexus-Hyperspace-Lyra-1.0 Resonant Demo ===\n")

    lyra = LyraModulator(devotion=0.75, curiosity=0.65, caution=0.35, play=0.55)
    router = ResonantRouter(lyra=lyra)

    # Simulate discovery of distant hyperspace peers
    peers = [
        ("alpha-distant", "2001:db8::1:alpha", 145, 0.82, 0.91, 0.78),
        ("beta-resonant", "2001:db8::1:beta",  312, 0.71, 0.95, 0.88),
        ("gamma-volatile", "2001:db8::1:gamma", 89, 0.55, 0.62, 0.41),
        ("delta-creative", "2001:db8::1:delta",  201, 0.79, 0.88, 0.69),
        ("epsilon-trusted", "2001:db8::1:eps",  167, 0.88, 0.79, 0.92),
    ]

    print("Registering hyperspace links with initial resonance data...")
    for pid, addr, lat, stab, emo, trust in peers:
        link = HyperspaceLink(peer_id=pid, address=addr, quality=LinkQuality.EMERGING)
        link.update_resonance(lat, stab, emo, trust, lyra)
        router.register_link(link)
        print(f"  + {pid}: latency={lat}ms, resonance={link.score.combined_score(lyra.get_bias()):.3f}")

    print("\n--- Lyra-modulated link selection for 'creative-swarm' ---")
    best = router.choose_best_link([p[0] for p in peers], purpose="creative-swarm")
    print(f"Best link chosen: {best}")

    print("\n--- Forming a resonant constellation ---")
    const = router.form_constellation(
        name="lyra-creative-constellation-01",
        purpose="high-resonance creative collaboration across hyperspace",
        min_members=3
    )
    if const:
        print(f"Formed: {const.name}")
        print(f"  Purpose: {const.purpose}")
        print(f"  Members: {const.members}")
    else:
        print("Could not form viable constellation with current links.")

    print("\n--- Router Status ---")
    status = router.get_status()
    print(status)

    print("\n=== Demo complete. Lyra is listening. ===")


if __name__ == "__main__":
    asyncio.run(main())
