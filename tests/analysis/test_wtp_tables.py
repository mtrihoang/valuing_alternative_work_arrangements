import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from valuing_alternative_work_arrangements.analysis.main_tables import (
    table_6,
    table_8,
)


@pytest.fixture()
def mock_table_6():
    np.random.seed(31032023)
    chose_position1 = np.random.choice([0, 1], size=100)
    chose_ot = np.random.choice([0, 1], size=100)
    wagegap = np.random.choice(np.arange(-5, 5, 1), size=100)
    treatment_number = np.random.choice([14, 26], size=100)
    version = np.random.choice([1.0, 2.0], size=100)
    df = pd.DataFrame(
        {
            "chose_position1": chose_position1,
            "chose_ot": chose_ot,
            "wagegap": wagegap,
            "treatment_number": treatment_number,
            "version": version,
        },
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


def test_table_6(mock_table_6, treatment, error):
    df_got = table_6(mock_table_6, treatment, error)
    df_expected = pd.DataFrame(
        [[0.69, 14.62], [3.59, 33.94]],
        columns=["WTP for 40 hour-per-week job", "Shadow value of time"],
        index=["20 hour-per-week job", "50 hour-per-week job"],
    )
    assert_frame_equal(df_got, df_expected)


@pytest.fixture()
def mock_wave_1():
    np.random.seed(31032023)
    chose_flex = np.random.choice([0, 1], size=100)
    chose_fixed = np.random.choice([0, 1], size=100)
    wagegap_irreg = np.random.choice([0, 2, 5, 10, 15, 25, 35], size=100)
    hasirregjob = np.random.choice([0, 1], size=100)
    wagegap_flex = np.random.choice([0, 2, 5, 10, 20, 35], size=100)
    hasflexjob = np.random.choice([0, 1], size=100)
    wgt_flex = np.random.normal(0, 1, size=100)
    wgt_irreg = np.random.normal(0, 1, size=100)
    df = pd.DataFrame(
        {
            "chose_flex": chose_flex,
            "chose_fixed": chose_fixed,
            "wagegap_irreg": wagegap_irreg,
            "hasirregjob": hasirregjob,
            "wagegap_flex": wagegap_flex,
            "hasflexjob": hasflexjob,
            "wgt_flex": wgt_flex,
            "wgt_irreg": wgt_irreg,
        },
    )
    return df


@pytest.fixture()
def mock_wave_2():
    np.random.seed(31032023)
    chose_wfh = np.random.choice([0, 1], size=100)
    chose_wfh = np.random.choice([0, 1], size=100)
    wagegap_wfh = np.random.choice([0, 2, 5, 10, 15, 25, 35], size=100)
    haswfhjob = np.random.choice([0, 1], size=100)
    wgt_wfh = np.random.normal(0, 1, size=100)
    df = pd.DataFrame(
        {
            "chose_wfh": chose_wfh,
            "wagegap_wfh": wagegap_wfh,
            "haswfhjob": haswfhjob,
            "wgt_wfh": wgt_wfh,
        },
    )
    return df


def test_table_8(mock_wave_1, mock_wave_2):
    df1 = mock_wave_1
    df1["wagegap_hasirregjob"] = df1["wagegap_irreg"] * df1["hasirregjob"]
    df1["wagegap_hasflexjob"] = df1["wagegap_flex"] * df1["hasflexjob"]
    df2 = mock_wave_2
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
    df_logit_31 = table_8(
        df1,
        endog="chose_fixed",
        exog=["wagegap_irreg"],
        weight="wgt_irreg",
        error=0.11363387,
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
            df_logit_31["llf"].mean(),
            df_logit_32["llf"].mean(),
        ],
    )
    llf_got = llf_got.astype(float)
    llf_got = llf_got.round(2)
    llf_expected = pd.array([-68.68, -68.45, -68.57, -67.28, -68.57, -68.79])
    assert np.all(
        llf_got >= llf_expected,
    ), "The log-likelihood values at the optimum must be at least as good as the ones generated from authors' Stata do files"
