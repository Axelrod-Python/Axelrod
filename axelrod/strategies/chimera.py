import axelrod as axl
from axelrod.action import Action

C, D = Action.C, Action.D

# FSM Probe: 16-state FSM for probe phase (turns 0-4)
# Encoding: 64 chars = 32 transitions (16 states x 2 inputs C/D)
# Each transition = 2 chars: hex(to_state) + output(C/D)
PROBE_FSM = "0C8D6C0D3C2D0C3D1D6D2C8D3C1D4D2C5CBDAD7CDD7DFD3D3C8D5D7D3D7CBC8D"

# Trained FSMs per opponent pattern (first 5 moves)
# Format: init_state(hex) + init_action(C/D) + 64-char transitions = 66 chars
FSMS = {
    "CCCCC": "0D0CAD4D0CBD5C3D9C7D5CDD6C6DAD8C2DDDEDBD0C9C3D9D7C3CED6CBD1C1D2DCD",
    "CCCCD": "0C0CCD7C7DFDBC3D3DDDCDCC2C5DCC3CBC9D5C2D0C6DADFCED3CEC1C4D4D4CED0D",
    "CCCDC": "CDDD3DFD2D1D8C3C2CFD3C2C7CFCCC8CADCDAD9DCCACAC9DDCEDADCC7CCDCD5DFC",
    "CCCDD": "0C9DDDACAC0CED3C3D4D0D6C0D5C4DECCC5D1CAC5D8D6CFD7C3DBDDDDDDC5CFD6C",
    "CCDCC": "1D4CCC7CCD2C3D3D3D4D6DCD4C5CACBCDD8DEC9D3D2DFDBDFD2C4C3DAC1D5CAD6D",
    "CCDCD": "8CBCDC1C1D5D4C7D1DED6C8DEC8C7C4D6CEDED1D8C6D7D1DCC8C9DFC0C8CCC5D4C",
    "CCDDC": "5CDDEDFCDC6D7D9D9DAD7C1CDD7DFDAD4CED2CBD5D2CFD8D0CCC4DFD3D0C8DCD7D",
    "CCDDD": "6DED7DEC0DAC6C4D7D6DBDAC1C2D4CFC0C6D6D9DCD7D2C8CFC4D2D6CDD6DBD8D8D",
    "CDCCC": "0C0CCD3D6C2DED3D3D0C0DCDAD5CCD3D1C5C5C0C0DBD8CFD5D8CBDDD7DDDDDFD2C",
    "CDCCD": "0C0DCD7D6C2DED3D3D0C0CCDAD5CCD3C1C5C5C0C0DBC8DFD5D8DBDDD7CBDDC4D6C",
    "CDCDC": "1C0C0D3D6C2DEC3D3D0D0CCDAD5C3D3C1C5D5C0C0DBD8CFD5C8CCCDD7DDDDDFD2D",
    "CDCDD": "0C0CCD3C6D2CED3D3D9C0CCCAD5CDC3D1C5C5D0D0D5D8CFD5C8CBCDD7DDCDDFC2C",
    "CDDCC": "0C0DCC3D0C2DED3D3D0D0DCDAD5CCD3D1C5C5C0D0DBD8CFD5D8CBDDD7DDDDDFD4C",
    "CDDCD": "0C0CDDFD6C2DED3D3D0C0DCDDD5DCC3D1D6C5CFD0DBD8DED5D5CBDDD7DDDDDDD2C",
    "CDDDD": "ED1CDCDDCCFD6C6D8DFDDD5D6D5D6D2CCDADCD8C0DCD3CBC5DACDC5D8DDDBC4D2C",
    "DCCCC": "3C9DCD2D3CEC0D8DFDBD5C9C9D4D8C7C5D4CAD7C3C2D7D6DEDCCFD3C3DDCECFDFC",
    "DCCDC": "1C0DCC3D6C2CED3D3D2D0DCCAD5CCC3D1D5D5D0CEDBD8CFD5D8DBDDDBDDD8CFD2C",
    "DCDCD": "0C0DFC6C1D9D9C7D8DBC2CCDDC5CEC9D6C6DAD4C2CCD5CFDADECADDC7D8C3D8CBD",
    "DCDDD": "3D1CED9C9D1D9C8DDC2C8C1CDD5CCD7C0C5CEC5C4CBDBC8C6C2D7D8CACBCAC0D5D",
    "DDCCC": "3D9D9CAD5D5D5D3D3D4DAD1C7DFC3DCDAC6DBD4DBC7C6C1D7C5DDDDC7D5C7D4DFD",
    "DDCCD": "0CBCCD3D6C2C3D0DFC0D0CCDAD5D7D4C4C5D2C0C7DBD8CFD8C8C0D5D7DDDDCFC8C",
    "DDCDC": "0CDCDD3C6C2DEC3D3D5CADCDAD1CCC3D1C5C5D6D0DBD8CFD5D8DBDDD7DDDDDFD2C",
    "DDCDD": "3D1D4DCDBCFD4C1C4C9DFD4DFD7CAD4C1C3DFD5C4DDC4C3C7D0C4D6CFD0DFDCDAD",
    "DDDCD": "CC0DCC3D6C2D8D7C3D0C4D5CFD5DCC3C5C5D5C0D0DBDECFD5D6D2D2D7CDD7C8C8D",
    "DDDDC": "3CFDCDAC2D1DED3DDD0D0DCCAC5CCD7C7C5C0C8D0CBD8CFD5D0CBD6D7DEDDDFD6D",
    "DDDDD": "8D8D1CED6CBCCC0D4CADFD1DDC2C6DDC5D5CDCED2C7D5C6D8DCC5CDDDD2D1D0D2D",
}

