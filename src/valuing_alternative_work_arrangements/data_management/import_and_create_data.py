import pandas as pd


def clean_cps_march2016(url):
    """Clean the cps_march2016 data.

    Args:
        df (str): The Uniform Resource Locators contains the cps_march2016 data.

    Returns:
    -------
        df (pandas.DataFrame): the final cpsmarch2016 data.

    """
    df = pd.read_stata(url)
    df.loc[(df["gtcbsast"] == 2) | (df["gtcbsast"] == 1), "any_city"] = 1
    df.loc[df["pesex"] == 2, "female"] = 1
    df["female"] = df["female"].fillna(0)
    df.loc[
        ((df["prwksch"] == 1) | (df["prwksch"] == 2)) & (df["prwksch"] > 0),
        "emp_emp",
    ] = 1
    df.loc[(df["emp_emp"] != 1) & (df["prwksch"] > 0), "emp_emp"] = 0
    df.loc[(df["emp_emp"] == 0) & (df["prwksch"] > 0), "emp_unemp"] = 1
    df.loc[(df["emp_unemp"] != 1) & (df["prwksch"] > 0), "emp_unemp"] = 0
    df.loc[
        (df["prftlf"] == 1) & (df["emp_emp"] == 1) & (df["prwksch"] > 0),
        "emp_ft",
    ] = 1
    df.loc[(df["emp_ft"] != 1) & (df["prwksch"] > 0), "emp_ft"] = 0
    df.loc[
        (df["prftlf"] == 2) & (df["emp_emp"] == 1) & (df["prwksch"] > 0),
        "emp_pt",
    ] = 1
    df.loc[(df["emp_pt"] != 1) & (df["prwksch"] > 0), "emp_pt"] = 0
    df.loc[df["pehspnon"] == 1, "race_hisp"] = 1
    df["race_hisp"] = df["race_hisp"].fillna(0)
    df.loc[
        (df["ptdtrace"] == 1) & (df["race_hisp"] != 1) & (df["ptdtrace"] > 0),
        "race_white",
    ] = 1
    df.loc[(df["race_white"] != 1) & (df["ptdtrace"] > 0), "race_white"] = 0
    df.loc[
        (df["ptdtrace"] == 2) & (df["race_hisp"] != 1) & (df["ptdtrace"] > 0),
        "race_black",
    ] = 1
    df.loc[(df["race_black"] != 1) & (df["ptdtrace"] > 0), "race_black"] = 0
    df.loc[
        (df["race_hisp"] == 0) & (df["race_white"] == 0) & (df["race_black"] == 0),
        "race_other",
    ] = 1
    df["race_black"] = df["race_black"].fillna(0)
    df.loc[df["prtage"] < 80, "age_"] = df["prtage"]
    df.loc[df["prtage"] < 30, "age_under30"] = 1
    df["age_under30"] = df["age_under30"].fillna(0)
    df.loc[(df["prtage"] >= 30) & (df["prtage"] <= 40), "age_30to40"] = 1
    df["age_30to40"] = df["age_30to40"].fillna(0)
    df.loc[df["prtage"] > 40, "age_over40"] = 1
    df["age_over40"] = df["age_over40"].fillna(0)
    df.loc[df["peeduca"] <= 38, "ed_lessthanhs"] = 1
    df["ed_lessthanhs"] = df["ed_lessthanhs"].fillna(0)
    df.loc[df["peeduca"] == 39, "ed_highschool"] = 1
    df["ed_highschool"] = df["ed_highschool"].fillna(0)
    df.loc[df["peeduca"] == 40, "ed_somecollege"] = 1
    df["ed_somecollege"] = df["ed_somecollege"].fillna(0)
    df.loc[
        (df["peeduca"] == 41) | (df["peeduca"] == 42) | (df["peeduca"] == 43),
        "ed_collegedeg",
    ] = 1
    df["ed_collegedeg"] = df["ed_collegedeg"].fillna(0)
    df.loc[df["peeduca"] >= 40, "ed_morethancol"] = 1
    df["ed_morethancol"] = df["ed_morethancol"].fillna(0)
    df.loc[
        (df["peio1ocd"] == 4940)
        | (df["peio1ocd"] == 5100)
        | (df["peio1ocd"] == 5240)
        | (df["peio1ocd"] == 5310),
        "callcenterworker",
    ] = 1
    df["callcenterworker"] = df["callcenterworker"].fillna(0)
    df.loc[df["emp_unemp"] == 1, "callcenterworker"] = 0
    return df
