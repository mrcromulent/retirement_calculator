from dials_and_buttons import get_rate_conversion


class InterestAndFees:
    
    interest_rate   = 0
    flat_fee        = 0
    percentage_fee  = 0
    
    def __init__(self,
                 interest_rate=0.0,
                 int_per_time='pYear',
                 flat_fee=0.0,
                 flat_per_time='pYear',
                 percentage_fee=0.0,
                 per_per_time='pYear'):

        self.interest_rate  = get_rate_conversion(interest_rate, int_per_time)
        self.flat_fee       = get_rate_conversion(flat_fee, flat_per_time)
        self.percentage_fee = get_rate_conversion(percentage_fee, per_per_time)


class InvSavAccount:
    
    balance         = 0
    interest_rate   = 0
    fees            = InterestAndFees()
    type            = ""
    
    def __init__(self, balance, fees):
        self.balance        = balance
        self.interest_rate  = fees.interest_rate
        self.fees           = fees
        
    def withdrawal(self, amount):
        if self.balance - amount >= 0:
            self.balance -= amount
            return amount
        else:
            allowable_withdrawal = self.balance
            self.balance = 0
            return allowable_withdrawal
        
    def deposit(self, amount):
        self.balance += amount
        
    def subtract_yearly_fees(self):
        curr_fee = self.fees.flat_fee + self.fees.percentage_fee * self.balance
        
        self.withdrawal(curr_fee)
        
    def accrue_interest(self):
        self.balance *= (1 + self.interest_rate)
        
    def fees_and_interest(self):
        self.subtract_yearly_fees()
        self.accrue_interest()


class InvSavList:
    
    etfs = []
    savs = []
    sups = []
    
    etf_contribution_pc     = 0.5
    savings_contribution_pc = 0.5
    
    def __init__(self, loan_list, etf_contribution_pc=0.5, savings_contribution_pc=0.5):

        etfs = []
        sups = []
        savs = []
        
        for loan in loan_list:
            if loan.type == "ETF Account":
                etfs.append(loan)
            elif loan.type == "Savings Account":
                savs.append(loan)
            elif loan.type == "Super Account":
                sups.append(loan)

        self.etfs = etfs
        self.sups = sups
        self.savs = savs

        self.etf_contribution_pc     = etf_contribution_pc 
        self.savings_contribution_pc = savings_contribution_pc
        
    def distributed_withdrawal(self, overdraft):
        """
        function to prioritise withdrawal first from savings, then etfs then super
        """
        
        ret_val      = True
        remaining   = overdraft
        
        w1 = self.savs[0].withdrawal(remaining)
        remaining -= w1
        
        if remaining != 0:
            w2 = self.etfs[0].withdrawal(remaining)
            remaining -= w2
            
            if remaining != 0:
                w3 = self.sups[0].withdrawal(remaining)
                remaining -= w3
                
                if remaining != 0:
                    ret_val = False
            
        return ret_val
    
    def contribute_to_savings(self, net_income):
        
        etf_contribution        = self.etf_contribution_pc * net_income
        savings_contribution    = self.savings_contribution_pc * net_income
        
        self.etfs[0].deposit(etf_contribution)
        self.savs[0].deposit(savings_contribution)
        
    def get_total_savings(self):
        return self.etfs[0].balance + self.savs[0].balance + self.sups[0].balance


class EtfAccount(InvSavAccount):

    def __init__(self, balance, fees):

        InvSavAccount.__init__(self, balance, fees)
        self.type = "ETF Account"


class SavingsAccount(InvSavAccount):

    def __init__(self, balance, fees):

        InvSavAccount.__init__(self, balance, fees)
        self.type = "Savings Account"


class SuperAccount(InvSavAccount):

    def __init__(self, balance, fees):

        InvSavAccount.__init__(self, balance, fees)
        self.type = "Super Account"


# Personal financial
# Super and investments
tmp1 = InterestAndFees(interest_rate=0.07, int_per_time='pYear',
                       flat_fee=5, flat_per_time='pMonth',
                       percentage_fee=0.004, per_per_time='pYear')
super_acct  = SuperAccount(8_000, tmp1)

tmp2 = InterestAndFees(interest_rate=0.07, int_per_time='pYear',
                       flat_fee=5, flat_per_time='pMonth',
                       percentage_fee=0.005, per_per_time='pYear')
etf_acct    = EtfAccount(23_000, tmp2)

# Bank
tmp3 = InterestAndFees(interest_rate=0.0002, int_per_time='pYear',
                       flat_fee=0, flat_per_time='pMonth',
                       percentage_fee=0, per_per_time='pYear')
savings_acct = SavingsAccount(9_000 + 6_300, tmp3)

inv_sav_list = InvSavList([etf_acct, super_acct, savings_acct], etf_contribution_pc=0.7, savings_contribution_pc=0.3)
