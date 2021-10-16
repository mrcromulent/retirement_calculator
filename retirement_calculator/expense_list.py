from dials_and_buttons import inflate, current_year, get_rate_conversion


class Expense:
    init_cost   = 0
    start_year  = 0
    end_year    = 0
    name        = ""

    def __init__(self,
                 name,
                 cost,
                 time_period="pYear",
                 pay_percentage=1.0,
                 start_year=current_year,
                 end_year=2100,
                 repeat_spacing_in_years=1):

        self.name = name
        self.start_year = start_year
        self.end_year = end_year
        self.repeat_spacing_in_years = repeat_spacing_in_years

        if repeat_spacing_in_years == 1:

            self.init_cost = pay_percentage * get_rate_conversion(cost, time_period)

        else:
            self.init_cost = pay_percentage * cost

    def cost_at_year(self, year):

        ret_val = 0

        if self.start_year <= year <= self.end_year:
            if (year - self.start_year) % self.repeat_spacing_in_years == 0:
                ret_val = round(inflate(self.init_cost, year), 0)

        return ret_val


class ExpenseList:
    expense_list = []

    def __init__(self, expense_list):
        self.expense_list = expense_list

    def total_expense_at_year(self, ts):
        total_expense = 0

        for expense in self.expense_list:
            total_expense += expense.cost_at_year(ts.year)

        return total_expense


# Costs
expl = [Expense("Car Insurance", 450, "pYear"),
        Expense("Phone Bill", 22, "pMonth"),
        Expense("Internet", 55, "pMonth", 0.5),
        Expense("Food", 150, "pWeek"),
        Expense("Fuel", 65 / 3, "pWeek"),
        Expense("Electricity", 200, "pQuarter", 0.5),
        Expense("Gas", 60, "pQuarter", 0.5),
        Expense("Car Service", 1000, "pYear", 0.0),
        Expense("Streaming", 20, "pMonth"),
        Expense("Healthcare", 250, "pYear"),
        Expense("New Cars", 15_000, "pYear", start_year=2025, repeat_spacing_in_years=10),
        Expense("New Phones", 800, "pYear", start_year=2021, repeat_spacing_in_years=4),
        Expense("Miscellaneous", 10_000, "pYear")
        ]

expense_list = ExpenseList(expl)
