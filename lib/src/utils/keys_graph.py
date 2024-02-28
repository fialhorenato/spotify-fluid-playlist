pitch_to_camelot = {
    0: {
        0: '5A',
        1: '8B'
    },
    1: {
        0: '3B',
        1: '12A'
    },
    2: {
        0: '7A',
        1: '10B'
    },
    3: {
        0: '2A',
        1: '5B'
    },
    4: {
        0: '9A',
        1: '12B'
    },
    5: {
        0: '4A',
        1: '7B'
    },
    6: {
        0: '11A',
        1: '2B'
    },
    7: {
        0: '6A',
        1: '9B'
    },
    8: {
        0: '1A',
        1: '4B'
    },
    9: {
        0: '8A',
        1: '11B'
    },
    10: {
        0: '3A',
        1: '6B'
    },
    11: {
        0: '10A',
        1: '1B'
    },
}


def change_pitch_to_camelot(pitch: int, mode: int) -> str:
    return pitch_to_camelot[pitch][mode]


def find_perfect_match_for_key(key: str) -> list[str]:
    best_matches = [key]
    chars = [char for char in key if char.isalpha()]
    numbers = [char for char in key if char.isdigit()]
    number = int(''.join(numbers))
    letter = chars[0]
    if number - 1 <= 0:
        best_matches.append("12B")
        return best_matches
    new_number = number - 1
    new_letter = chr(ord(letter) + 1)
    best_matches.append(str(new_number) + '' + new_letter)
    return best_matches
