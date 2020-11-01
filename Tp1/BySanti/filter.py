import pandas as pd

def full_correction(df):
    date_correction(df)
    int_correction(df)

def date_correction(df):
    _account_created_date_correction(df)
    _opportunity_created_date_correction(df)
    _last_activity_correction(df)
    _quote_expiry_date_correction(df)
    _last_modified_date_correction(df)
    _planned_delivery_start_date_correction(df)
    _planned_delivery_end_date_correction(df)
    _month_correction(df)

def int_correction(df):
    _sales_contract_no_correction(df)
    _price_correction(df)

# DATE SECTION

""" Converts column to date"""
def _account_created_date_correction(df):
    df["Account_Created_Date"] = pd.to_datetime(df["Account_Created_Date"])

""" Converts column to date"""
def _opportunity_created_date_correction(df):
    df["Opportunity_Created_Date"] = pd.to_datetime(df["Opportunity_Created_Date"])

""" Converts column to date"""
def _last_activity_correction(df):
    df["Last_Activity"] = pd.to_datetime(df["Last_Activity"])

def _quote_expiry_date_correction(df):
    df["Quote_Expiry_Date"] = pd.to_datetime(df["Quote_Expiry_Date"])

def _last_modified_date_correction(df):
    df["Last_Modified_Date"] = pd.to_datetime(df["Last_Modified_Date"])

def _planned_delivery_start_date_correction(df):
    df["Planned_Delivery_Start_Date"] = pd.to_datetime(df["Planned_Delivery_Start_Date"])

def _planned_delivery_end_date_correction(df):
    df["Planned_Delivery_End_Date"] = pd.to_datetime(df["Planned_Delivery_End_Date"])

def _month_correction(df):
    df["Month"] = df["Month"].map(lambda x: x.split(" "))
    df["Month"] = df["Month"].map(lambda x: (x[2], x[0])) # (month, year)
    print(df["Month"].head(50))

# INT SECTION

""" Converts None to nan"""
def _sales_contract_no_correction(df):
    df["Sales_Contract_No"] = pd.to_numeric(df["Sales_Contract_No"], errors="coerce")

# FLOAT SECTION

""" Converts None and Other to nan"""
def _price_correction(df):
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")