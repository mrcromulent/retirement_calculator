"""

Notes:
    I tried to find information on the old age pension and cap gains taxes but it was too hard to understand. Could be
    worth revisiting at a later date

TODO:
    Fix the retirement year as int vs datetime thing and simplify the fields in human.retirement* and human.death*
    Exporting results
    Stretch idea : Export report with images. Capability to compare different strategies
    (i.e. passing different humans to sim?)
    Stretch idea : add capability to see difference between past projected and collected data
"""

from helper_functions import Simulation, Human, Portfolio
from expense_list import expense_list
from inv_sav_list import inv_sav_list
from income_list import income_list
from loan_list import loan_list


def main():
    portfolio   = Portfolio(income_list, inv_sav_list, loan_list, expense_list)
    pierre      = Human(portfolio)

    sim = Simulation(pierre)
    sim.run_simulation()
    sim.plot_data()


if __name__ == "__main__":
    main()
