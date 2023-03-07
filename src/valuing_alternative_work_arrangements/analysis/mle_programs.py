import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf


def me_correction(experimentdata):
    """Apply ME correction procedure in order to obtain the appropriate error rate.

    Args:
        df (pandas.DataFrame): The experimentdata data.

    Returns:
    -------
        table_1 (pandas.DataFrame): Contain estimates for compensating differentials from the observational data using weekly earnings.

    """
    mm1 = (
        experimentdata.groupby(["wagegap"])["chose_position1"]
        .agg(["mean"])
        .reset_index()
    )
    mm1["tag"] = 1
    mm1 = mm1.rename(columns={"mean": "mm1"})
    temp_mm1 = mm1.loc[
        (mm1["tag"] == 1) & (mm1["wagegap"] <= -2),
    ]
    sd_mm1 = temp_mm1["mm1"].std()
    if sd_mm1 == 0:
        temp_mm2 = mm1.loc[
            (mm1["tag"] == 1) & (mm1["wagegap"] < 0),
        ]
        model = smf.glm(
            formula="mm1 ~ wagegap",
            data=temp_mm2,
            family=sm.families.Binomial(),
        )
        result = model.fit()
    else:
        temp_mm2 = mm1.loc[
            (mm1["tag"] == 1) & (mm1["wagegap"] < -2),
        ]
        model = smf.ols(formula="mm1 ~ wagegap", data=temp_mm2)
        result = model.fit()
    ec_b = result.params[1]
    temp_mm2["predict"] = pd.DataFrame(result.predict())
    if ec_b <= 0:
        r_mean = temp_mm2.loc[temp_mm2["wagegap"] == -5, "predict"].mean()
    else:
        r_mean = temp_mm2.loc[temp_mm2["wagegap"] <= -2, "predict"].mean()
        temp_mm2.loc[temp_mm2["wagegap"] <= -2, "predict"] = r_mean
        r_mean = temp_mm2.loc[temp_mm2["wagegap"] == -5, "predict"].mean()
    error = 1 - r_mean
    if error > 0:
        mm1["mmf1"] = (mm1["mm1"] - error) / (1 - 2 * error)
    else:
        mm1["mmf1"] = mm1["mm1"]
    return mm1