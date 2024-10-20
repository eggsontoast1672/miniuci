import subprocess
from subprocess import PIPE
from typing import Literal


class Evaluation:
    Kind = Literal["cp", "mate"]

    def __init__(self, kind: Kind, value: float | int) -> None:
        self.kind = kind
        self.value = value

    def __str__(self) -> str:
        if self.kind == "cp":
            assert isinstance(self.value, float)
            return str(self.value)
        else:
            assert isinstance(self.value, int)
            return f"mate in {self.value}"


class Engine:
    def __init__(self, path: str, search_time_millis: int) -> None:
        self.engine = subprocess.Popen(path, stdin=PIPE, stdout=PIPE, text=True)
        self.search_time_millis = search_time_millis

    def load_position(self, fen: str) -> None:
        assert self.engine.stdin is not None

        self.engine.stdin.write(f"position fen {fen}\n")
        self.engine.stdin.flush()

    def get_best_move(self) -> str:
        # TODO: Return an evaluation

        assert self.engine.stdin is not None
        assert self.engine.stdout is not None

        # self.engine.stdin.write(f"go movetime {self.search_time_millis}\n")
        self.engine.stdin.write(f"go depth 18\n")
        self.engine.stdin.flush()

        while True:
            line = self.engine.stdout.readline()
            print(line, end="")
            if line.startswith("bestmove"):
                return line.split()[1]
