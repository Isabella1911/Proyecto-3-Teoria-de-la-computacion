# maquina/decoder_mt.py

from pathlib import Path
from typing import Optional

from .turing import TuringMachine
from .parser import load_mt_from_json


def _get_project_root() -> Path:
    """
    Devuelve la ruta raíz del proyecto asumiendo que este archivo está en:
    .../Proyecto-3-Teoria-de-la-computacion/maquina/decoder_mt.py
    """
    return Path(__file__).resolve().parent.parent


def load_decoder_machine(json_path: Optional[str] = None) -> TuringMachine:
    """
    Carga la máquina de Turing de DECRIPTACIÓN (César -3).

    Si json_path es None, usa por defecto:
        <raiz_proyecto>/ejemplos/mt_decoder.json
    """
    root = _get_project_root()
    if json_path is None:
        mt_path = root / "ejemplos" / "mt_decoder.json"
    else:
        mt_path = Path(json_path)

    config = load_mt_from_json(str(mt_path))
    tm = TuringMachine(config)
    return tm


def decrypt(input_word: str, json_path: Optional[str] = None) -> str:
    """
    Decripta una cadena usando la MT de decriptación.

    input_word debe venir en el formato:
        "3#URPD QR IXH FRQVWUXLGD HQ XQ GLD."
    (o cualquier mensaje cifrado con César +3).

    Retorna la cinta 1 al finalizar la ejecución, sin blancos externos.
    """
    tm = load_decoder_machine(json_path)
    tm.reset([input_word])
    tm.run(verbose=False)
    return tm.get_tape(tape_index=0, strip_blanks=True)


if __name__ == "__main__":
    # Pequeña prueba rápida:
    ejemplo = "3#URPD QR IXH FRQVWUXLGD HQ XQ GLD."
    salida = decrypt(ejemplo)
    print("Entrada :", ejemplo)
    print("Salida  :", salida)
