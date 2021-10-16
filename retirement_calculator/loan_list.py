from dials_and_buttons import inflation_rate


class Loan:
    
    loan_amount         = 0
    interest_rate       = 0
    remaining_amount    = 0
    active              = False
    type                = ""

    def __init__(self, loan_amount, interest_rate):
        self.loan_amount        = loan_amount
        self.remaining_amount   = loan_amount
        self.interest_rate      = interest_rate
        self.active             = True
        
    def repay(self, amount):
        
        if self.loan_amount > 0:
            if self.remaining_amount - amount <= 0:
                self.close_loan()
            else:
                self.remaining_amount -= amount 
            
    def get_remaining_amount(self):
        return self.remaining_amount
    
    def add_interest(self):
        if self.active:
            self.remaining_amount *= (1 + self.interest_rate)
            
    def close_loan(self):
        self.remaining_amount   = 0
        self.active             = False
            

class HecsLoan(Loan):

    def __init__(self, loan_amount, interest_rate):
        Loan.__init__(self, loan_amount, interest_rate)

        self.type = "HECS Loan"


class Mortgage(Loan):

    def __init__(self, loan_amount, interest_rate):
        Loan.__init__(self, loan_amount, interest_rate)

        self.type = "Mortgage"


class LoanList:
    
    loan_list = []
    
    def __init__(self, loan_list):
        self.loan_list = loan_list

    def any_active_loans(self):
        
        ret_val = False
        
        for loan in self.loan_list:
            if loan.active:
                ret_val = True
                
        return ret_val
    
    def repay_priority_loan(self, amount):
        """
        Find the loan whose principal will grow the most and repay that one
        """
        
        curr_leader = self.loan_list[0]
        
        for loan in self.loan_list:
            if ((loan.remaining_amount * loan.interest_rate) > 
                    (curr_leader.remaining_amount * curr_leader.interest_rate)):
                curr_leader = loan
        
        curr_leader.repay(amount)
        
    def add_interests(self):
        
        for loan in self.loan_list:
            loan.add_interest()

    def get_active_mortgages(self):

        m_list = []

        for loan in self.loan_list:
            if loan.type == "Mortgage" and loan.active:
                m_list.append(loan)

        return m_list

    def get_active_hecs_loans(self):

        h_list = []

        for loan in self.loan_list:
            if loan.type == "HECS Loan" and loan.active:
                h_list.append(loan)

        return h_list

    def any_active_hecs_loans(self):

        ret_val = True

        if not self.get_active_hecs_loans():
            ret_val = False

        return ret_val

    def any_active_mortgages(self):

        ret_val = True

        if not self.get_active_mortgages():
            ret_val = False

        return ret_val


ll          = [Mortgage(52_500, 0.0403), Mortgage(286_850, 0.0389), HecsLoan(47_000, inflation_rate)]
loan_list   = LoanList(ll)
