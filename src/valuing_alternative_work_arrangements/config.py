"""This module contains the general configuration of the project."""
from pathlib import Path

SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()

TEST_DIR = SRC.joinpath("..", "..", "tests").resolve()
PAPER_DIR = SRC.joinpath("..", "..", "paper").resolve()

TASK_FIGURES_1 = [1, 4, 3, 5, 2]

TASK_FIGURES_2 = ["1a", "4a", "3a", "5a", "2a"]

__all__ = ["BLD", "SRC", "TEST_DIR", "GROUPS"]
