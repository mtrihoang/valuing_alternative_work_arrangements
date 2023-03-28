import pandas as pd
import pytest
from valuing_alternative_work_arrangements.analysis.mle_programs import mylogit_mle2

DESIRED_LOG_LIKELIHOOD = -382.74


@pytest.fixture()
def data():
    experimentdata = pd.read_stata(
        "https://www.dropbox.com/s/x9un4pkhd57vdei/experimentdata.dta?dl=1",
    )
    return experimentdata


def test_mylogit_mle2(data):
    experimentdata = data.loc[
        (data["treatment_number"] == 1) & (data["chose_position1"].notnull()),
        :,
    ]
    LOG_LIKELIHOOD = round(mylogit_mle2(experimentdata).llf.mean(), 2)
    assert LOG_LIKELIHOOD == DESIRED_LOG_LIKELIHOOD
