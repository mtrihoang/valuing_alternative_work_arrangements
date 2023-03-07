import itertools

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
    type = ["", "i.ind1990"]
    for cond in sample:
        df_ols = df if cond == "" else df.query(cond)
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
            dummy = ["C(year)", "C(region)"]
            for ind in type:
                if ind == "i.ind1990":
                    dummy.append("C(ind1990)")
                formula = "lnearn" + " ~ " + " + ".join(other_var + prefix_var + dummy)
                res = smf.wls(formula, data=df_ols, weights=df_ols.earnwt).fit()
                summary_col([res], stars=True).tables[0]
