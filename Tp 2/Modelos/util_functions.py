import numpy as np
import pandas as pd

def apply_imputation_to_all(pipe, X):
  numerical_columns = list(X.select_dtypes(include=["float64", "int64"]).columns)
  numerical_columns.remove("Stage")
  pipe.apply_imputation(numerical_columns, "mean")
  date_columns = list(X.select_dtypes(include="datetime64").columns)
  pipe.apply_imputation(date_columns, "mean")

def apply_one_hot_to_all(pipe, X):
  categoric_columns = list(X.select_dtypes(include=object).columns)
  pipe.apply_remove_columns(categoric_columns)

def preprocess_amounts(X):
  X["Total_Amount_Sum"] = X.groupby("Opportunity_ID")["Total_Amount"].transform("sum")
  X = X.drop("Total_Taxable_Amount", axis=1)
  return X

def preprocess_dates(pipe):
  columns_to_date = [
    'Planned_Delivery_Start_Date',
    'Planned_Delivery_End_Date',
    'Opportunity_Created_Date',
  ]
  pipe.apply_to_date(columns_to_date)
  
def preprocess_delivery_dates(X):
  X["Planned_Delivery_Date_Diff"] = X['Planned_Delivery_End_Date'] - X['Planned_Delivery_Start_Date']
  return X

def sort_by_dates(X):
  X = X.sort_values(by="Opportunity_Created_Date")
  return X

def groupby_opp_id(X):
  X = X.drop_duplicates(subset="Opportunity_ID")
  return X

def dates_to_timestamp(X):
  X_dates = X.select_dtypes(include="datetime")
  for col in X_dates.columns:
    X[col] = X[col].astype(np.int64)
  X_timedeltas = X.select_dtypes(include="timedelta64")
  for col in X_timedeltas:
    X[col] = X[col].astype(np.int64)
  return X