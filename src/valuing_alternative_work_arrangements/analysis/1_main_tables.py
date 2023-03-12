import itertools

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col


def table_1(df):
    """Replicate table 1 of Mas, Alexandre, and Amanda Pallais (2017).

    Args:
        df (pandas.DataFrame): The cpswss data.

    Returns:
    -------
        table_1 (pandas.DataFrame): Contain estimates for compensating differentials from the observational data using weekly earnings.

    """
    prefix = ["race_", "ed_", "mar_"]
    prefix_var = [df.columns[df.columns.str.startswith(i)].tolist() for i in prefix]
    prefix_var = list(itertools.chain(*prefix_var))
    xvar = [
        "flexhrs",
        "workhome_dum",
        "workhome_paid",
        "irreg",
        "irreg_const",
        "irreg_inconst",
    ]
    sample = ["", "callcenterworker == 1", "hourly == 1"]
    dummy = ["C(year)", "C(region)"]
    type = ["", "i.ind1990"]
    coef_lst = []
    for cond in sample:
        df_ols = df if cond == "" else df.query(cond)
        for ind in type:
            if ind == "i.ind1990":
                dummy.append("C(ind1990)")
            for var in xvar:
                other_var = [
                    var,
                    "uhrswork1",
                    "emp_pt",
                    "female",
                    "age",
                    "selfemp",
                    "foreignborn",
                    "inornearmetro",
                ]
                formula = "lnearn" + " ~ " + " + ".join(other_var + prefix_var + dummy)
                res = smf.wls(formula, data=df_ols, weights=df_ols.earnwt).fit()
                coef_table = summary_col([res], stars=True).tables[0]
                coef_lst.append(coef_table.loc[var, :])
    coef_matrix = np.array(coef_lst).reshape(6, 6)
    coef_df = pd.DataFrame(coef_matrix)
    coef_df = coef_df.rename(
        index={
            0: "Can vary the times at which workday starts or ends",
            1: "Does any work from home",
            2: "Formal work from home arrangement",
            3: "Works an irregular schedule",
            4: "Works an irregular but consistent schedule",
            5: "Works an irregular, inconsistent schedule",
        },
    )
    coef_df = coef_df.rename(
        columns={
            0: "(All) No industry fixed effects",
            1: "(All) Industry fixed effects",
            2: "(Phone occupations) No industry fixed effects",
            3: "(Phone occupations) Industry fixed effects",
            4: "(All hourly workers) No industry fixed effects",
            5: "(All hourly workers) Industry fixed effects",
        },
    )
    return coef_df
