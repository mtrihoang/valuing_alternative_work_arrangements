import shutil

import pytask
from pytask_latex import compilation_steps as cs
from valuing_alternative_work_arrangements.config import BLD
from valuing_alternative_work_arrangements.config import PAPER_DIR


documents = ["valuing_alternative_work_arrangements", "valuing_alternative_work_arrangements_pres"]

for document in documents:

    @pytask.mark.latex(
        script=PAPER_DIR / f"{document}.tex",
        document=BLD / "latex" / f"{document}.pdf",
        compilation_steps=cs.latexmk(
            options=("--pdf", "--interaction=nonstopmode", "--synctex=1", "--cd")
        ),
    )
    @pytask.mark.task(id=document)
    def task_compile_documents():
        pass

    kwargs = {
        "depends_on": BLD / "latex" / f"{document}.pdf",
        "produces": BLD.parent.resolve() / f"{document}.pdf",
    }

    @pytask.mark.task(id=document, kwargs=kwargs)
    def task_copy_to_root(depends_on, produces):
        shutil.copy(depends_on, produces)
