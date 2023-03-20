import pandas as pd
import pytask
from valuing_alternative_work_arrangements.analysis.main_tables import (
    table_1,
)
from valuing_alternative_work_arrangements.config import BLD


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
