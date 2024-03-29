import pandas as pd
import pytask
from valuing_alternative_work_arrangements.config import (
    BLD,
    DATA_FILES,
    DROPBOX_URL,
    EXPERIMENTAL_DATA,
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


@pytask.mark.depends_on(BLD / "python" / "data" / "cps_march2016.pkl")
@pytask.mark.produces(BLD / "python" / "data" / "cpsmarch2016.pkl")
def task_clean_cps_march2016(depends_on, produces):
    """Clean the cps_march2016 data and save it into the bld folder.

    Args:
        depends_on (str): The cps_march2016 data.
        produces (str): Specify the folder path where the cpsmarch2016 data will be located in.

    Returns:
    -------
        The cpsmarch2016 dataset.

    """
    data = clean_cps_march2016(depends_on)
    data.to_pickle(produces)


@pytask.mark.depends_on(BLD / "python" / "data" / "cps_wss.pkl")
@pytask.mark.produces(BLD / "python" / "data" / "cpswss.pkl")
def task_clean_cps_wss(depends_on, produces):
    """Clean the cps_wss data and save it into the bld folder.

    Args:
        depends_on (str): The cps_wss data.
        produces (str): Specify the folder path where the cpswss data will be located in.

    Returns:
    -------
        The cpswss dataset.

    """
    data = clean_cps_wss(depends_on)
    data.to_pickle(produces)


@pytask.mark.depends_on(
    {
        "experimentdata": BLD / "python" / "data" / "experimentdata.pkl",
        "experiment_age": BLD / "python" / "data" / "experiment_age.pkl",
        "experiment_education": BLD / "python" / "data" / "experiment_education.pkl",
        "experiment_employmentstatus": BLD
        / "python"
        / "data"
        / "experiment_employmentstatus.pkl",
        "experiment_race": BLD / "python" / "data" / "experiment_race.pkl",
    },
)
@pytask.mark.produces(BLD / "python" / "data" / "experiment_all.pkl")
def task_append_data(depends_on, produces):
    """Append experimental data files into a single file.

    Args:
        depends_on (str): The (individual) experimental data.
        produces (str): Specify the folder path where the appended data will be located in.

    Returns:
    -------
        The (appended) experimental data.

    """
    df = pd.read_pickle(depends_on[EXPERIMENTAL_DATA[0]])
    for experiment in EXPERIMENTAL_DATA[1:]:
        df_experiment = pd.read_pickle(depends_on[experiment])
        df = df.append(df_experiment)
    df.to_pickle(produces)
