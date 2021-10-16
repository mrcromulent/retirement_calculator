import numpy as np
import pandas as pd
from datetime import date, timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pandas.plotting import register_matplotlib_converters
from dials_and_buttons import tax_brackets, hecs_brackets, empl_contr


class Portfolio:
    income_list     = None
    inv_sav_list    = None
    loan_list       = None
    expense_list    = None

    def __init__(self, income_list=None, inv_sav_list=None, loan_list=None, expense_list=None):
        self.income_list = income_list
        self.inv_sav_list = inv_sav_list
        self.loan_list = loan_list
        self.expense_list = expense_list


class Human:
    portfolio = Portfolio()
    life_expectancy = 0
    life_buffer = 0
    retirement_age = 0
    retirement_year = 0
    retirement_dt = 0
    current_age = 0
    death_age = 0
    death_date = 0

    def __init__(self,
                 portfolio=Portfolio(),
                 dob=date(1995, 8, 1),
                 life_expectancy=82.5,
                 life_buffer=8,
                 retirement_age=67):
        self.portfolio = portfolio

        self.life_expectancy = life_expectancy
        self.life_buffer = life_buffer
        self.retirement_age = retirement_age

        now = date.today()
        self.retirement_dt = dob + timedelta(days=retirement_age * 365)
        self.retirement_year = self.retirement_dt.year
        self.death_date = dob + timedelta(days=life_expectancy * 365)
        self.current_age = now.year - dob.year
        self.death_age = self.death_date.year + life_buffer


