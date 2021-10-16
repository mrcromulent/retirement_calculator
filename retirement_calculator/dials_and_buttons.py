from datetime import date
from numpy import inf

now             = date.today()
current_year    = now.year
inflation_rate  = 0.020
empl_contr      = 0.095

tax_brackets_2020 = [
    [18_200, 000000, 0.000, 0000],
    [37_000, 18_200, 0.190, 0000],
    [90_000, 37_000, 0.235, 3572],
    [180_000, 90_000, 0.370, 20_797],
    [inf, 180_000, 0.450, 54_097]]

hecs_brackets_2020 = [
    [45_881, 0.000],
    [52_973, 0.010],
    [56_151, 0.020],
    [59_521, 0.025],
    [63_092, 0.030],
    [66_877, 0.035],
    [70_890, 0.040],
    [75_144, 0.045],
    [79_652, 0.050],
    [84_432, 0.055],
    [89_498, 0.060],
    [94_868, 0.065],
    [100_560, 0.070],
    [106_593, 0.075],
    [112_989, 0.080],
    [119_769, 0.085],
    [126_955, 0.090],
    [134_572, 0.095],
    [inf, 0.100]]


def tax_brackets(year):

    tax_brackets_year = []
    for bracket in tax_brackets_2020:
        inflated_bracket = [inflate(bracket[0], year), inflate(bracket[1], year), bracket[2], inflate(bracket[3], year)]
        tax_brackets_year.append(inflated_bracket)

    return tax_brackets_year


def hecs_brackets(year):

    hecs_brackets_year = []
    for bracket in hecs_brackets_2020:
        inflated_bracket = [inflate(bracket[0], year), bracket[1]]
        hecs_brackets_year.append(inflated_bracket)

    return hecs_brackets_year


def inflate(p, year):
    return p * (1 + inflation_rate) ** (year - current_year)


def get_rate_conversion(cost, p_time):
    """
    Converts to yearly cost
    """

    switcher = {
        "pYear": 1,
        "pMonth": 12,
        "pWeek": 52,
        "pQuarter": 4,
        "pDay": 365}

    return cost * switcher.get(p_time, 0)
