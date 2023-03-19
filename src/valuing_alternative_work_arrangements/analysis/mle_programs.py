import numpy as np
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
        mm1 (pandas.DataFrame): The appropriate error rate for mylogit.

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


def mylogit(df):
    """Apply the maximum likelihood estimation method to estimate the parameters of the
    (standard) logistic regression model.

    Args:
        df (pandas.DataFrame): The experimentdata data.

    Returns:
    -------
        logit_fit_df (pandas.DataFrame): Estimates for the probability of choosing flexible schedule job.

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


class CustomLogit(sm.Logit):
    """Define likelihood functions for error-corrected maximum likelihood logit model,
    following Mas, Alexandre, and Amanda Pallais (2017).

    Attributes:
        error (pandas.Series): The correction error generated by function me_correction().
        loglike (float):

    """

    def __init__(self, endog, exog, error):
        """Initialize parameters of (log) likelihood function for error-corrected
        maximum likelihood logit model.

        Args:
            error (pandas.Series): The error generated by function me_correction().

        """
        super().__init__(endog, exog)
        self.error = error

    def loglike(self, params):
        """Estimate the log likelihood function associated with the error-corrected
        maximum likelihood logit model.

        Args:
            params (pandas.Series): The logit coefficients generated from sm.Logit().

        Returns:
        -------
            llf (float): The value of the log likelihood function.

        """
        lin_pred = self.exog.dot(params)
        llf = self.endog
        llf[self.endog == 1] = np.log(
            expit(lin_pred[self.endog == 1]) * (1 - self.error[self.endog == 1])
            + (1 - expit(lin_pred[self.endog == 1])) * self.error[self.endog == 1],
        )
        llf[self.endog == 0] = np.log(
            expit(lin_pred[self.endog == 0]) * (self.error[self.endog == 0])
            + (1 - expit(lin_pred[self.endog == 0]))
            * (1 - self.error[self.endog == 0]),
        )
        llf = np.sum(llf)
        return llf


def mylogit_mle2(df):
    """Apply the maximum likelihood estimation method to estimate the parameters of the
    (error-corrected) logistic regression model.

    Args:
        df (pandas.DataFrame): The experimentdata data.

    Returns:
    -------
        logit_fit_df (pandas.DataFrame): Estimates for the probability of choosing flexible schedule job.

    """
    df = df.dropna(subset=["wagegap", "chose_position1"])
    df = me_correction(df)
    error = df["error"]
    y = df["chose_position1"]
    X = df[["wagegap"]]
    X = sm.add_constant(X)
    model = CustomLogit(endog=y, exog=X, error=error)
    result = model.fit(method="newton", cov_type="HC3", maxiter=100)
    lfit = result.predict(X, linear=True)
    prop_fit_temp = expit(lfit)
    prop_fit = (prop_fit_temp - error) / (1 - 2 * error)
    prop_fit[(prop_fit < 0)] = 0
    prop_fit[(prop_fit > 1)] = 1
    rev_wagegap = -X["wagegap"]
    logit_fit_df = pd.concat([rev_wagegap, prop_fit], axis=1)
    logit_fit_df = logit_fit_df.rename(columns={"wagegap": "rev_wagegap", 0: "lnf"})
    logit_fit_df = logit_fit_df.sort_values("rev_wagegap")
    logit_fit_df["llf"] = result.llf
    logit_fit_df["error"] = error
    return logit_fit_df
