import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from valuing_alternative_work_arrangements.analysis.main_tables import table_6
from valuing_alternative_work_arrangements.analysis.mle_programs import mylogit_mle2


@pytest.fixture()
def data():
    experimentdata = pd.read_stata(
        "https://www.dropbox.com/s/x9un4pkhd57vdei/experimentdata.dta?dl=1",
    )
    return experimentdata


@pytest.fixture()
def treatment():
    treatment_numbers = [14, 26]
    return treatment_numbers


@pytest.fixture()
def error():
    err = 0.145
    return err


def test_table_6(data, treatment, error):
    df_got = table_6(data, treatment, error)
    df_expected = pd.DataFrame(
        [[6.00, 4.01], [0.88, 20.41]],
        columns=["WTP for 40 hour-per-week job", "Shadow value of time"],
        index=["20 hour-per-week job", "50 hour-per-week job"],
    )
    assert_frame_equal(df_got, df_expected)


def test_mylogit_mle2(data):
    mylogit_mle2(data)
