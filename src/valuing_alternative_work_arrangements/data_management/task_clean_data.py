import pandas as pd
import pytask
from valuing_alternative_work_arrangements.config import (
    BLD,
    DATA_FILES,
    DROPBOX_URL,
)
from valuing_alternative_work_arrangements.data_management.clean_data import (
    clean_cps_march2016,
    clean_cps_wss,
)

for index, data_file in enumerate(DATA_FILES):

    kwargs = {
        "index": index,
        "produces": BLD / "python" / "data" / f"{data_file}.pkl",
    }

    @pytask.mark.task(id=index, kwargs=kwargs)
    def task_import_data(produces, index):
        """Import the CPS Work Schedules Supplement and experimental data files and save
        to the bld folder.

        Args:
            produces (str): The folder path where CPS and experimental data files are stored.
            index (int): the pytask index.

        Returns:
        -------
            The CPS and experimental datasets.

        """
        df = pd.read_stata(DROPBOX_URL[index])
        df.to_pickle(produces)


url_cps_march2016 = "https://www.dropbox.com/s/ri1mq4859sngizx/cps_march2016.dta?dl=1"


@pytask.mark.produces(BLD / "python" / "data" / "cpsmarch2016.csv")
def task_clean_cps_march2016(produces):
    """Clean the cps_march2016 data from the Dropbox link and save it into the bld
    folder.

    Args:
        produces: Specify the folder path where the cpsmarch2016 data will be located in.

    Returns:
    -------
        The cpsmarch2016 dataset.

    """
    data = clean_cps_march2016(url_cps_march2016)
    data.to_csv(produces)


url_clean_cps_wss = "https://www.dropbox.com/s/8r70kj4qxda61vh/cps_wss.dta?dl=1"


@pytask.mark.produces(BLD / "python" / "data" / "cpswss.csv")
def task_clean_cps_wss(produces):
    """Clean the cps_wss data from the Dropbox link and save it into the bld folder.

    Args:
        produces: Specify the folder path where the cpswss data will be located in.

    Returns:
    -------
        The cpswss dataset.

    """
    data = clean_cps_wss(url_clean_cps_wss)
    data.to_csv(produces)
