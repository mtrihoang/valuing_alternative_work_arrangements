import pytask
from valuing_alternative_work_arrangements.config import BLD
from valuing_alternative_work_arrangements.config import GROUPS
from valuing_alternative_work_arrangements.config import SRC

import pandas as pd
from valuing_alternative_work_arrangements.analysis.model import fit_logit_model
from valuing_alternative_work_arrangements.analysis.model import load_model
from valuing_alternative_work_arrangements.analysis.predict import predict_prob_by_age
from valuing_alternative_work_arrangements.utilities import read_yaml


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "data" / "data_clean.csv",
        "data_info": SRC / "data_management" / "data_info.yaml",
    }
)
@pytask.mark.produces(BLD / "python" / "models" / "model.pickle")
def task_fit_model_python(depends_on, produces):
    data_info = read_yaml(depends_on["data_info"])
    data = pd.read_csv(depends_on["data"])
    model = fit_logit_model(data, data_info, model_type="linear")
    model.save(produces)


for group in GROUPS:

    kwargs = {
        "group": group,
        "produces": BLD / "python" / "predictions" / f"{group}.csv",
    }

    @pytask.mark.depends_on(
        {
            "data": BLD / "python" / "data" / "data_clean.csv",
            "model": BLD / "python" / "models" / "model.pickle",
        }
    )
    @pytask.mark.task(id=group, kwargs=kwargs)
    def task_predict_python(depends_on, group, produces):
        model = load_model(depends_on["model"])
        data = pd.read_csv(depends_on["data"])
        predicted_prob = predict_prob_by_age(data, model, group)
        predicted_prob.to_csv(produces, index=False)

