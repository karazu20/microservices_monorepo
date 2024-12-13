import random


def generate_random_nip(len_nip: int) -> str:
    """Generate a random string of min 7 chars, max 25 max of uppercase letters and digits."""
    nip = ""
    for _ in range(len_nip):
        rand = random.randint(0, 9)  # Sensitive
        nip += str(rand)
    return nip
