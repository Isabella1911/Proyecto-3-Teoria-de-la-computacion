# main_encoder.py

import sys
from pathlib import Path

from maquina.encoder_mt import encrypt


def main():
    base = Path(__file__).parent

    if len(sys.argv) >= 2:
        input_word = sys.argv[1]
    else:
        input_file = base / "ejemplos" / "input_encoder.txt"
        if input_file.exists():
            input_word = input_file.read_text(encoding="utf-8").strip()
        else:
            input_word = "3#ROMA NO FUE CONSTRUIDA EN UN DIA."

    print(f"[ENCRIPTAR] Entrada: {input_word}")
    output = encrypt(input_word)
    print(f"[ENCRIPTAR] Salida: {output}")

    output_dir = base / "output"
    output_dir.mkdir(exist_ok=True)
    out_file = output_dir / "encoder_output.txt"
    out_file.write_text(output, encoding="utf-8")
    print(f"Salida guardada en: {out_file}")


if __name__ == "__main__":
    main()
