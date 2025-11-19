"""Generador de máquinas de Turing para cifrado César (encoder/decoder).

Produce dos archivos JSON:
  ejemplos/mt_encoder.json
  ejemplos/mt_decoder.json

Características:
 - Una sola cinta.
 - Formato input: KEY#MENSAJE (KEY puede ser dígito 0..26 o letra A..Z)
 - Se soportan llaves numéricas de 0 a 26 (0 => sin desplazamiento, 26 => identidad).
 - Llaves con dos dígitos (10-26) se reconocen.
 - Llaves en forma de letra: índice en alfabeto (A=0, B=1, ..., Z=25).
 - Solo se cifran letras del alfabeto; espacio y punto se copian sin modificación.

Restricciones / Suposiciones:
 - Si aparece un patrón numérico inválido (p.e. segundo dígito fuera de rango para 2X > 26), la máquina se detendrá (sin transición) conservando el texto original.
 - No se realiza validación exhaustiva de formatos erróneos más allá de lo necesario para el proyecto.

Diseño de estados principales:
  q0               : lee primer símbolo (key start)
  qMaybeTwo_1      : posible clave de dos dígitos iniciando en '1'
  qMaybeTwo_2      : posible clave de dos dígitos iniciando en '2'
  qKey_k           : estado después de conocer la clave k, esperando '#'
  qProc_k          : procesa el mensaje aplicando el desplazamiento k
  qAccept          : estado final

Para cada k en 0..26 se crean qKey_k y qProc_k.

Nota: Esta construcción genera un número grande de transiciones pero permite
mantener la lógica dentro del modelo MT sin cálculos externos.
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
    # Add qKey_k and qProc_k for k in 0..27
    for k in range(ALPHABET_LEN + 1):  # 0..27
        states.append(f"qKey_{k}")
        states.append(f"qProc_{k}")

    transitions = []

    # Helper to add transition
    def add(state, read, next_state, write, move):
        transitions.append([state, [read], next_state, [write], [move]])

    # q0: first symbol determines path (digit or letter)
    # Digits '0'-'9'
    for d in range(10):
        if d in (1,2):
            # could be two-digit key
            add("q0", str(d), f"qMaybeTwo_{d}", str(d), "R")
        else:
            # single digit key
            k = d
            add("q0", str(d), f"qKey_{k}", str(d), "R")

    # Letters A..Z, Ñ
    for idx, letter in enumerate(ALPHABET):
        k = idx  # A=0, B=1,...
        add("q0", letter, f"qKey_{k}", letter, "R")

    # qMaybeTwo_1: either '#'(=> key=1) or second digit forming 10+d
    add("qMaybeTwo_1", "#", "qProc_1", "#", "R")
    for d in range(10):
        k = 10 + d
        if k <= 27:
            # keep second digit, move to wait for '#'
            add("qMaybeTwo_1", str(d), f"qKey_{k}", str(d), "R")
    # qMaybeTwo_2: '#' => key=2 or second digit 0..6 forming 20..26
    add("qMaybeTwo_2", "#", "qProc_2", "#", "R")
    for d in range(7):  # 0..6
        k = 20 + d
        add("qMaybeTwo_2", str(d), f"qKey_{k}", str(d), "R")

    # qKey_k: expect '#'; when seen go to qProc_k
    for k in range(ALPHABET_LEN + 1):
        add(f"qKey_{k}", "#", f"qProc_{k}", "#", "R")

    # Processing states qProc_k
    for k in range(ALPHABET_LEN + 1):
        proc = f"qProc_{k}"
        # Letters
        for letter in ALPHABET:
            out = shift_letter(letter, k % ALPHABET_LEN, encode)
            add(proc, letter, proc, out, "R")
        # Space and period remain
        add(proc, " ", proc, " ", "R")
        add(proc, ".", proc, ".", "R")
        # Digits (copy unchanged if appear in message)
        for d in range(10):
            add(proc, str(d), proc, str(d), "R")
        # On blank -> accept
        add(proc, "_", "qAccept", "_", "S")
        # '#' inside message (unlikely) keep and continue
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
