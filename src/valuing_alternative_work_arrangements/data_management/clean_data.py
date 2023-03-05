import numpy as np
import pandas as pd


def clean_cps_march2016(url_cps_march2016):
    """Clean the cps_march2016 data.

    Args:
        df (str): The Uniform Resource Locators contains the cps_march2016 data.

    Returns:
    -------
        df (pandas.DataFrame): the final cpsmarch2016 data.

    """
    df = pd.read_stata(url_cps_march2016)
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


def clean_cps_wss(url_cps_wss):
    """Clean the cps_wss data.

    Args:
        df (str): The Uniform Resource Locators contains the cps_wss data.

    Returns:
    -------
        df (pandas.DataFrame): the final cps_wss data.

    """
    df = pd.read_stata(url_cps_wss)
    df.loc[
        (df["wkstat"] == 12)
        | (df["wkstat"] == 21)
        | (df["wkstat"] == 22)
        | (df["wkstat"] == 41),
        "emp_pt",
    ] = 1
    df["emp_pt"] = df["emp_pt"].fillna(0)
    df.loc[df["sex"] == 2, "female"] = 1
    df["female"] = df["female"].fillna(0)
    df["emp_emp"] = 1
    df.loc[
        (df["occ2010"] == 4940)
        | (df["occ2010"] == 5100)
        | (df["occ2010"] == 5240)
        | (df["occ2010"] == 5310),
        "callcenterworker",
    ] = 1
    df["callcenterworker"] = df["callcenterworker"].fillna(0)
    df.loc[(df["classwkr"] == 13) | (df["classwkr"] == 14), "selfemp"] = 1
    df["selfemp"] = df["selfemp"].fillna(0)
    df.loc[df["nativity"] == 5, "foreignborn"] = 1
    df["foreignborn"] = df["foreignborn"].fillna(0)
    df.loc[(df["hispan"] > 0) & (df["hispan"] < 900), "race_hisp"] = 1
    df.loc[(df["race_hisp"] != 1) & (df["hispan"] < 900), "race_hisp"] = 0
    df.loc[df["race"] == 200, "race_black"] = 1
    df.loc[(df["race_black"] != 1) & (df["race"] != np.nan), "race_black"] = 0
    df.loc[df["race"] == 100, "race_white"] = 1
    df.loc[(df["race_white"] != 1) & (df["race"] != np.nan), "race_white"] = 0
    df.loc[df["race"] == 300, "race_natamer"] = 1
    df.loc[(df["race_natamer"] != 1) & (df["race"] != np.nan), "race_natamer"] = 0
    df.loc[(df["race"] == 650) | (df["race"] == 651), "race_asian"] = 1
    df.loc[(df["race_asian"] != 1) & (df["race"] != np.nan), "race_asian"] = 0
    df.loc[df["race"] == 652, "race_pacisl"] = 1
    df.loc[(df["race_pacisl"] != 1) & (df["race"] != np.nan), "race_pacisl"] = 0
    df.loc[df["race"] > 700, "race_multirace"] = 1
    df.loc[(df["race_multirace"] != 1) & (df["race"] != np.nan), "race_multirace"] = 0
    df.loc[df["marst"] == 1, "mar_spouse"] = 1
    df.loc[(df["mar_spouse"] != 1) & (df["marst"] != np.nan), "mar_spouse"] = 0
    df.loc[df["marst"] == 2, "mar_nospouse"] = 1
    df.loc[(df["mar_nospouse"] != 1) & (df["marst"] != np.nan), "mar_nospouse"] = 0
    df.loc[df["marst"] == 3, "mar_separated"] = 1
    df.loc[(df["mar_separated"] != 1) & (df["marst"] != np.nan), "mar_separated"] = 0
    df.loc[df["marst"] == 4, "mar_divorced"] = 1
    df.loc[(df["mar_divorced"] != 1) & (df["marst"] != np.nan), "mar_divorced"] = 0
    df.loc[df["marst"] == 5, "mar_widowed"] = 1
    df.loc[(df["mar_widowed"] != 1) & (df["marst"] != np.nan), "mar_widowed"] = 0
    df.loc[df["marst"] == 6, "mar_nevermar"] = 1
    df.loc[(df["mar_nevermar"] != 1) & (df["marst"] != np.nan), "mar_nevermar"] = 0
    df.loc[df["educ"] <= 71, "ed_lessthanhs"] = 1
    df.loc[(df["ed_lessthanhs"] != 1) & (df["educ"] != np.nan), "ed_lessthanhs"] = 0
    df.loc[df["educ"] == 73, "ed_highschool"] = 1
    df.loc[(df["ed_highschool"] != 1) & (df["educ"] != np.nan), "ed_highschool"] = 0
    df.loc[df["educ"] == 81, "ed_somecollege"] = 1
    df.loc[(df["ed_somecollege"] != 1) & (df["educ"] != np.nan), "ed_somecollege"] = 0
    df.loc[(df["educ"] == 91) | (df["educ"] == 92), "ed_assocdeg"] = 1
    df.loc[(df["ed_assocdeg"] != 1) & (df["educ"] != np.nan), "ed_assocdeg"] = 0
    df.loc[df["educ"] == 111, "ed_bachdeg"] = 1
    df.loc[(df["ed_bachdeg"] != 1) & (df["educ"] != np.nan), "ed_bachdeg"] = 0
    df.loc[df["educ"] > 111, "ed_advanceddeg"] = 1
    df.loc[(df["ed_advanceddeg"] != 1) & (df["educ"] != np.nan), "ed_advanceddeg"] = 0
    df.loc[
        ((df["metro"] == 2) | (df["metro"] == 3)) & (df["metro"] != 0),
        "inornearmetro",
    ] = 1
    df.loc[(df["inornearmetro"] != 1) & (df["metro"] != 0), "inornearmetro"] = 0
    df.loc[df["uhrswork1"] > 990, "uhrswork1"] = np.nan
    df.loc[df["earnweek"] > 990, "earnweek"] = np.nan
    df.loc[df["paidhour"] == 2, "hourly"] = 1
    df.loc[(df["wsflexhrs"] == 2) & (df["wsflexhrs"] < 3), "flexhrs"] = 1
    df.loc[(df["flexhrs"] != 1) & (df["wsflexhrs"] < 3), "flexhrs"] = 0
    df.loc[(df["wswkhm"] == 2) & (df["wswkhm"] < 3), "workhome_dum"] = 1
    df.loc[(df["workhome_dum"] != 1) & (df["wswkhm"] < 3), "workhome_dum"] = 0
    df.loc[
        (df["wswkhmpaid"] == 2)
        & (df["wswkhm"] < 3)
        & ((df["wswkhmpaid"] < 3) | ((df["wswkhmpaid"] == 99) & (df["wswkhm"] == 1))),
        "workhome_paid",
    ] = 1
    df.loc[
        (df["workhome_paid"] != 1)
        & (df["wswkhm"] < 3)
        & ((df["wswkhmpaid"] < 3) | ((df["wswkhmpaid"] == 99) & (df["wswkhm"] == 1))),
        "workhome_paid",
    ] = 0
    df.loc[df["wssttime"] < 9995, "inschedsample"] = 1
    df.loc[
        ((df["wsothshft"] == 1) | (df["wsothshft"] == 2) | (df["wsothshft"] == 4))
        & (df["inschedsample"] == 1),
        "irreg_const",
    ] = 1
    df.loc[
        (df["irreg_const"] != 1)
        & (df["inschedsample"] == 1)
        & (df["wsothshft"] != 96)
        & (df["wsothshft"] != 97)
        & (df["wsothshft"] != 98),
        "irreg_const",
    ] = 0
    df.loc[(df["wsothshft"] == 1) & (df["inschedsample"] == 1), "eveningshift"] = 1
    df.loc[
        (df["eveningshift"] != 1)
        & (df["inschedsample"] == 1)
        & (df["wsothshft"] != 96)
        & (df["wsothshft"] != 97)
        & (df["wsothshft"] != 98),
        "eveningshift",
    ] = 0
    df.loc[(df["wsothshft"] == 2) & (df["inschedsample"] == 1), "nightshift"] = 1
    df.loc[
        (df["nightshift"] != 1)
        & (df["inschedsample"] == 1)
        & (df["wsothshft"] != 96)
        & (df["wsothshft"] != 97)
        & (df["wsothshft"] != 98),
        "nightshift",
    ] = 0
    df.loc[(df["wsothshft"] == 3) & (df["inschedsample"] == 1), "rotatingshift"] = 1
    df.loc[
        (df["rotatingshift"] != 1)
        & (df["inschedsample"] == 1)
        & (df["wsothshft"] != 96)
        & (df["wsothshft"] != 97)
        & (df["wsothshft"] != 98),
        "rotatingshift",
    ] = 0
    df.loc[(df["wsothshft"] == 4) & (df["inschedsample"] == 1), "splitshift"] = 1
    df.loc[
        (df["splitshift"] != 1)
        & (df["inschedsample"] == 1)
        & (df["wsothshft"] != 96)
        & (df["wsothshft"] != 97)
        & (df["wsothshft"] != 98),
        "splitshift",
    ] = 0
    df.loc[(df["wsothshft"] == 5) & (df["inschedsample"] == 1), "irreg_byemp"] = 1
    df.loc[
        (df["irreg_byemp"] != 1)
        & (df["inschedsample"] == 1)
        & (df["wsothshft"] != 96)
        & (df["wsothshft"] != 97)
        & (df["wsothshft"] != 98),
        "irreg_byemp",
    ] = 0
    df.loc[(df["wsothshft"] == 6) & (df["inschedsample"] == 1), "irreg_someother"] = 1
    df.loc[
        (df["irreg_someother"] != 1)
        & (df["inschedsample"] == 1)
        & (df["wsothshft"] != 96)
        & (df["wsothshft"] != 97)
        & (df["wsothshft"] != 98),
        "irreg_someother",
    ] = 0
    df.loc[
        (
            (df["rotatingshift"] == 1)
            | (df["irreg_byemp"] == 1)
            | (df["irreg_someother"] == 1)
        )
        & (df["inschedsample"] == 1),
        "irreg_inconst",
    ] = 1
    df.loc[
        (df["irreg_inconst"] != 1)
        & (df["inschedsample"] == 1)
        & (df["wsothshft"] != 96)
        & (df["wsothshft"] != 97)
        & (df["wsothshft"] != 98),
        "irreg_inconst",
    ] = 0
    df.loc[(df["irreg_const"] == 1) | (df["irreg_inconst"] == 1), "irreg"] = 1
    df.loc[
        (df["irreg"] != 1)
        & (df["irreg_const"] != np.nan)
        & (df["irreg_inconst"] != np.nan),
        "irreg",
    ] = 0
    return df
