import chess
import enum
import subprocess
from subprocess import PIPE


class EvaluationKind(enum.Enum):
    CENTIPAWN = enum.auto()
    MATE = enum.auto()


class Evaluation:
    def __init__(self, kind: EvaluationKind, value: float | int) -> None:
        self.kind = kind
        self.value = value

    def __str__(self) -> str:
        if self.kind == "cp":
            assert isinstance(self.value, float)
            return str(self.value)
        else:
            assert isinstance(self.value, int)
            return f"mate in {self.value}"


class SearchKind(enum.Enum):
    DEPTH = enum.auto()
    TIME = enum.auto()


class Search:
    def __init__(self, kind: SearchKind, amount: int) -> None:
        self.kind = kind
        self.amount = amount


class Engine:
    def __init__(self, path: str, search: Search) -> None:
        self.engine = subprocess.Popen(path, stdin=PIPE, stdout=PIPE, text=True)
        self.search = search

    def load_board(self, board: chess.Board) -> None:
        assert self.engine.stdin is not None

        self.engine.stdin.write(f"position fen {board.fen()}\n")
        self.engine.stdin.flush()

    def get_best_move(self) -> chess.Move:
        assert self.engine.stdin is not None
        assert self.engine.stdout is not None

        match self.search.kind:
            case SearchKind.DEPTH:
                self.engine.stdin.write(f"go depth {self.search.amount}\n")
            case SearchKind.TIME:
                self.engine.stdin.write(f"go movetime {self.search.amount}\n")

        self.engine.stdin.flush()

        while True:
            line = self.engine.stdout.readline()
            print(line, end="")
            if line.startswith("bestmove"):
                return chess.Move.from_uci(line.split()[1])