# Give up (keep defecting) when
CHECK_INTERVAL = 28
RESET_THRESHOLD = -20


def decode_fsm(enc):
    trans = {}
    for state in range(16):
        for i, inp in enumerate([C, D]):
            idx = (state * 2 + i) * 2
            trans[(state, inp)] = (int(enc[idx], 16), C if enc[idx + 1] == 'C' else D)
    return trans


class Chimera(axl.Player):
    """
    An adaptive FSM-based strategy that probes the opponent and selects
    an appropriate finite state machine based on their behavior.

    The strategy operates in four phases:

    1. **Probe (turns 0-4)**: Uses a reactive 16-state FSM to probe the opponent
       while gathering information about their behavior pattern.

    2. **Classification (turn 5)**: Analyzes the opponent's first 5 moves to
       create a 5-character pattern (e.g., "CCDDC"). This pattern is used to
       select the most appropriate FSM from 26 pre-trained FSMs.

    3. **FSM Operation (turn 6+)**: Plays using the selected FSM, which was
       trained to perform optimally against opponents matching that pattern.

    4. **Reset Check (turn 28)**: If the score differential drops below -20,
       switches permanently to Always Defect mode as a protective measure.

    A genetic chimerism or chimera is a single organism composed of cells
    of different genotypes (Wikipedia)

    Names:

    - Chimera: Original name by Joep Vullinghs
    """

    name = "Chimera"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self):
        super().__init__()
        self._probe = decode_fsm(PROBE_FSM)
        self._cache = {}
        self._reset_state()

    def _reset_state(self):
        self._trans = None
        self._state = self._probe_state = 0
        self._in_probe = True
        self._in_alld = False
        self._score = 0

    def _load_fsm(self, pattern):
        if pattern not in FSMS:
            pattern = "DDDDD"
        if pattern not in self._cache:
            data = FSMS[pattern]
            self._cache[pattern] = (
                int(data[0], 16),
                C if data[1] == 'C' else D,
                decode_fsm(data[2:])
            )
        self._state, init_act, self._trans = self._cache[pattern]
        return init_act

    def strategy(self, opponent):
        turn = len(self.history)

        # Update score differential
        if turn > 0:
            my, opp = self.history[-1], opponent.history[-1]
            if my == C and opp == D:
                self._score -= 5
            elif my == D and opp == C:
                self._score += 5

        # Probe phase (turns 0-4)
        if self._in_probe:
            if turn == 0:
                return C
            if turn < 5:
                self._probe_state, out = self._probe[(self._probe_state, opponent.history[-1])]
                return out
            # Turn 5: classify and load FSM
            self._in_probe = False
            pattern = ''.join('C' if m == C else 'D' for m in opponent.history[:5])
            self._load_fsm(pattern)
            # React to X4 (opponent's last move)
            key = (self._state, opponent.history[-1])
            if key in self._trans:
                self._state, out = self._trans[key]
                return out
            return C

        # Reset check from turn 28 onwards
        if not self._in_alld and turn >= CHECK_INTERVAL and self._score < RESET_THRESHOLD:
            self._in_alld = True

        if self._in_alld:
            return D

        # FSM operation
        key = (self._state, opponent.history[-1])
        if key in self._trans:
            self._state, out = self._trans[key]
            return out
        return C

    def reset(self):
        super().reset()
        self._reset_state() 