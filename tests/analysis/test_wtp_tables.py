import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from valuing_alternative_work_arrangements.analysis.main_tables import (
    table_6,
    table_8,
)
from valuing_alternative_work_arrangements.config import BLD


@pytest.fixture()
def experimentdata():
    df = pd.read_pickle(
        BLD / "python" / "data" / "experimentdata.pkl",
    )
    return df


@pytest.fixture()
def treatment():
    treatment_numbers = [14, 26]
    return treatment_numbers


@pytest.fixture()
def error():
    err = 0.145
    return err


def test_table_6(experimentdata, treatment, error):
    df_got = table_6(experimentdata, treatment, error)
    df_expected = pd.DataFrame(
        [[6.00, 4.01], [0.88, 20.41]],
        columns=["WTP for 40 hour-per-week job", "Shadow value of time"],
        index=["20 hour-per-week job", "50 hour-per-week job"],
    )
    assert_frame_equal(df_got, df_expected)


@pytest.fixture()
def survey_wave1():
    df = pd.read_pickle(BLD / "python" / "data" / "survey_wave1.pkl")
    return df


@pytest.fixture()
def survey_wave2():
    df = pd.read_pickle(BLD / "python" / "data" / "survey_wave2.pkl")
    return df


def test_table_8(survey_wave1, survey_wave2):
    df1 = survey_wave1
    df1["wagegap_hasirregjob"] = df1["wagegap_irreg"] * df1["hasirregjob"]
    df1["wagegap_hasflexjob"] = df1["wagegap_flex"] * df1["hasflexjob"]
    df2 = survey_wave2
    df2["wagegap_haswfhjob"] = df2["wagegap_wfh"] * df2["haswfhjob"]
    df_logit_11 = table_8(
        df1,
        endog="chose_flex",
        exog=["wagegap_flex"],
        weight="wgt_flex",
        error=0.11363387,
    )
    df_logit_12 = table_8(
        df1,
        endog="chose_flex",
        exog=["wagegap_flex", "wagegap_hasflexjob", "hasflexjob"],
        weight="wgt_flex",
        error=0.11363387,
    )
    df_logit_21 = table_8(
        df2,
        endog="chose_wfh",
        exog=["wagegap_wfh"],
        weight="wgt_wfh",
        error=0.03205054,
    )
    df_logit_22 = table_8(
        df2,
        endog="chose_wfh",
        exog=["wagegap_wfh", "wagegap_haswfhjob", "haswfhjob"],
        weight="wgt_wfh",
        error=0.03205054,
    )
    df_logit_32 = table_8(
        df1,
        endog="chose_fixed",
        exog=["wagegap_irreg", "wagegap_hasirregjob", "hasirregjob"],
        weight="wgt_irreg",
        error=0.11363387,
    )
    llf_got = pd.array(
        [
            df_logit_11["llf"].mean(),
            df_logit_12["llf"].mean(),
            df_logit_21["llf"].mean(),
            df_logit_22["llf"].mean(),
            df_logit_32["llf"].mean(),
        ],
    )
    llf_got = llf_got.astype(float)
    llf_expected = pd.array([-953.12854, -944.75662, -978.73315, -886.88245, -884.9632])
    assert np.all(
        llf_got >= llf_expected,
    ), "The log-likelihood values at the optimum must be at least as good as the ones generated from authors' Stata do files"
