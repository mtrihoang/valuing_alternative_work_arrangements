# Valuing Alternative Work Arrangements | Effective Programming Practices for Economists | Winter Term 2022/23

by Minh Tri Hoang | Master of Science in Economics - University of Bonn

This is my final project on Effective Programming Practices for Economists. The course
was taught by [Dr. Janoś Gabler](https://janosg.com/) (University of Bonn).

This repository contains my replication for the following paper: Mas, Alexandre, and
Amanda Pallais. 2017.
[Valuing Alternative Work Arrangements](https://www.aeaweb.org/articles?id=10.1257/aer.20161500).
American Economic Review. 107 (12): 3722-59. It is my final project on

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/mtrihoang/valuing_alternative_work_arrangements/main.svg)](https://results.pre-commit.ci/latest/github/mtrihoang/valuing_alternative_work_arrangements/main)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Usage

In my final EPP project, I replicated main results of the original paper by Python. I
used [pytask](https://pytask-dev.readthedocs.io/en/stable/) to facilitate
reproducibility. Please follow the below instruction to set up my project and generate
datasets, figures, tables, and replication results.

To get started, please clone the repository with

```
git clone https://github.com/mtrihoang/valuing_alternative_work_arrangements.git
```

Then you need to create and activate the environment with

```
conda env create -f environment.yml
conda activate valuing_alternative_work_arrangements
```

Now, please install packages and dependencies used in my project via an editable mode by
using

```
pip install -e .
```

Finally, you can build the project by typing

```
pytask
```

## Folder Structure

My repository contains the following folders

- `src`

  - `src/valuing_alternative_work_arrangements/data_management`: contains Python scripts
    (`.py`) which are used to import original datasets (`.dta`) from Dropbox and clean
    these datasets.
  - `src/valuing_alternative_work_arrangements/analysis`: contains Python scripts to
    replicate main tables in the original paper. Those scripts include crucial functions
    to simulate the breakpoint model and conduct Monte-Carlo simulations associated with
    logistic regressions (with custom likelihood functions).
  - `src/valuing_alternative_work_arrangements/final`: contains a Python script to
    generate main figures of the paper. The script has several dependencies in the
    `analysis` subfolder.

- `test`: contains Python scripts which provide some unit tests for important functions
  in my project. The tests focus on

  - Verifying results of logistic regression models using error-corrected maximum
    likelihood.
  - Making a performance comparison between MLE algorithms used in Stata and Python,
    verified through log-likelihood values.

- `paper`: contains my `.tex` source code which generates a report to make a summary of
  the paper.

- `bld`: generated by running `pytask`. The subfolder contains all replication outputs
  (tables, figures, and papers). The below tree shows the structure of the output
  folder.

```
bld/
├── latex/
│   ├── alternative_work_arrangements.aux
│   ├── alternative_work_arrangements.bbl
│   ├── alternative_work_arrangements.blg
│   ├── alternative_work_arrangements.fdb_latexmk
│   ├── alternative_work_arrangements.fls
│   ├── alternative_work_arrangements.log
│   ├── alternative_work_arrangements.pdf
│   ├── alternative_work_arrangements.synctex.gz
│   └── alternative_work_arrangements.toc
└── python/
    ├── data/
    │   ├── cps_march2016.pkl
    │   ├── cps_wss.pkl
    │   ├── cpswss.pkl
    │   ├── experiment_age.pkl
    │   ├── experiment_all.pkl
    │   ├── experiment_education.pkl
    │   ├── experiment_employmentstatus.pkl
    │   ├── experiment_race.pkl
    │   ├── experimentdata.pkl
    │   ├── survey_wave1.pkl
    │   └── survey_wave2.pkl
    ├── figures/
    │   ├── fig_1_error_corrected_logit.png
    │   ├── fig_1_standard_logit.png
    │   ├── fig_2_error_corrected_logit.png
    │   ├── fig_2_standard_logit.png
    │   ├── fig_3_error_corrected_logit.png
    │   ├── fig_3_standard_logit.png
    │   ├── fig_4_error_corrected_logit.png
    │   ├── fig_4_standard_logit.png
    │   ├── fig_5_error_corrected_logit.png
    │   └── fig_5_standard_logit.png
    └── tables/
        ├── dummy_vars_cpswss.pkl
        ├── table_1.pkl
        ├── table_3.pkl
        ├── table_5.pkl
        ├── table_6.pkl
        ├── table_7.pkl
        └── table_8.pkl
```

## Information about Replication and Transparency

The original data and Stata do files used in the paper can be accessed
[here](https://www.aeaweb.org/articles?id=10.1257/aer.20161500).

For the replication, I try to remain the original structure of Stata programs so that
readers can easily follow and compare. In particular, Python functions and classes are
named almost the same as Stata programs in authors' do files. All figures are labelled
as those in the paper.

The below tables shows Stata to Python equivalents.

| Stata                   | Python                                              |
| ----------------------- | --------------------------------------------------- |
| `1_main_tables.do`      | `main_tables.py` + `task_main_tables.py`            |
| `2_figures.do`          | `task_fig_setup.py`                                 |
| `mle_programs.do`       | `mle_programs.py`                                   |
| `breakpoint_program.do` | `breakpoint_program.py`                             |
| program `fig_setup`     | function `fig_setup()`                              |
| program `breakval_figs` | function `breakval_figs()`                          |
| program `me_correction` | function `me_correction()`                          |
| program `mylogit_mle1`  | function `test_mylogit_mle1()`                      |
| program `mylogit_mle2`  | class `Newlikelihood()` + function `mylogit_mle2()` |

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
econ-project-templates\](https://github.com/OpenSourceEconomics/econ-project-templates).
