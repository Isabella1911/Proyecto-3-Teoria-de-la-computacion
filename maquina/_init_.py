# maquina/__init__.py

from .turing import TuringMachine
from .parser import load_mt_from_json

__all__ = ["TuringMachine", "load_mt_from_json"]
