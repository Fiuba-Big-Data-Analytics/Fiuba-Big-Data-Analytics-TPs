import numpy as np
import pandas as pd
from xgboost import XGBClassifier

""" Receives a pipe and a dict with all params and sets the model to the pipe."""
def set_xgb_model(pipe, xgb_params):
  """my_xgb = XGBClassifier(
    max_depth=xgb_params["max_depth"],
    learning_rate=xgb_params["learning_rate"],
    n_estimators=xgb_params["n_estimators"],
    objective=xgb_params["objective"],
    booster=xgb_params["booster"],
    n_jobs=xgb_params["n_jobs"],
    nthread=xgb_params["nthread"],
    gamma=xgb_params["gamma"],
    min_child_weight=xgb_params["min_child_weight"],
    max_delta_step=xgb_params["max_delta_step"],
    subsample=xgb_params["subsample"],
    colsample_bytree=xgb_params["colsample_bytree"],
    colsample_bylevel=xgb_params["colsample_bylevel"],
    reg_alpha=xgb_params["reg_alpha"],
    reg_lambda=xgb_params["reg_lambda"],
    scale_pos_weight=xgb_params["scale_pos_weight"],
    base_score=xgb_params["base_score"],
    random_state=xgb_params["random_state"],
    seed=xgb_params["seed"],
    missing=xgb_params["missing"],
    use_label_encoder=xgb_params["use_label_encoder"],
    eval_metric=xgb_params["eval_metric"]
  )"""
  my_xgb = XGBClassifier(**xgb_params)
  pipe.set_model(my_xgb)
  pipe.set_params(xgb_params)

def impute_all(pipe, X, filtered_columns):
  impute_numericals(pipe, X, filtered_columns)
  impute_datetimes(pipe, X, filtered_columns)
  impute_source(pipe, X)

def impute_numericals(pipe, X, filtered_columns):
  numerical_columns = list(X.select_dtypes(include=["float64", "int64"]).columns)
  numerical_columns = [col for col in numerical_columns if col not in filtered_columns]
  numerical_columns.remove("Stage")
  pipe.apply_imputation(numerical_columns, "mean")

def impute_datetimes(pipe, X, filtered_columns):
  date_columns = [
    "Account_Created_Date",
    'Planned_Delivery_Start_Date',
    'Planned_Delivery_End_Date',
    'Opportunity_Created_Date',
    "Quote_Expiry_Date"
  ]
  date_columns = [col for col in date_columns if col not in filtered_columns]
  pipe.apply_imputation(date_columns, "mean")

def impute_source(pipe, X):
  pipe.apply_imputation(["Source "], "constant", fill_value="Source_0")

""" Applies one hot to all categorical columns. DANGER. Will crash the PC."""
def apply_one_hot_to_all(pipe, X):
  categoric_columns = list(X.select_dtypes(include=object).columns)
  pipe.apply_one_hot(categoric_columns)

""" Drops all categorical columns."""
def drop_categoricals(X):
  categoric_columns = list(X.select_dtypes(include=object).columns)
  X = X.drop(categoric_columns, axis=1)
  return X

def drop_datetimes(X):
  datetimes_columns = list(X.select_dtypes(include="datetime"))
  X = X.drop(datetimes_columns, axis=1)
  return X

""" Sum Total_Amount into Total_Amount_Sum, dropping Total_Taxable_Amount."""
def preprocess_amounts(X):
  X["Total_Amount_Sum"] = X.groupby("Opportunity_ID")["Total_Amount"].transform("sum")
  X = X.drop("Total_Taxable_Amount", axis=1)
  return X

""" Converts desired columns to datetime."""
def preprocess_dates(pipe):
  columns_to_date = [
    "Account_Created_Date",
    'Planned_Delivery_Start_Date',
    'Planned_Delivery_End_Date',
    'Opportunity_Created_Date',
    "Quote_Expiry_Date",
    "Last_Modified_Date"
  ]
  pipe.apply_to_date(columns_to_date)
  
""" Create column from substracting 2 columns."""
def preprocess_delivery_dates(X):
  X["Planned_Delivery_Date_Diff"] = X['Planned_Delivery_End_Date'] - X['Planned_Delivery_Start_Date']
  return X

""" Sort the DataFrame by Date."""
def sort_by_dates(X):
  X = X.sort_values(by="Opportunity_Created_Date")
  return X

""" Drops duplicates of Opportunity_ID."""
def groupby_opp_id(X):
  X = X.drop_duplicates(subset="Opportunity_ID")
  return X

""" Converts dates to int."""
def dates_to_timestamp(X):
  X_dates = X.select_dtypes(include="datetime")
  for col in X_dates.columns:
    X[col] = X[col].astype(np.int64)
  X_timedeltas = X.select_dtypes(include="timedelta64")
  for col in X_timedeltas:
    X[col] = X[col].astype(np.int64)
  return X

def binary_columns(X):
  X["Brand"] = X["Brand"].apply(lambda v: 1 if v=="None" else 0)
  X["Product_Type"] = X["Product_Type"].apply(lambda v: 1 if v=="None" else 0)
  X["Size"] = X["Size"].apply(lambda v: 1 if v=="None" else 0)
  X["Product_Category_B"] = X["Product_Category_B"].apply(lambda v: 1 if v=="None" else 0)
  X["Price"] = X["Price"].apply(lambda v: 1 if v=="None" else 0)
  X["Currency"] = X["Currency"].apply(lambda v: 1 if v=="None" else 0)
  return X