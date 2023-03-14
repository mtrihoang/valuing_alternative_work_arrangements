import matplotlib.pyplot as plt
import seaborn as sns
from valuing_alternative_work_arrangements.analysis.breakpoint_program import (
    breakval_figs,
)
from valuing_alternative_work_arrangements.analysis.mle_programs import (
    mylogit_mle2,
)


def fig_setup(df, i):
    """Replicate figures of Mas, Alexandre, and Amanda Pallais (2017).

    Args:
        df (pandas.DataFrame): The experimentdata data.
        i (int): The index of figures.

    Returns:
    -------
        Export figures to .png files.

    """
    df_scatter = breakval_figs(df)
    df_line = mylogit_mle2(df)

    fig, ax = plt.subplots()

    ax = sns.set_style("darkgrid")
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

    ax.set_xlim(-5.5, 5.5)
    ax.set_ylim(-0.2, 1.2)
    ax.set_xlabel("Wage premium for flexible schedule job")
    ax.set_ylabel("Share choosing flexible schedule job")
    ax.legend(
        [
            "Maximum likelihood logit",
            "Breakpoint model",
            "Uncorrected for inattention",
            "Corrected for inattention",
        ],
        loc="lower right",
    )
    ax.set_title("WTP for flexible schedule")

    fig.savefig(f"fig_{i}.png", dpi=1000)
    plt.show()
