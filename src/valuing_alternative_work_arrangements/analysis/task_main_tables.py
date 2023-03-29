import pandas as pd
import pytask
from valuing_alternative_work_arrangements.analysis.main_tables import (
    table_1,
    table_3,
    table_5_and_7,
    table_6,
    table_8,
)
from valuing_alternative_work_arrangements.config import (
    BLD,
    DUMMY_VARS,
    TABLE_3,
    TABLE_5,
    TABLE_6,
    TABLE_7,
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
    stat_df = stat_df.drop(labels="age_")
    stat_df.columns = [
        "Experiment main treatments",
        "CPSphone occupations",
        "CPS phone occupations in cities",
        "UAS",
        "CPS all",
    ]
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
        table_5_wtp (pandas.DataFrame): Table 5.

    """
    df = pd.read_pickle(depends_on)
    table_5_wtp = table_5_and_7(df, TABLE_5)
    table_5_wtp.to_pickle(produces)


@pytask.mark.depends_on(BLD / "python" / "data" / "experimentdata.pkl")
@pytask.mark.produces(BLD / "python" / "tables" / "table_6.pkl")
def task_create_table_6(depends_on, produces):
    """Replicate table 6 of Mas, Alexandre, and Amanda Pallais (2017).

    Args:
        depends_on (str): The experimentdata data.
        produces (str): The folder path contains table 6.

    Returns:
    -------
        table_6_wtp (pandas.DataFrame): Table 6.

    """
    df = pd.read_pickle(depends_on)
    table_6_wtp = table_6(df, TABLE_6, 0.145)
    table_6_wtp.to_pickle(produces)


@pytask.mark.depends_on(BLD / "python" / "data" / "experimentdata.pkl")
@pytask.mark.produces(BLD / "python" / "tables" / "table_7.pkl")
def task_create_table_7(depends_on, produces):
    """Replicate table 7 of Mas, Alexandre, and Amanda Pallais (2017).

    Args:
        depends_on (str): The experimentdata data.
        produces (str): The folder path contains table 7.

    Returns:
    -------
        table_7_wtp (pandas.DataFrame): Table 7.

    """
    df = pd.read_pickle(depends_on)
    table_7_wtp = table_5_and_7(df, TABLE_7)
    table_7_wtp.to_pickle(produces)


@pytask.mark.depends_on(
    {
        1: BLD / "python" / "data" / "survey_wave1.pkl",
        2: BLD / "python" / "data" / "survey_wave2.pkl",
    },
)
@pytask.mark.produces(BLD / "python" / "tables" / "table_8.pkl")
def task_create_table_8(depends_on, produces):
    """Replicate each column of table 8 of Mas, Alexandre, and Amanda Pallais (2017).

    Args:
        depends_on (str): The survey data.
        produces (str): The folder path contains table 8.

    Returns:
    -------
        table_8_wtp (pandas.DataFrame): Table 8.

    """
    df1 = pd.read_pickle(depends_on[1])

    df1["wagegap_hasirregjob"] = df1["wagegap_irreg"] * df1["hasirregjob"]
    df1["wagegap_hasflexjob"] = df1["wagegap_flex"] * df1["hasflexjob"]

    df_logit_11 = table_8(
        df1,
        endog="chose_flex",
        exog=["wagegap_flex"],
        weight="wgt_flex",
        error=0.11363387,
    )
    c11 = -df_logit_11["const"] / df_logit_11["wagegap_flex"]

    df_logit_12 = table_8(
        df1,
        endog="chose_flex",
        exog=["wagegap_flex", "wagegap_hasflexjob", "hasflexjob"],
        weight="wgt_flex",
        error=0.11363387,
    )
    c13 = -df_logit_12["const"] / df_logit_12["wagegap_flex"]
    c12 = -(df_logit_12["const"] + df_logit_12["hasflexjob"]) / (
        df_logit_12["wagegap_flex"] + df_logit_12["wagegap_hasflexjob"]
    )
    c14 = c13 - c12

    df_logit_31 = table_8(
        df1,
        endog="chose_fixed",
        exog=["wagegap_irreg"],
        weight="wgt_irreg",
        error=0.11363387,
    )
    c31 = -df_logit_31["const"] / df_logit_31["wagegap_irreg"]

    df_logit_32 = table_8(
        df1,
        endog="chose_fixed",
        exog=["wagegap_irreg", "wagegap_hasirregjob", "hasirregjob"],
        weight="wgt_irreg",
        error=0.11363387,
    )
    c33 = -df_logit_32["const"] / df_logit_32["wagegap_irreg"]
    c32 = -(df_logit_32["const"] + df_logit_32["hasirregjob"]) / (
        df_logit_32["wagegap_irreg"] + df_logit_32["wagegap_hasirregjob"]
    )
    c34 = c33 - c32

    df2 = pd.read_pickle(depends_on[2])

    df2["wagegap_haswfhjob"] = df2["wagegap_wfh"] * df2["haswfhjob"]

    df_logit_21 = table_8(
        df2,
        endog="chose_wfh",
        exog=["wagegap_wfh"],
        weight="wgt_wfh",
        error=0.03205054,
    )
    c21 = -df_logit_21["const"] / df_logit_21["wagegap_wfh"]

    df_logit_22 = table_8(
        df2,
        endog="chose_wfh",
        exog=["wagegap_wfh", "wagegap_haswfhjob", "haswfhjob"],
        weight="wgt_wfh",
        error=0.03205054,
    )
    c23 = -df_logit_22["const"] / df_logit_22["wagegap_wfh"]
    c22 = -(df_logit_22["const"] + df_logit_22["haswfhjob"]) / (
        df_logit_22["wagegap_wfh"] + df_logit_22["wagegap_haswfhjob"]
    )
    c24 = c22 - c23

    wtp_df = [[c11, c12, c13, c14], [c21, c22, c23, c24], [c31, c32, c33, c34]]
    index = [
        "Panel A. Mean WTP for flexible schedule",
        "Panel B. Mean WTP for work from home",
        "Panel C. Mean WTP to avoid employer discretion",
    ]
    columns = [
        "All",
        "In flexible schedule job",
        "Not in flexible schedule job",
        "Difference",
    ]
    wtp_df = pd.DataFrame(wtp_df, index=index, columns=columns).astype(float)
    table_8_wtp = wtp_df.round(1)
    table_8_wtp.to_pickle(produces)
