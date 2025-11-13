# maquina/parser.py

import json
from typing import Dict, Tuple, List

from .turing import TMConfig, TransitionKey, TransitionVal


def load_mt_from_json(path: str) -> TMConfig:
    """
    Carga una MT de k cintas desde un JSON con formato:

    {
      "Q": [...],
      "Sigma": [...],
      "Gamma": [...],
      "blank": "_",
      "q0": "q0",
      "F": [...],
      "num_tapes": 2,
      "transitions": [
        [
          "q",
          ["r1","r2",...],
          "q'",
          ["w1","w2",...],
          ["m1","m2",...]
        ],
        ...
      ]
    }
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    states: List[str] = data["Q"]
    sigma: List[str] = data["Sigma"]
    gamma: List[str] = data["Gamma"]
    blank: str = data["blank"]
    q0: str = data["q0"]
    F: List[str] = data["F"]

    num_tapes: int = data.get("num_tapes", 1)

    transitions_data = data["transitions"]

    transitions: Dict[TransitionKey, TransitionVal] = {}

    for t in transitions_data:
        if len(t) != 5:
            raise ValueError(f"Transición inválida, se esperaban 5 elementos: {t}")
        state = t['0'] if isinstance(t, dict) else t[0]  # por si alguien usa dict
        reads = t['1'] if isinstance(t, dict) else t[1]
        next_state = t['2'] if isinstance(t, dict) else t[2]
        writes = t['3'] if isinstance(t, dict) else t[3]
        moves = t['4'] if isinstance(t, dict) else t[4]

        if not (isinstance(reads, list) and isinstance(writes, list) and isinstance(moves, list)):
            raise ValueError(f"reads/writes/moves deben ser listas: {t}")

        if not (len(reads) == len(writes) == len(moves) == num_tapes):
            raise ValueError(f"Longitud inconsistente con num_tapes en transición: {t}")

        key: TransitionKey = (state, tuple(reads))
        val: TransitionVal = (next_state, tuple(writes), tuple(moves))

        if key in transitions:
            raise ValueError(f"Transición duplicada para {key}")
        transitions[key] = val

    return TMConfig(
        states=states,
        input_alphabet=sigma,
        tape_alphabet=gamma,
        blank=blank,
        initial_state=q0,
        accept_states=F,
        transitions=transitions,
        num_tapes=num_tapes,
    )
