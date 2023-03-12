import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from valuing_alternative_work_arrangements.analysis.mle_programs import (
    me_correction,
)


def breakval_figs(df):
    """Search for the optimal breakpoint.

    Args:
        experimentdata (pandas.DataFrame): The experimentdata data.

    Returns:
    -------
        df (pandas.DataFrame): Contain breakpoint predicted values.

    """
    df = df.groupby(["wagegap"])["chose_position1"].agg(["mean"]).reset_index()
    df["tag"] = 1
    df = df.rename(columns={"mean": "chose_position1"})
    mm1 = me_correction(df)
    mm1["mmk1"] = mm1["mmf1"] - 1
    rmse = []
    K = [
        -5,
        -4,
        -3,
        -2.75,
        -2.5,
        -2.25,
        -2,
        -1.75,
        -1.5,
        -1.25,
        -1,
        -0.75,
        -0.5,
        -0.25,
        0,
        0.25,
        0.5,
        0.75,
        1,
        1.25,
        1.5,
        1.75,
        2,
    ]
    for k in K:
        mm2 = mm1.loc[mm1["wagegap"] >= k, :]
        model = smf.glm(formula="mmf1 ~ wagegap", data=mm2)
        result = model.fit(cov_type="HC3")
        mm2["pf"] = result.predict()
        mm3 = mm2[["wagegap", "pf"]]
        mm4 = pd.merge(mm1, mm3, how="left", on="wagegap")
        mm4.loc[mm4["wagegap"] < k, "pf"] = 1
        h = mm4.loc[mm4["wagegap"] == k, "pf"].mean()
        b = result.params[1]
        if b > 0:
            mm4.loc[mm4["wagegap"] >= k, "pf"] = h
        rmse_k = np.sqrt(((mm4["mmf1"] - mm4["pf"]) ** 2).mean())
        rmse.append(rmse_k)
    rmse_dict = {"k": pd.Series(K), "rmse": pd.Series(rmse)}
    rmse_df = pd.DataFrame(rmse_dict)
    track = rmse_df[["rmse"]].idxmin()
    break_val = rmse_df.iloc[track].iloc[0, 0]
    mm5 = mm1.loc[mm1["wagegap"] >= break_val, :]
    model = smf.glm(formula="mmf1 ~ wagegap", data=mm5, family=sm.families.Binomial())
    result = model.fit(cov_type="HC3")
    mm5["pg"] = result.predict()
    mm6 = mm5[["wagegap", "pg"]]
    df = pd.merge(mm1, mm6, how="left", on="wagegap")
    df.loc[df["wagegap"] < break_val, "pg"] = 1
    h = df.loc[df["wagegap"] == break_val, "pg"].mean()
    result.params[0]
    b = result.params[1]
    if b > 0:
        df.loc[df["wagegap"] >= break_val, "pg"] = h
    df["rev_wagegap"] = -df["wagegap"]
    df = df.sort_values("rev_wagegap")
    return df
