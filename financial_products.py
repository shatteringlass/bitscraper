class FinancialProduct(object):
    pass


class BITProduct(FinancialProduct):
    pass


class IDEMProduct(BITProduct):
    slots = {'Isin_Code',
             'Series_Name',
             'Contract_Size',
             'Underlying_Code',
             'Closing_Price',
             'Var._%',
             'First_Price',
             'Low_Price',
             'Max_Price',
             'Last_Stream_Price',
             'Open_Interest',
             'Trades',
             'Of_which_negotiated_trades',
             'Turnover',
             'Of_which_negotiated_trades',
             'Expiry_Date'}

    pass
