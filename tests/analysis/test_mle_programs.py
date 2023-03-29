import pandas as pd
import pytest
from valuing_alternative_work_arrangements.analysis.mle_programs import (
    me_correction,
    mylogit_mle2,
)
from valuing_alternative_work_arrangements.config import BLD

DESIRED_LOG_LIKELIHOOD = -382.74


@pytest.fixture()
def data():
    experimentdata = pd.read_pickle(
        BLD / "python" / "data" / "experimentdata.pkl",
    )
    return experimentdata


def test_mylogit_mle1(data):
    experimentdata = me_correction(data)
    error = experimentdata["error"].mean()
    assert 0 < error < 1, f"Error term must be between 0 and 1, but error = {error}"


def test_mylogit_mle2(data):
    experimentdata = data.loc[
        (data["treatment_number"] == 1) & (data["chose_position1"].notnull()),
        :,
    ]
    LOG_LIKELIHOOD = round(mylogit_mle2(experimentdata).llf.mean(), 2)
    assert (
        LOG_LIKELIHOOD == DESIRED_LOG_LIKELIHOOD
    ), "The log-likelihood value at the optimum must be equal to the one generated from authors' Stata do files"
