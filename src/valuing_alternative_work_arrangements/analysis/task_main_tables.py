import pandas as pd
import pytask
from valuing_alternative_work_arrangements.analysis.main_tables import (
    table_1,
)
from valuing_alternative_work_arrangements.config import (
    BLD,
    DUMMY_VARS,
)


@pytask.mark.depends_on(BLD / "python" / "data" / "cpswss.csv")
@pytask.mark.produces(BLD / "python" / "tables" / "table_1.csv")
def task_create_table_1(depends_on, produces):
    """Replicate table 1 of Mas, Alexandre, and Amanda Pallais (2017).

    Args:
        depends_on (str): The cpswss data.
        produces (str): The folder path contains table 1.

    Returns:
    -------
        coef_df (pandas.DataFrame): Table 1.

    """
    df = pd.read_csv(depends_on)
    coef_df = table_1(df)
    coef_df.to_csv(produces)


@pytask.mark.depends_on(BLD / "python" / "data" / "cpswss.csv")
@pytask.mark.produces(BLD / "python" / "tables" / "dummy_vars_cpswss.csv")
def task_freq_dummy_vars(depends_on, produces):
    """Generate a summary table with frequency of dummy variables.

    Args:
        depends_on (str): The cpswss data.
        produces (str): The folder path contains the frequency table.

    Returns:
    -------
        freq_df (pandas.DataFrame): The table contains frequencies of dummy variables.

    """
    df = pd.read_csv(depends_on)
    freq_df = pd.DataFrame()
    for var in DUMMY_VARS:
        freq_df = freq_df.append(df[var].value_counts().to_frame().T)
    freq_df.to_csv(produces)
