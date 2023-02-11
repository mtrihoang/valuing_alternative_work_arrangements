import pytask
from valuing_alternative_work_arrangements.config import BLD
from valuing_alternative_work_arrangements.config import GROUPS
from valuing_alternative_work_arrangements.config import SRC

import pandas as pd
from valuing_alternative_work_arrangements.final import plot_regression_by_age
from valuing_alternative_work_arrangements.utilities import read_yaml
from valuing_alternative_work_arrangements.analysis.model import load_model


for group in GROUPS:

    kwargs = {
        "group": group,
        "depends_on": {"predictions": BLD / "python" / "predictions" / f"{group}.csv"},
        "produces": BLD / "python" / "figures" / f"smoking_by_{group}.png",
    }

    @pytask.mark.depends_on(
        {
            "data_info": SRC / "data_management" / "data_info.yaml",
            "data": BLD / "python" / "data" / "data_clean.csv",
        }
    )
    @pytask.mark.task(id=group, kwargs=kwargs)
    def task_plot_regression_python(depends_on, group, produces):
        data_info = read_yaml(depends_on["data_info"])
        data = pd.read_csv(depends_on["data"])
        predictions = pd.read_csv(depends_on["predictions"])
        fig = plot_regression_by_age(data, data_info, predictions, group)
        fig.write_image(produces)


@pytask.mark.depends_on(BLD / "python" / "models" / "model.pickle")
@pytask.mark.produces(BLD / "python" / "tables" / "estimation_results.tex")
def task_create_estimation_results_python(depends_on, produces):
    model = load_model(depends_on)
    table = model.summary().as_latex()
    with open(produces, "w") as f:
        f.writelines(table)

