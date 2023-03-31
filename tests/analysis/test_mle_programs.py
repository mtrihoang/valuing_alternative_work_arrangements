import numpy as np
import pandas as pd
import pytest
from valuing_alternative_work_arrangements.analysis.mle_programs import (
    me_correction,
    mylogit_mle2,
)

DESIRED_LOG_LIKELIHOOD = -32.9


@pytest.fixture()
def mock_exp_data():
    """Create the mock experimental data."""
    np.random.seed(31032023)
    chose_position1 = np.random.choice([0, 1], size=100)
    wagegap = np.random.choice(np.arange(-5, 5, 1), size=100)
    treatment_number = np.random.choice([1, 2], size=100)
    df = pd.DataFrame(
        {
            "chose_position1": chose_position1,
            "wagegap": wagegap,
            "treatment_number": treatment_number,
        },
    )
    return df


def test_mylogit_mle1(mock_exp_data):
    """This function is created to verify the range of error rate, which must be in (0,
    1).

    Args:
        mock_exp_data (pandas.DataFrame): The mock experimental data.

    Returns:
    -------
        Show the error message if function me_correction does not pass the test.

    """
    experimentdata = me_correction(mock_exp_data)
    error = experimentdata["error"].mean()
    assert 0 < error < 1, f"Error term must be between 0 and 1, but error = {error}"


def test_mylogit_mle2(mock_exp_data):
    """This function is created to verify the Stata to Python equivalence with MLE
    functions. The log-likelihood values at the optimum must be consistent.

    Args:
        mock_exp_data (pandas.DataFrame): The mock experimental data.

    Returns:
    -------
        Show the error message if function mylogit_mle2 does not pass the test.

    """
    experimentdata = mock_exp_data.loc[
        (mock_exp_data["treatment_number"] == 1)
        & (mock_exp_data["chose_position1"].notnull()),
        :,
    ]
    LOG_LIKELIHOOD = round(mylogit_mle2(experimentdata).llf.mean(), 2)
    assert (
        LOG_LIKELIHOOD == DESIRED_LOG_LIKELIHOOD
    ), "The log-likelihood value at the optimum must be equal to the one generated from authors' Stata do files"
