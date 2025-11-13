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
    # cinta 1 = input_word; cinta 2 se inicializa en blanco
    tm.reset([input_word])
    tm.run(verbose=False)
    return tm.get_tape(tape_index=0, strip_blanks=True)


if __name__ == "__main__":
    # Pequeña prueba rápida:
    ejemplo = "3#ROMA NO FUE CONSTRUIDA EN UN DIA."
    salida = encrypt(ejemplo)
    print("Entrada :", ejemplo)
    print("Salida  :", salida)
