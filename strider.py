"""
Fishing automation script for Minescript.
Casts the rod, monitors nearby entities for the bobber "bite" signal,
then reels in and recasts.
"""
import time
import minescript as m


def cast_rod():
    """Cast the fishing rod by simulating right-click press and release."""
    m.player_press_use(True)
    m.player_press_use(False)


def reel_in():
    """Reel in the fishing rod."""
    m.player_press_use(True)
    m.player_press_use(False)


# Reel-in trigger markers. Hypixel/SkyBlock often uses '!!!' or red color code (§c) in the bobber entity name
REEL_TRIGGERS = ("!!!", "§c")


def is_reel_trigger(entity) -> bool:
    """
    Check if an entity's name indicates it's time to reel in.

    On fishing servers (e.g. Hypixel SkyBlock), the fishing bobber entity
    may get a custom name when a fish bites. Common signals include:
    - '!!!' (exclamation marks) in the entity name
    - '§c' (Minecraft red color code) to highlight the bobber when bite occurs

    We use a substring check rather than regex for simplicity and to avoid
    false negatives from different server implementations.
    """
    name = getattr(entity, "name", None)
    if not name or not isinstance(name, str):
        return False
    return any(trigger in name for trigger in REEL_TRIGGERS)


def main():
    cast_rod()

    while True:
        for entity in m.entities():
            if is_reel_trigger(entity):
                reel_in()
                time.sleep(1.5)  # Allow for server lag and loot animations
                cast_rod()
                break
        time.sleep(0.05)  # Throttle the scan loop


if __name__ == "__main__":
    main()
