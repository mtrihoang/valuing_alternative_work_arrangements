import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytask
import seaborn as sns
from valuing_alternative_work_arrangements.analysis.breakpoint_program import (
    breakval_figs,
)
from valuing_alternative_work_arrangements.analysis.mle_programs import (
    mylogit,
    mylogit_mle2,
)
from valuing_alternative_work_arrangements.config import (
    BLD,
    TASK_FIGURES,
)

url_experimentdata = "https://www.dropbox.com/s/x9un4pkhd57vdei/experimentdata.dta?dl=1"

for index, treatment_number in enumerate(TASK_FIGURES):
    index = index + 1
    kwargs = {
        "treatment_number": treatment_number,
        "produces": BLD / "python" / "figures" / f"fig_{index}_standard_logit.png",
    }

    @pytask.mark.task(id=treatment_number, kwargs=kwargs)
    def fig_setup_sd_logit(produces, treatment_number):
        """Replicate figures of Mas, Alexandre, and Amanda Pallais (2017) associated
        with (standard) logit models.

        Args:
            produces (str): The folder path contains outputs.
            treatment_number (int): The value of the treatment variable in list TASK_FIGURES.

        Returns:
        -------
            The plot for workers's willingness to pay.

        """
        df = pd.read_stata(url_experimentdata)
        df = df.loc[
            (df["treatment_number"] == treatment_number)
            & (df["chose_position1"].notnull()),
            :,
        ]
        df_scatter = breakval_figs(df)
        df_line = mylogit(df)

        fig, ax = plt.subplots()

        ax = sns.lineplot(data=df_line, x="rev_wagegap", y="lnf", color="black")
        ax = sns.scatterplot(
            data=df_scatter,
            x="rev_wagegap",
            y="mm1",
            s=50,
            color="red",
            marker="+",
        )
        ax = sns.scatterplot(
            data=df_scatter,
            x="rev_wagegap",
            y="mmf1",
            s=50,
            color="black",
            marker="+",
        )
        ax = sns.lineplot(
            data=df_scatter,
            x="rev_wagegap",
            y="pg",
            color="red",
            linestyle="--",
        )

        ax.set_xticks(np.arange(-5, 6, 1))
        ax.set_xlim(-5.5, 5.5)
        ax.set_ylim(-0.2, 1.2)
        ax.set_xlabel("Wage premium for flexible schedule job")
        ax.set_ylabel("Share choosing flexible schedule job")
        ax.legend(
            [
                "(Standard) maximum likelihood logit",
                "Breakpoint model",
                "Uncorrected for inattention",
                "Corrected for inattention",
            ],
            loc="lower right",
        )
        ax.set_title("WTP for flexible schedule")

        fig.savefig(produces, dpi=1000)


url_experimentdata = "https://www.dropbox.com/s/x9un4pkhd57vdei/experimentdata.dta?dl=1"

for index, treatment_number in enumerate(TASK_FIGURES):
    index = index + 1
    kwargs = {
        "treatment_number": treatment_number,
        "produces": BLD / "python" / "figures" / f"fig_{index}_error_corrected.png",
    }

    @pytask.mark.task(id=treatment_number, kwargs=kwargs)
    def fig_setup_ec_logit(produces, treatment_number):
        """Replicate figures of Mas, Alexandre, and Amanda Pallais (2017) associated
        with (error-corrected) logit models.

        Args:
            produces (str): The folder path contains outputs.
            treatment_number (int): The value of the treatment variable in list TASK_FIGURES.

        Returns:
        -------
            The plot for workers's willingness to pay.

        """
        df = pd.read_stata(url_experimentdata)
        df = df.loc[
            (df["treatment_number"] == treatment_number)
            & (df["chose_position1"].notnull()),
            :,
        ]
        df_scatter = breakval_figs(df)
        df_line = mylogit_mle2(df)

        fig, ax = plt.subplots()

        ax = sns.lineplot(data=df_line, x="rev_wagegap", y="lnf", color="black")
        ax = sns.scatterplot(
            data=df_scatter,
            x="rev_wagegap",
            y="mm1",
            s=50,
            color="red",
            marker="+",
        )
        ax = sns.scatterplot(
            data=df_scatter,
            x="rev_wagegap",
            y="mmf1",
            s=50,
            color="black",
            marker="+",
        )
        ax = sns.lineplot(
            data=df_scatter,
            x="rev_wagegap",
            y="pg",
            color="red",
            linestyle="--",
        )

        ax.set_xticks(np.arange(-5, 6, 1))
        ax.set_xlim(-5.5, 5.5)
        ax.set_ylim(-0.2, 1.2)
        ax.set_xlabel("Wage premium for flexible schedule job")
        ax.set_ylabel("Share choosing flexible schedule job")
        ax.legend(
            [
                "(Error-corrected) maximum likelihood logit",
                "Breakpoint model",
                "Uncorrected for inattention",
                "Corrected for inattention",
            ],
            loc="lower right",
        )
        ax.set_title("WTP for flexible schedule")

        fig.savefig(produces, dpi=1000)
