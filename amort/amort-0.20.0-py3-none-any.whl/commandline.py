import click
from decimal import Decimal, getcontext
import locale
import pandas as pd


class Amortization(object):

    def __init__(self, p, i, t, q, name="Loan"):
        """
        Locale is used to format currency symbols to amounts. The precision
        for Decimal is set to 20 to eliminate rounding issues. The variables
        p, i, t, and q correlate to present value, interest rate, loan duration
        in years, and number of payments made annually, respectively.
        """
        locale.setlocale(locale.LC_ALL, '')
        getcontext().prec = 50
        self.rounding = Decimal(10) ** -2
        self.p = Decimal(p)
        self.t = Decimal(t)
        self.q = Decimal(q)
        self.i = Decimal(i) / 100 / self.q
        self.name = name
        self.n = int(self.t * self.q)

    def present_value(self):
        """
        Returns the borrowed amount, but more importantly
        is used to calculate the monthly payment amount.
        """
        return self.p

    def number_of_payments(self):
        """
        Returns the total number of payments made throughout
        the duration of the loan. Also, used in the calculation of the
        monthly payment.
        """
        return self.n

    def interest_rate(self):
        """
        Returns the interest rate of the loan as a percentage
        of the number of payments made per annum.
        """
        return self.i

    def monthly_payment(self):
        """
        Calculates the monthly payment of the given loan using the annuity
        formula.
        """
        amount = (self.i * self.p * pow(1 + self.i, self.n)) / (pow(1 + self.i, self.n) - 1)
        return amount

    def beginning_balances(self):
        """
        Calculates the beginning balance of the loan after each payment.
        The beginning balance after the first payment consists of the
        previous balance minus the principal portion of the monthly payment.
        """
        balances = []
        beginning_balance = self.p
        for _ in range(self.n):
            balances.append(beginning_balance)
            beginning_balance -= (self.monthly_payment() - (beginning_balance * self.i))
        return balances

    def monthly_payments(self):
        """
        Calculates the monthly payment for each beginning balance.
        """
        number_of_monthly_payments = []
        for i in range(self.n):
            if self.monthly_payment() < self.beginning_balances()[i]:
                number_of_monthly_payments.append(self.monthly_payment())
            else:
                number_of_monthly_payments.append(self.beginning_balances()[i])
        return number_of_monthly_payments

    def principal_payments(self):
        """
        Calculates the principal portion of each monthly payment.
        """
        principal_payments_balances = []
        for i in range(self.n):
            if self.monthly_payment() - self.interest_payments()[i] < self.beginning_balances()[i]:
                principal_payments_balances.append(self.monthly_payment() - self.interest_payments()[i])
            else:
                principal_payments_balances.append(principal_payments_balances[i-1])
        return principal_payments_balances

    def interest_payments(self):
        """
        Calculates the interest portion of each monthly payment.
        """
        return [(balance * self.i) for balance in self.beginning_balances()]

    def ending_balances(self):
        """
        Calculates the ending balance after each monthly payment by subtracting
        the prinicpal portion of the monthly payment from the beginning balance.
        """
        return [(bal - pay) for bal, pay in zip(self.beginning_balances(), self.monthly_payments())]

    def cumulative_interest(self):
        """
        Calculates the cumulative interest after each monthly payment.
        """
        cumulative = []
        cumulative_interest_payment = 0
        for i in self.interest_payments():
            cumulative_interest_payment += i
            cumulative.append(cumulative_interest_payment)
        return cumulative

    def amortization_schedule(self):
        """
        Outputs an amortization schedule in a Pandas dataframe with columns for the
        number of payments, beginning balance, monthly payment, principal payment,
        interest payment, ending balance, and cumulative interest.
        """
        beginning_balances = [locale.currency(Decimal(b).quantize(self.rounding),
                              grouping=True) for b in self.beginning_balances()]

        monthly_payments = [locale.currency(Decimal(m).quantize(self.rounding),
                            grouping=True) for m in self.monthly_payments()]

        principal_payments = [locale.currency(Decimal(p).quantize(self.rounding),
                              grouping=True) for p in self.principal_payments()]

        interest_payments = [locale.currency(Decimal(i).quantize(self.rounding),
                             grouping=True) for i in self.interest_payments()]

        ending_balances = [locale.currency(Decimal(e).quantize(self.rounding),
                           grouping=True) for e in self.ending_balances()]

        cumulative_interest = [locale.currency(Decimal(c).quantize(self.rounding),
                               grouping=True) for c in self.cumulative_interest()]

        df = pd.DataFrame.from_items([('Beginning Balance', beginning_balances),
                                      ('Monthly Payment', monthly_payments),
                                      ('Principal', principal_payments),
                                      ('Interest', interest_payments),
                                      ('Ending Balance', ending_balances),
                                      ('Cumulative Interest', cumulative_interest)])
        df.index = df.index + 1
        pd.set_option('display.max_rows', len(df))
        pd.set_option('display.width', 1080)
        return df


@click.command()
@click.option('--html', is_flag=True, help="Output amortization schedule to new html file.")
@click.argument('borrowed')
@click.argument('interest')
@click.argument('length')
@click.argument('periods')
@click.argument('name', default="Loan Schedule")
def cli(html, borrowed, interest, length, periods, name):
    """Amortization requires the borrowed amount of the loan, interest rate of the loan.
    length of the loan in years, and the total number of payments made annually. An optional
    argument for name allows the input of a name for the loan schedule. By default, this argument
    is 'Loan Schedule'. The first four arguments may be entered as either string or
    integer data types. The loan name argument requires a string data type.

    Example usage with integers: amortization 500000 4 7 12 "My Aston Martin Loan"

    Example usage with strings: amortization "1000000" "3" "5" "12" "My Bugatti Loan"

    The resulting amortization schedule will print to terminal. If output to an html
    file is preferred, the --html flag will output the amortization schedule to
    'schedule.html' in the current working directory.
    """
    loan = Amortization(borrowed, interest, length, periods, name)
    if html:
        with open('schedule.html', 'w') as output:
            loan.amortization_schedule().to_html(output)
    else:
        print(loan.amortization_schedule())
