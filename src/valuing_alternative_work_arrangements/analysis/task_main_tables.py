import pandas as pd
import pytask
from valuing_alternative_work_arrangements.analysis.main_tables import (
    table_1,
    table_3,
    table_5,
)
from valuing_alternative_work_arrangements.config import (
    BLD,
    DUMMY_VARS,
    TABLE_3,
)


@pytask.mark.depends_on(BLD / "python" / "data" / "cpswss.pkl")
@pytask.mark.produces(BLD / "python" / "tables" / "table_1.pkl")
def task_create_table_1(depends_on, produces):
    """Replicate table 1 of Mas, Alexandre, and Amanda Pallais (2017).

    Args:
        depends_on (str): The cpswss data.
        produces (str): The folder path contains table 1.

    Returns:
    -------
        coef_df (pandas.DataFrame): Table 1.

    """
    df = pd.read_pickle(depends_on)
    coef_df = table_1(df)
    coef_df.to_pickle(produces)


@pytask.mark.depends_on(BLD / "python" / "data" / "cpswss.pkl")
@pytask.mark.produces(BLD / "python" / "tables" / "dummy_vars_cpswss.pkl")
def task_freq_dummy_vars(depends_on, produces):
    """Generate a summary table with frequency of dummy variables.

    Args:
        depends_on (str): The cpswss data.
        produces (str): The folder path contains the frequency table.

    Returns:
    -------
        freq_df (pandas.DataFrame): The table contains frequencies of dummy variables.

    """
    df = pd.read_pickle(depends_on)
    freq_df = pd.DataFrame()
    for var in DUMMY_VARS:
        freq_df = freq_df.append(df[var].value_counts().to_frame().T)
    freq_df.to_pickle(produces)


@pytask.mark.depends_on(
    {
        1: BLD / "python" / "data" / "experiment_all.pkl",
        2: BLD / "python" / "data" / "cpsmarch2016.pkl",
        3: BLD / "python" / "data" / "cpsmarch2016.pkl",
        4: BLD / "python" / "data" / "survey_wave1.pkl",
        5: BLD / "python" / "data" / "cpsmarch2016.pkl",
    },
)
@pytask.mark.produces(BLD / "python" / "tables" / "table_3.pkl")
def task_create_table_3(depends_on, produces):
    """Replicate each column of table 3 of Mas, Alexandre, and Amanda Pallais (2017).

    Args:
        depends_on (str): The experimentdata data.
        produces (str): The folder path contains the descriptive statistics table.

    Returns:
    -------
        stat_df (pandas.DataFrame): Table 3.

    """
    for col, data in TABLE_3.items():
        globals()[f"{data}"] = pd.read_pickle(depends_on[col])
        if col == 2:
            globals()[f"{data}"] = globals()[f"{data}"].loc[
                (globals()[f"{data}"]).callcenterworker == 1,
                :,
            ]
        elif col == 3:
            globals()[f"{data}"] = globals()[f"{data}"].loc[
                ((globals()[f"{data}"]).callcenterworker == 1)
                & ((globals()[f"{data}"]).any_city == 1),
                :,
            ]
        globals()[f"{data}"] = table_3(globals()[f"{data}"])

    name_list = []
    for name_df in TABLE_3.values():
        name_list.append(eval(name_df))
    stat_df = pd.concat(name_list, axis=1)
    stat_df.to_pickle(produces)


@pytask.mark.depends_on(BLD / "python" / "data" / "experimentdata.pkl")
@pytask.mark.produces(BLD / "python" / "tables" / "table_5.pkl")
def task_create_table_5(depends_on, produces):
    """Replicate table 5 of Mas, Alexandre, and Amanda Pallais (2017).

    Args:
        depends_on (str): The experimentdata data.
        produces (str): The folder path contains table 5.

    Returns:
    -------
        table5_wtp (pandas.DataFrame): Table 5.

    """
    df = pd.read_pickle(depends_on)
    table5_wtp = table_5(df)
    table5_wtp.to_pickle(produces)
