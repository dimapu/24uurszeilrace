from collections import Counter
from itertools import pairwise


def check_leg_repetition(ends: list) -> tuple[bool, str]:
    MAX_LEG_REP = 2
    n = Counter("{}{}".format(*sorted([s, e])) for s, e in pairwise(ends))

    if n.most_common(1)[0][1] > MAX_LEG_REP:
        data = n.most_common(1)
        return False, f"Some legs are used more than {MAX_LEG_REP} times: {data}."

    
def evaluate_correctness(ends: list):
    repetitions_result = check_leg_repetition(ends)
    
    if repetitions_result[0] is False:
        return repetitions_result
    
    if ends[-1] != "TOCHT":
        return False, f"Finish must be TOCHT rather than {ends[-1]}."
    
    if ends[0] not in ["ENKN", "HIND", "LELYN", "MED", "OEVE", "STAV", "LEMMER"]:
        return False, f"Start must be a proper start rather than {ends[0]}."

