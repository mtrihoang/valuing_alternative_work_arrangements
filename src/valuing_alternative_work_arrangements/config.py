"""This module contains the general configuration of the project."""
from pathlib import Path

SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()

TEST_DIR = SRC.joinpath("..", "..", "tests").resolve()
PAPER_DIR = SRC.joinpath("..", "..", "paper").resolve()

TASK_FIGURES = [1, 4, 3, 5, 2]

DUMMY_VARS = [
    "emp_pt",
    "female",
    "emp_emp",
    "callcenterworker",
    "selfemp",
    "foreignborn",
    "race_hisp",
    "race_black",
    "race_white",
    "race_natamer",
    "race_asian",
    "race_pacisl",
    "race_multirace",
    "mar_spouse",
    "mar_nospouse",
    "mar_separated",
    "mar_divorced",
    "mar_widowed",
    "mar_nevermar",
    "ed_lessthanhs",
    "ed_highschool",
    "ed_somecollege",
    "ed_assocdeg",
    "ed_bachdeg",
    "ed_advanceddeg",
    "inornearmetro",
    "hourly",
    "workhome_dum",
    "workhome_paid",
    "inschedsample",
    "irreg_const",
    "eveningshift",
    "nightshift",
    "rotatingshift",
    "splitshift",
    "irreg_byemp",
    "irreg_someother",
    "irreg_inconst",
    "irreg",
]

__all__ = ["BLD", "SRC", "TEST_DIR", "GROUPS"]
