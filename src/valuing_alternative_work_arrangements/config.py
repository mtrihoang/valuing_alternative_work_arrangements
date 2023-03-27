"""This module contains the general configuration of the project."""
from pathlib import Path

SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()

TEST_DIR = SRC.joinpath("..", "..", "tests").resolve()
PAPER_DIR = SRC.joinpath("..", "..", "paper").resolve()

TASK_FIGURES = [1, 4, 3, 5, 2]

PREFIX = ["emp_", "age_", "ed_", "race_"]

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

DATA_FILES = [
    "cps_march2016",
    "cps_wss",
    "experiment_age",
    "experiment_education",
    "experiment_employmentstatus",
    "experiment_race",
    "experimentdata",
    "survey_wave1",
    "survey_wave2",
]

DROPBOX_URL = [
    "https://www.dropbox.com/s/ri1mq4859sngizx/cps_march2016.dta?dl=1",
    "https://www.dropbox.com/s/8r70kj4qxda61vh/cps_wss.dta?dl=1",
    "https://www.dropbox.com/s/kiqu9ti8cj7nrgq/experiment_age.dta?dl=1",
    "https://www.dropbox.com/s/0wvxtshpx60c862/experiment_education.dta?dl=1",
    "https://www.dropbox.com/s/8u2kwr5wyjzn8i6/experiment_employmentstatus.dta?dl=1",
    "https://www.dropbox.com/s/lryhd5u4991w4zn/experiment_race.dta?dl=1",
    "https://www.dropbox.com/s/x9un4pkhd57vdei/experimentdata.dta?dl=1",
    "https://www.dropbox.com/s/wyei613o0m09s16/survey_wave1.dta?dl=1",
    "https://www.dropbox.com/s/26ymj2ek3mvmty6/survey_wave2.dta?dl=1",
]

EXPERIMENTAL_DATA = [
    "experimentdata",
    "experiment_age",
    "experiment_education",
    "experiment_employmentstatus",
    "experiment_race",
]

TABLE_3 = {
    1: "experiment_all",
    2: "cpsmarch2016_1",
    3: "cpsmarch2016_2",
    4: "survey_wave1",
    5: "cpsmarch2016",
}

TABLE_5 = [1, 4, 3, 5, 2]

TABLE_6 = [14, 26]

TABLE_7 = [8, 11, 10, 12, 13]

__all__ = [
    "BLD",
    "SRC",
    "TEST_DIR",
    "PAPER_DIR",
    "TASK_FIGURES",
    "PREFIX",
    "DUMMY_VARS",
    "DATA_FILES",
    "DROPBOX_URL",
    "EXPERIMENTAL_DATA",
]
