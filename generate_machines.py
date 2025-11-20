"""Genera las MT de cifrado César (encoder/decoder) en JSON.

Salida:
    - ejemplos/mt_encoder.json
    - ejemplos/mt_decoder.json

Notas:
    - 1 cinta; entrada: "LLAVE#MENSAJE" (llave 0..26 o A..Z).
    - Se crean estados qKey_k y qProc_k para k=0..26.
    - Solo letras A..Z cambian; espacio y punto se copian.
"""

from pathlib import Path
import json

ALPHABET = [
    "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"
]
ALPHABET_LEN = len(ALPHABET)  # 26

SIGMA_BASE = [" ", "#", "."] + ALPHABET + [str(d) for d in range(10)]
GAMMA_BASE = ["_"] + SIGMA_BASE  # blank + symbols

def shift_letter(letter: str, k: int, encode: bool = True) -> str:
    if letter not in ALPHABET:
        return letter
    idx = ALPHABET.index(letter)
    if encode:
        new_idx = (idx + k) % ALPHABET_LEN
    else:
        new_idx = (idx - k) % ALPHABET_LEN
    return ALPHABET[new_idx]

def build_machine(encode: bool) -> dict:
    states = ["q0", "qMaybeTwo_1", "qMaybeTwo_2", "qAccept"]
    # Agregar qKey_k y qProc_k para k=0..26
    for k in range(ALPHABET_LEN + 1):  # 0..26
        states.append(f"qKey_{k}")
        states.append(f"qProc_{k}")

    transitions = []

    # Helper to add transition
    def add(state, read, next_state, write, move):
        transitions.append([state, [read], next_state, [write], [move]])

    # q0: primer símbolo (dígito o letra)
    # Dígitos '0'-'9'
    for d in range(10):
        if d in (1,2):
            # posible clave de dos dígitos
            add("q0", str(d), f"qMaybeTwo_{d}", str(d), "R")
        else:
            # clave de un dígito
            k = d
            add("q0", str(d), f"qKey_{k}", str(d), "R")

    # Letras A..Z
    for idx, letter in enumerate(ALPHABET):
        k = idx  # A=0, B=1,...
        add("q0", letter, f"qKey_{k}", letter, "R")

    # qMaybeTwo_1: '#' => k=1 o segundo dígito 10+d
    add("qMaybeTwo_1", "#", "qProc_1", "#", "R")
    for d in range(10):
        k = 10 + d
        if k <= 26:
            # keep second digit, move to wait for '#'
            add("qMaybeTwo_1", str(d), f"qKey_{k}", str(d), "R")
    # qMaybeTwo_2: '#' => k=2 o segundo dígito 0..6 formando 20..26
    add("qMaybeTwo_2", "#", "qProc_2", "#", "R")
    for d in range(7):  # 0..6
        k = 20 + d
        add("qMaybeTwo_2", str(d), f"qKey_{k}", str(d), "R")

    # qKey_k: expect '#'; when seen go to qProc_k
    for k in range(ALPHABET_LEN + 1):
        add(f"qKey_{k}", "#", f"qProc_{k}", "#", "R")

    # Procesamiento en qProc_k
    for k in range(ALPHABET_LEN + 1):
        proc = f"qProc_{k}"
        # Letras
        for letter in ALPHABET:
            out = shift_letter(letter, k % ALPHABET_LEN, encode)
            add(proc, letter, proc, out, "R")
        # Espacio y punto se copian
        add(proc, " ", proc, " ", "R")
        add(proc, ".", proc, ".", "R")
        # Dígitos: copiar si aparecen en el mensaje
        for d in range(10):
            add(proc, str(d), proc, str(d), "R")
        # En blanco => aceptar
        add(proc, "_", "qAccept", "_", "S")
        # Si aparece '#', conservar y continuar
        add(proc, "#", proc, "#", "R")

    machine = {
        "Q": states,
        "Sigma": SIGMA_BASE,
        "Gamma": GAMMA_BASE,
        "blank": "_",
        "q0": "q0",
        "F": ["qAccept"],
        "num_tapes": 1,
        "max_steps": 500000,
        "transitions": transitions,
    }
    return machine

def main():
    root = Path(__file__).parent
    ejemplos = root / "ejemplos"
    ejemplos.mkdir(exist_ok=True)
    enc = build_machine(encode=True)
    dec = build_machine(encode=False)
    (ejemplos / "mt_encoder.json").write_text(json.dumps(enc, ensure_ascii=False, indent=2), encoding="utf-8")
    (ejemplos / "mt_decoder.json").write_text(json.dumps(dec, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Máquinas generadas:")
    print(" - ejemplos/mt_encoder.json")
    print(" - ejemplos/mt_decoder.json")

if __name__ == "__main__":
    main()
