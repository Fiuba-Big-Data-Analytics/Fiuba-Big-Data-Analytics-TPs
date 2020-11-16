import pandas as pd


def full_correction(df):
    date_correction(df)
    numeric_correction(df)
    name_correction(df)
    categoric_to_numeric(df)
    delete_correction(df)


def categoric_to_numeric(df):
    _bureaucratic_code_to_numeric(df)
    _source_to_numeric(df)
    _account_name_to_numeric(df)
    _opportunity_name_to_numeric(df)
    _account_type_to_numeric(df)
    _opportunity_type_to_numeric(df)
    _account_owner_to_numeric(df)
    _opportunity_owner_to_numeric(df)
    _brand_to_numeric(df)
    _product_type_to_numeric(df)
    _last_modified_by_to_numeric(df)
    _product_family_to_numeric(df)
    _product_name_to_numeric(df)


def date_correction(df):
    _account_created_date_correction(df)
    _opportunity_created_date_correction(df)
    _quote_expiry_date_correction(df)
    _last_modified_date_correction(df)
    _planned_delivery_start_date_correction(df)
    _planned_delivery_end_date_correction(df)
    _month_correction(df)


def numeric_correction(df):
    _sales_contract_no_correction(df)
    _price_correction(df)


def name_correction(df):
    _total_power_correction(df)
    _source_correction(df)


def delete_correction(df):
    _last_activity_delete(df)
    _actual_delivery_date_delete(df)
    _submitted_for_approval(df)
    _product_category_a(df)

# DATE SECTION


""" Converts column to date"""


def _account_created_date_correction(df):
    df["Account_Created_Date"] = pd.to_datetime(df["Account_Created_Date"])


""" Converts column to date"""


def _opportunity_created_date_correction(df):
    df["Opportunity_Created_Date"] = pd.to_datetime(
        df["Opportunity_Created_Date"])


""" Converts column to date"""


def _last_activity_correction(df):
    #df["Last_Activity"] = pd.to_datetime(df["Last_Activity"])
    return


""" Converts column to Datetime"""


def _quote_expiry_date_correction(df):
    df["Quote_Expiry_Date"] = pd.to_datetime(df["Quote_Expiry_Date"])


""" Converts column to Datetime"""


def _last_modified_date_correction(df):
    df["Last_Modified_Date"] = pd.to_datetime(df["Last_Modified_Date"])


""" Converts column to Datetime"""


def _planned_delivery_start_date_correction(df):
    df["Planned_Delivery_Start_Date"] = pd.to_datetime(
        df["Planned_Delivery_Start_Date"])


""" Converts column to Datetime"""


def _planned_delivery_end_date_correction(df):
    df["Planned_Delivery_End_Date"] = pd.to_datetime(
        df["Planned_Delivery_End_Date"])


""" Converts 'year - month' to (month, year)"""


def _month_correction(df):
    df["Month"] = df["Month"].map(lambda x: x.split(" "))
    df["Month"] = df["Month"].map(lambda x: (x[2], x[0]))  # (month, year)


""" Converts column to Datetime"""


def _actual_delivery_date_correction(df):
    #df["Actual_Delivery_Date"] = pd.to_datetime(df["Actual_Delivery_Date"])
    return

# INT SECTION


""" Converts None to nan"""


def _sales_contract_no_correction(df):
    df["Sales_Contract_No"] = pd.to_numeric(
        df["Sales_Contract_No"], errors="coerce")

# FLOAT SECTION


""" Converts None and Other to nan"""


def _price_correction(df):
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

# NAME SECTION


def _total_power_correction(df):
    df.rename(columns={"TRF": "Total_Power"}, inplace=True)


def _source_correction(df):
    df.rename(columns={"Source ": "Source"}, inplace=True)

# DELETE SECTION


def _last_activity_delete(df):
    df.drop(columns="Last_Activity", inplace=True)


def _actual_delivery_date_delete(df):
    df.drop(columns="Actual_Delivery_Date", inplace=True)


def _submitted_for_approval(df):
    df.drop(columns="Submitted_for_Approval", inplace=True)


def _product_category_a(df):
    df.drop(columns="Prod_Category_A", inplace=True)

# TO NUMERIC SECTION


def _bureaucratic_code_to_numeric(df):
    df["Bureaucratic_Code"] = df["Bureaucratic_Code"].str.replace(
        "Bureaucratic_Code_", "")
    df["Bureaucratic_Code"] = pd.to_numeric(df["Bureaucratic_Code"])


def _source_to_numeric(df):
    df["Source"] = df["Source"].str.replace("Source_", "")
    df["Source"] = pd.to_numeric(df["Source"], errors="coerce")


def _account_name_to_numeric(df):
    df["Account_Name"] = df["Account_Name"].str.replace("Account_Name_", "")
    df["Account_Name"] = pd.to_numeric(df["Account_Name"])


def _opportunity_name_to_numeric(df):
    df["Opportunity_Name"] = df["Opportunity_Name"].str.replace(
        "Opportunity_Name_", "")
    df["Opportunity_Name"] = pd.to_numeric(df["Opportunity_Name"])


def _account_owner_to_numeric(df):
    df["Account_Owner"] = df["Account_Owner"].str.replace("Person_Name_", "")
    df["Account_Owner"] = pd.to_numeric(df["Account_Owner"])


def _opportunity_owner_to_numeric(df):
    df["Opportunity_Owner"] = df["Opportunity_Owner"].str.replace(
        "Person_Name_", "")
    df["Opportunity_Owner"] = pd.to_numeric(df["Opportunity_Owner"])


def _account_type_to_numeric(df):
    df["Account_Type"] = df["Account_Type"].str.replace("Account_Type_", "")
    df["Account_Type"] = pd.to_numeric(df["Account_Type"], errors="coerce")


def _opportunity_type_to_numeric(df):
    df["Opportunity_Type"] = df["Opportunity_Type"].str.replace(
        "Opportunity_Type_", "")
    df["Opportunity_Type"] = pd.to_numeric(df["Opportunity_Type"])


def _delivery_terms_to_numeric(df):
    df["Delivery_Terms"] = df["Delivery_Terms"].str.replace(
        "Delivery_Terms_", "")
    df["Delivery_Terms"] = pd.to_numeric(df["Delivery_Terms"])


def _brand_to_numeric(df):
    df["Brand"] = df["Brand"].str.replace("Brand_", "")
    df["Brand"] = df["Brand"].str.replace("Other", "-1")
    df["Brand"] = pd.to_numeric(df["Brand"], errors="coerce")


def _product_type_to_numeric(df):
    df["Product_Type"] = df["Product_Type"].str.replace("Product_Type_", "")
    df["Product_Type"] = df["Product_Type"].str.replace("Other", "-1")
    df["Product_Type"] = pd.to_numeric(df["Product_Type"], errors="coerce")


def _last_modified_by_to_numeric(df):
    df["Last_Modified_By"] = df["Last_Modified_By"].str.replace(
        "Person_Name_", "")
    df["Last_Modified_By"] = pd.to_numeric(df["Last_Modified_By"])


def _product_family_to_numeric(df):
    df["Product_Family"] = df["Product_Family"].str.replace(
        "Product_Family_", "")
    df["Product_Family"] = pd.to_numeric(df["Product_Family"])


def _product_name_to_numeric(df):
    df["Product_Name"] = df["Product_Name"].str.replace("Product_Name_", "")
    df["Product_Name"] = pd.to_numeric(df["Product_Name"])
