# maquina/encoder_mt.py

from pathlib import Path
from typing import Optional

from .turing import TuringMachine
from .parser import load_mt_from_json


def _get_project_root() -> Path:
    """
    Devuelve la ruta raíz del proyecto asumiendo que este archivo está en:
    .../Proyecto-3-Teoria-de-la-computacion/maquina/encoder_mt.py
    """
    return Path(__file__).resolve().parent.parent


def load_encoder_machine(json_path: Optional[str] = None) -> TuringMachine:
    """
    Carga la máquina de Turing de ENCRIPTACIÓN (César +3).

    Si json_path es None, usa por defecto:
        <raiz_proyecto>/ejemplos/mt_encoder.json
    """
    root = _get_project_root()
    if json_path is None:
        mt_path = root / "ejemplos" / "mt_encoder.json"
    else:
        mt_path = Path(json_path)

    config = load_mt_from_json(str(mt_path))
    tm = TuringMachine(config)
    return tm


def encrypt(input_word: str, json_path: Optional[str] = None) -> str:
    """
    Encripta una cadena usando la MT de encriptación.

    input_word debe venir en el formato:
        "3#ROMA NO FUE CONSTRUIDA EN UN DIA."
    (o el mensaje que quieras en mayúsculas).

    Retorna la cinta 1 al finalizar la ejecución, sin blancos externos.
    """
    tm = load_encoder_machine(json_path)
    tm.reset([input_word])
    tm.run(verbose=False)
    raw = tm.get_tape(tape_index=0, strip_blanks=True)
    # Si la salida conserva la llave, removerla para entregar solo el mensaje cifrado
    if '#' in raw:
        parts = raw.split('#', 1)
        if len(parts) == 2:
            return parts[1]
    return raw


def encrypt_with_trace(input_word: str, json_path: Optional[str] = None, max_steps: int = 10_000) -> tuple[str, list]:
    """Encripta la cadena y devuelve (salida, trazado_de_cinta).

    El trazado es una lista de diccionarios con:
      step: número de paso
      state: estado actual
      head: posición de la cabeza
      tape: representación de la cinta con símbolo bajo cabeza entre corchetes

    max_steps limita la captura para evitar explosión de memoria en entradas grandes.
    """
    tm = load_encoder_machine(json_path)
    tm.reset([input_word])
    trace = []

    def snapshot(step: int):
        head = tm.heads[0]
        tape_list = tm.tapes[0][:]
        rendered = "".join(
            f"[{c}]" if i == head else c for i, c in enumerate(tape_list)
        )
        trace.append({
            "step": step,
            "state": tm.current_state,
            "head": head,
            "tape": rendered
        })

    snapshot(0)
    while not tm.halted and tm.steps < max_steps:
        if not tm.step():
            break
        snapshot(tm.steps)

    raw = tm.get_tape(tape_index=0, strip_blanks=True)
    if '#' in raw:
        parts = raw.split('#', 1)
        if len(parts) == 2:
            return parts[1], trace
    return raw, trace


if __name__ == "__main__":
    # Pequeña prueba rápida:
    ejemplo = "3#ROMA NO FUE CONSTRUIDA EN UN DIA."
    salida = encrypt(ejemplo)
    print("Entrada :", ejemplo)
    print("Salida  :", salida)
