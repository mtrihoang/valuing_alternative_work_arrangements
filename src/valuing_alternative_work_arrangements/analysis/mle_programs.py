import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.special import expit


def me_correction(df):
    """Apply ME correction procedure in order to obtain the appropriate error rate.

    Args:
        df (pandas.DataFrame): The experimentdata data.

    Returns:
    -------
        mm1 (pandas.DataFrame): Contain appropriate error rate for mylogit_mle2.

    """
    mm1 = df.sort_values(["wagegap"])
    group_by_wagegap = mm1.groupby("wagegap")
    mm1["tag"] = (group_by_wagegap.cumcount() == 0).astype(int)
    mm1["mm1"] = group_by_wagegap["chose_position1"].transform("mean")
    mm1.loc[mm1["tag"] != 1, "mm1"] = 0
    temp_mm1 = mm1.loc[
        (mm1["tag"] == 1) & (mm1["wagegap"] <= -2),
    ]
    sd_mm1 = temp_mm1["mm1"].std()
    if sd_mm1 == 0:
        temp_mm2 = mm1.loc[
            (mm1["wagegap"] < 0) & (mm1["tag"] == 1),
        ]
        model = smf.glm(formula="mm1 ~ wagegap", data=temp_mm2)
        result = model.fit(cov_type="HC3")
    else:
        temp_mm2 = mm1.loc[
            (mm1["wagegap"] <= -2) & (mm1["tag"] == 1),
        ]
        model = smf.ols(formula="mm1 ~ wagegap", data=temp_mm2)
        result = model.fit(cov_type="HC3")
    ec_b = result.params[1]
    temp_mm1 = mm1.loc[(mm1["wagegap"] <= -2), :]
    temp_mm2["predict"] = result.predict(sm.add_constant(temp_mm1[["wagegap"]]))
    if ec_b <= 0:
        r_mean = temp_mm2.loc[temp_mm2["wagegap"] == -5, "predict"].mean()
        error = 1 - r_mean
    else:
        r_mean = temp_mm2.loc[temp_mm2["wagegap"] <= -2, "mm1"].mean()
        temp_mm2.loc[temp_mm2["wagegap"] <= -2, "predict"] = r_mean
        r_mean = temp_mm2.loc[temp_mm2["wagegap"] == -5, "predict"].mean()
        error = 1 - r_mean
    if error >= 0:
        mm1["mmf1"] = (mm1["mm1"] - error) / (1 - 2 * error)
        mm1["error"] = error
    else:
        mm1["mmf1"] = mm1["mm1"]
        mm1["error"] = 0
    return mm1


def mylogit_mle2(df):
    """Apply the maximum likelihood estimation method to estimate the parameters of the
    logistic regression model.

    Args:
        df (pandas.DataFrame): The experimentdata data.

    Returns:
    -------
        logit_fit_df (pandas.DataFrame): Contain estimates of the probability of choosing flexible schedule job.

    """
    df = df.dropna(subset=["wagegap", "chose_position1"])
    df = me_correction(df)
    y = df["chose_position1"]
    X = df[["wagegap"]]
    X = sm.add_constant(X)
    model = sm.Logit(y, X)
    result = model.fit(method="newton", cov_type="HC3", maxiter=100)
    lfit = result.predict(X, linear=True)
    prop_fit = expit(lfit)
    rev_wagegap = -X["wagegap"]
    logit_fit_df = pd.concat([rev_wagegap, prop_fit], axis=1)
    logit_fit_df = logit_fit_df.rename(columns={0: "lnf", "wagegap": "rev_wagegap"})
    logit_fit_df = logit_fit_df.sort_values("rev_wagegap")
    return logit_fit_df