class Simulation:

    t = 0
    current_year = 0
    human = Human()

    untaxable_income = []
    taxable_income = []
    net_income = []
    tax_bill = []
    sup_bal = []
    sav_bal = []
    etf_bal = []
    loan_amounts_remaining = []

    def __init__(self, human=Human()):
        now = date.today()
        self.current_year = now.year
        self.human = human

        self.t = pd.date_range(start=now, end=human.death_date, freq='Y')

    def run_simulation(self):

        p               = self.human.portfolio
        income_list     = p.income_list
        inv_sav_list    = p.inv_sav_list
        loan_list       = p.loan_list
        expense_list    = p.expense_list
        sup_acct        = inv_sav_list.sups[0]
        etf_acct        = inv_sav_list.etfs[0]
        sav_acct        = inv_sav_list.savs[0]

        time_to_retire = False

        mort_self = 625 * 12
        mort_ben = 2125 * 12
        mortgage_repayment = mort_self + mort_ben

        for year in self.t:

            if self.time_to_retire(year) and not time_to_retire:
                time_to_retire = True
                self.human.retirement_dt = year

            # Net_income keeps track of money in and out over the year
            net_income          = 0
            gross_income        = 0
            taxable_income      = 0
            untaxable_income    = 0

            if not time_to_retire:
                # Earn money
                untaxable_income, taxable_income = income_list.find_income_by_year(year)
                gross_income = untaxable_income + taxable_income

            # Contribute to Super
            super_contribution = empl_contr * gross_income
            sup_acct.deposit(super_contribution)

            # Pay Taxes
            tax_bill = self.find_income_tax(taxable_income, year.year)
            net_income += gross_income - tax_bill

            # Add interest to loans
            if loan_list.any_active_loans():
                loan_list.add_interests()

            # Pay HECS on the first listed loan
            if loan_list.any_active_hecs_loans():
                hecs_repayment = self.find_hecs_repayment(net_income, year.year)
                h_list = loan_list.get_active_hecs_loans()
                h_list[0].repay(hecs_repayment)
                net_income -= hecs_repayment

            # Pay Down Mortgages
            if loan_list.any_active_mortgages():
                loan_list.repay_priority_loan(mortgage_repayment)
                net_income -= mort_self

            # Pay for expenses
            expenses = expense_list.total_expense_at_year(year)
            net_income -= expenses

            # Contribute to or draw from savings

            if net_income > 0:  # Income exceeds expenditure
                inv_sav_list.contribute_to_savings(net_income)

            else:  # Living off savings
                overdraft = abs(net_income)
                inv_sav_list.distributed_withdrawal(overdraft)

            # Pay fees
            sup_acct.fees_and_interest()
            etf_acct.fees_and_interest()
            sav_acct.fees_and_interest()

            # Add data
            self.untaxable_income.append(untaxable_income)
            self.taxable_income.append(taxable_income)
            self.net_income.append(net_income)
            self.tax_bill.append(tax_bill)
            self.sup_bal.append(sup_acct.balance)
            self.sav_bal.append(sav_acct.balance)
            self.etf_bal.append(etf_acct.balance)

            self.loan_amounts_remaining.append([loan.get_remaining_amount() for loan in loan_list.loan_list])

    def plot_data(self, export=False):

        register_matplotlib_converters()
        self.plot_income_and_tax()
        self.plot_net_income()
        self.plot_savings()
        self.plot_loans()

        plt.show()

        if export:
            pass

    def plot_income_and_tax(self):
        width = 0.3
        x = np.array(self.t.year)

        fig, ax = plt.subplots()
        plt.title("Income and taxes")
        p0 = plt.bar(x, self.untaxable_income, width)
        p1 = plt.bar(x, self.tax_bill, width)
        p2 = plt.bar(x, np.array(self.taxable_income) - np.array(self.tax_bill), width, bottom=self.tax_bill)
        self.plot_axes_years_aud(ax)
        self.plot_retirement_age(ax, no_dt=True)
        plt.legend((p0[0], p1[0], p2[0]), ('Untaxable Income', 'Tax Bill', 'Taxable Income'), loc='best')

    def plot_net_income(self):
        width = 0.3
        x = np.array(self.t.year)
        y = np.array(self.net_income)

        fig, ax = plt.subplots()
        plt.title("Net Income")
        p0 = plt.bar(x[y >= 0], y[y >= 0], width, color='black')
        p1 = plt.bar(x[y < 0], y[y < 0], width, color='red')
        plt.legend((p0[0], p1[0]), ('Net Income', 'Net Income'), loc='best')
        self.plot_axes_years_aud(ax)
        self.plot_retirement_age(ax, no_dt=True)

    def plot_savings(self):

        x = self.t
        y1 = np.array(self.etf_bal)
        y2 = np.array(self.sav_bal)
        y3 = np.array(self.sup_bal)
        total = y1 + y2 + y3

        fig, ax = plt.subplots()
        plt.title("Savings")
        plt.plot(x, y1, label='ETF account balance')
        plt.plot(x, y2, label='Savings account balance')
        plt.plot(x, y3, label='Super account balance')
        plt.plot(x, total, label='Total')
        self.plot_axes_years_aud(ax)
        self.plot_retirement_age(ax)
        plt.legend(loc='best')

    def plot_loans(self):

        if self.loan_amounts_remaining:
            fig, ax = plt.subplots()
            plt.title("Loan Balances")

            for i in range(len(self.loan_amounts_remaining[0])):
                y = [lra[i] for lra in self.loan_amounts_remaining]
                plt.plot(self.t, y, label='Loan balance' + str(i)
                                          + ' ' + self.human.portfolio.loan_list.loan_list[i].type)

            self.plot_axes_years_aud(ax)
            self.plot_retirement_age(ax)
            plt.legend(loc='best')

    def plot_retirement_age(self, ax, no_dt=False):

        if no_dt:
            ret_year = self.human.retirement_dt.year
        else:
            ret_year = self.human.retirement_dt

        ax.axvline(x=ret_year, linestyle='dashed', alpha=0.5)

    def time_to_retire(self, year):
        p = self.human.portfolio
        income_list = p.income_list
        inv_sav_list = p.inv_sav_list

        untaxable_income, taxable_income = income_list.find_income_by_year(year)
        gross_income = untaxable_income + taxable_income - self.find_income_tax(taxable_income, year.year)

        return inv_sav_list.get_total_savings() > 25 * gross_income

    @staticmethod
    def plot_axes_years_aud(ax):

        plt.xlabel("Years")
        plt.xticks(rotation=25)

        plt.ylabel("AUD")
        plt.yticks(rotation=60)
        fmt = '${x:,.0f}'
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter(fmt))

        plt.grid(True)

    @staticmethod
    def find_income_tax(income, year):

        ret_val = 0

        tax_brackets_year = tax_brackets(year)
        for bracket in tax_brackets_year:
            if income <= bracket[0]:
                ret_val = (income - bracket[1]) * bracket[2] + bracket[3]
                break

        return ret_val

    @staticmethod
    def find_hecs_repayment(income, year):

        ret_val = 0

        hecs_brackets_year = hecs_brackets(year)
        for bracket in hecs_brackets_year:
            if income <= bracket[0]:
                ret_val = bracket[1] * income
                break

        return ret_val
