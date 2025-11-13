# maquina/turing.py

from dataclasses import dataclass
from typing import Dict, Tuple, List


# Claves y valores de la función de transición para k cintas
# key  = (estado, (s1, s2, ..., sk))
# val  = (estado_siguiente, (w1, w2, ..., wk), (m1, m2, ..., mk))

TransitionKey = Tuple[str, Tuple[str, ...]]
TransitionVal = Tuple[str, Tuple[str, ...], Tuple[str, ...]]


@dataclass
class TMConfig:
    states: List[str]
    input_alphabet: List[str]
    tape_alphabet: List[str]
    blank: str
    initial_state: str
    accept_states: List[str]
    transitions: Dict[TransitionKey, TransitionVal]
    num_tapes: int = 1
    max_steps: int = 100_000


class TuringMachine:
    """
    Máquina de Turing determinista de k cintas.

    - Cada cinta es una lista de símbolos.
    - Cada cinta tiene su propia cabeza de lectura/escritura.
    - Las transiciones están definidas sobre el estado actual
      y el k-tuple de símbolos leídos en cada cinta.
    """

    def __init__(self, config: TMConfig):
        self.config = config
        self.num_tapes = config.num_tapes
        self.reset([""])

    # ----------------- manejo de cinta y estado ----------------- #

    def reset(self, input_words: List[str]) -> None:
        """
        input_words: lista de strings, uno por cinta.
        - La cinta 1 recibirá el input real.
        - Las demás pueden empezar en blanco o con algún contenido dado.
        Si la lista es más corta que num_tapes, las cintas faltantes se
        inicializan con una sola celda en blanco.
        """
        tapes = []
        heads = []

        for i in range(self.num_tapes):
            if i < len(input_words) and input_words[i]:
                tapes.append(list(input_words[i]))
            else:
                tapes.append([self.config.blank])
            heads.append(0)

        self.tapes = tapes
        self.heads = heads
        self.current_state = self.config.initial_state
        self.halted = False
        self.steps = 0

    def _ensure_head_in_bounds(self, tape_index: int) -> None:
        """Asegura que la cabeza de la cinta i tenga una celda válida."""
        head = self.heads[tape_index]
        tape = self.tapes[tape_index]

        if head < 0:
            tape.insert(0, self.config.blank)
            self.heads[tape_index] = 0
        elif head >= len(tape):
            tape.append(self.config.blank)

    def _read_all(self) -> Tuple[str, ...]:
        """Lee el símbolo bajo la cabeza de cada cinta."""
        symbols = []
        for i in range(self.num_tapes):
            self._ensure_head_in_bounds(i)
            symbols.append(self.tapes[i][self.heads[i]])
        return tuple(symbols)

    def _write_all(self, write_symbols: Tuple[str, ...]) -> None:
        """Escribe en todas las cintas los símbolos dados."""
        for i in range(self.num_tapes):
            self._ensure_head_in_bounds(i)
            self.tapes[i][self.heads[i]] = write_symbols[i]

    def _move_all(self, moves: Tuple[str, ...]) -> None:
        """Mueve todas las cabezas según L, R o S."""
        for i in range(self.num_tapes):
            move = moves[i]
            if move == "L":
                self.heads[i] -= 1
            elif move == "R":
                self.heads[i] += 1
            elif move == "S":
                pass
            else:
                raise ValueError(f"Movimiento inválido en cinta {i}: {move}")

    # ----------------- ejecución ----------------- #

    def step(self) -> bool:
        """
        Ejecuta un paso de la MT.
        Devuelve False si ya no hay transición (la máquina se detiene).
        """
        if self.halted:
            return False

        if self.current_state in self.config.accept_states:
            self.halted = True
            return False

        read_symbols = self._read_all()
        key: TransitionKey = (self.current_state, read_symbols)

        if key not in self.config.transitions:
            # sin transición definida => halt
            self.halted = True
            return False

        next_state, write_symbols, moves = self.config.transitions[key]

        # escribir, cambiar estado, mover
        self._write_all(write_symbols)
        self.current_state = next_state
        self._move_all(moves)

        self.steps += 1
        if self.steps >= self.config.max_steps:
            self.halted = True

        return True

    def run(self, verbose: bool = False) -> None:
        """Corre la MT hasta que se detenga o se alcance max_steps."""
        while not self.halted:
            if verbose:
                self.print_configuration()
            if not self.step():
                break

    # ----------------- salida y debug ----------------- #

    def get_tape(self, tape_index: int = 0, strip_blanks: bool = True) -> str:
        """Retorna el contenido de una cinta como string."""
        tape = self.tapes[tape_index]
        s = "".join(tape)
        if strip_blanks:
            return s.strip(self.config.blank)
        return s

    def print_configuration(self) -> None:
        """Imprime una configuración instantánea simple."""
        print(f"Paso {self.steps} | Estado: {self.current_state}")
        for i in range(self.num_tapes):
            tape = self.tapes[i]
            head = self.heads[i]
            out = ""
            for j, sym in enumerate(tape):
                if j == head:
                    out += f"[{sym}]"
                else:
                    out += f" {sym} "
            print(f"  Cinta {i+1}: {out}")
        print("-" * 40)
