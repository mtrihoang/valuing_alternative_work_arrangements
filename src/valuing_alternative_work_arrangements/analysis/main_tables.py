import itertools
import random

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col
from valuing_alternative_work_arrangements.analysis.mle_programs import (
    mylogit_mle2,
)
from valuing_alternative_work_arrangements.config import (
    PREFIX,
)


def table_1(df):
    """Replicate table 1 of Mas, Alexandre, and Amanda Pallais (2017).

    Args:
        df (pandas.DataFrame): The cpswss data.

    Returns:
    -------
        coef_df (pandas.DataFrame): Contain estimates for compensating differentials from the observational data using weekly earnings.

    """
    prefix_var = [df.columns[df.columns.str.startswith(i)].tolist() for i in PREFIX]
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


def table_3(df):
    """Replicate table 3 of Mas, Alexandre, and Amanda Pallais (2017).

    Args:
        df (pandas.DataFrame): The experimentdata data.

    Returns:
    -------
        stat_df (pandas.DataFrame): Table 3.

    """
    prefix_var = [df.columns[df.columns.str.startswith(i)].tolist() for i in PREFIX]
    prefix_var = list(itertools.chain(*prefix_var))
    prefix_var = ["female", *prefix_var]
    stat_df = df[prefix_var].describe().T
    stat_df = round(stat_df[["mean"]] * 100)
    return stat_df


def table_5(df):
    """Replicate table 5 of Mas, Alexandre, and Amanda Pallais (2017).

    Args:
        df (pandas.DataFrame): The experimentdata data.

    Returns:
    -------
        wtp_df (pandas.DataFrame): Table 5.

    """
    reps = 5
    for t in [1, 4, 3, 5, 2]:
        globals()[f"bstrapresults{t}"] = pd.DataFrame(index=range(1), columns=range(6))
        globals()[f"bstrapresults{t}"].columns = [
            "treatment",
            "mean",
            "sd",
            "p25",
            "p50",
            "p75",
        ]
        globals()[f"pointestimates{t}"] = pd.DataFrame(index=range(1), columns=range(6))
        globals()[f"pointestimates{t}"].columns = [
            "treatment",
            "mean",
            "sd",
            "p25",
            "p50",
            "p75",
        ]
        random.seed(91857785)
        convergencecounter = 0
        expdata = df.loc[df.treatment_number == t, :]
        for j in list(range(1, reps + 1)):
            if convergencecounter < 500:
                runresults = pd.DataFrame(index=range(1), columns=range(6))
                runresults.columns = ["treatment", "mean", "sd", "p25", "p50", "p75"]
                runresults.iloc[0, 0] = t
                bsample = expdata.sample(frac=1, replace=True) if j != 1 else expdata
                bsample = bsample.reset_index()
                ml = mylogit_mle2(bsample)
                converged = ml.converged.mean()
                const = ml.const.mean()
                wagegap = ml.wagegap.mean()
                if converged is True:
                    runresults.iloc[0, 1] = -const / wagegap
                    runresults.iloc[0, 2] = -1 / (wagegap * 0.5516)
                    runresults.iloc[0, 3] = (
                        np.log(0.75 / (1 - 0.75)) - const
                    ) / wagegap
                    runresults.iloc[0, 4] = (np.log(0.5 / (1 - 0.5)) - const) / wagegap
                    runresults.iloc[0, 5] = (
                        np.log(0.25 / (1 - 0.25)) - const
                    ) / wagegap
                if j == 1:
                    globals()[f"pointestimates{t}"] = runresults
                else:
                    globals()[f"bstrapresults{t}"] = pd.concat(
                        [(globals()[f"bstrapresults{t}"]), runresults],
                    )
                convergencecounter += 1
    tablecode = pd.DataFrame(index=range(1), columns=range(6))
    tablecode.columns = ["treatment", "mean", "sd", "p25", "p50", "p75"]
    for t in [1, 4, 3, 5, 2]:
        globals()[f"se{t}"] = (
            globals()[f"bstrapresults{t}"]
            .groupby(["treatment"])["mean", "sd", "p25", "p50", "p75"]
            .agg("std")
        )
        tablecode = pd.concat(
            [tablecode, globals()[f"pointestimates{t}"], globals()[f"se{t}"]],
        )
    wtp_df = tablecode.dropna(subset=["mean", "sd", "p25", "p50", "p75"]).reset_index()
    return wtp_df
