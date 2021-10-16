class Income:
    start_year = 0
    start_salary = 0
    end_year = 0
    end_salary = 0
    m = 0
    b = 0
    taxable = True

    def __init__(self, start, end, taxable=True):
        """
        start   = [start_year, start_salary]
        end     = [end_year, end_salary]
        """

        self.start_year = start[0]
        self.start_salary = start[1]
        self.end_year = end[0]
        self.end_salary = end[1]
        self.taxable = taxable

        self.m = (self.end_salary - self.start_salary) / (self.end_year - self.start_year)
        self.b = self.start_salary - self.m * self.start_year

    def income_at_year(self, ts):
        if ts.year < self.start_year or ts.year > self.end_year:
            return 0
        else:
            return self.m * ts.year + self.b


class IncomeList:
    income_list = []

    def __init__(self, income_list):

        self.income_list = income_list

    def find_income_by_year(self, year):

        untaxable_income = 0
        taxable_income = 0

        for income in self.income_list:
            if income.taxable:
                taxable_income += income.income_at_year(year)
            else:
                untaxable_income += income.income_at_year(year)

        return [untaxable_income, taxable_income]


income_list = IncomeList([Income([2020, 30_000], [2024, 30_000], False),
                          Income([2025, 80_000], [2035, 110_000]),
                          Income([2036, 110_000], [2100, 120_000])])
