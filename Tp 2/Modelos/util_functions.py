import numpy as np
import pandas as pd
from xgboost import XGBClassifier

from datetime import timedelta

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
  X = X.drop(["Total_Taxable_Amount","Total_Amount"], axis=1)
  return X

""" Sum Total_Amount into Total_Amount_Sum, truncating down to tens of thousands, dropping Total_Taxable_Amount."""
def preprocess_amounts_blocks(X):
  X["Total_Amount_Sum"] = X.groupby("Opportunity_ID")["Total_Amount"].transform("sum")
  X["Total_Amount_Sum"] = (X["Total_Amount_Sum"] // 10000) * 10000
  X = X.drop(["Total_Taxable_Amount","Total_Amount"], axis=1)

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

""" Delete old registers due to possible lack of full registers on the dataframe."""
def delete_old_registers(X):
  X = X.loc[X["Opportunity_Created_Date"] >= (np.datetime64("2015-01-01").astype(np.int64) // 10 ** 9) , :]
  return X

""" Deletes registers which weirdly have values and might corrupt the data."""
def delete_anomalous_registers(X):
  X = X.loc[X["Brand"] == "None",:]
  X = X.loc[X["Product_Type"] == "None", :]
  X = X.loc[X["Size"] == "None", :]
  X = X.loc[X["Product_Category_B"] == "None", :]
  X = X.loc[X["Price"] == "None", :]
  X = X.loc[X["Currency"] == "None", :]
  return X


""" Inserts a new column with negotiation length."""
def insert_negotiation_length(X):
  X["Negotiation_Length"] = X["Last_Modified_Date"] - X["Opportunity_Created_Date"]
  return X

""" Inserts a new column with negotiation length."""
def insert_client_age(X):
  X["Client_Age"] = X["Opportunity_Created_Date"] - X["Account_Created_Date"]
  X = X.drop("Account_Created_Date", axis=1)
  return X

""" Inserts a new column indicating whether TRF is Zero or not"""
def insert_trf_zero(X):
  X["TRF_Zero"] = X["TRF"].apply(lambda x: 0 if x == 0 else 1)
  return X

def concat_region_territory(X):
  X['reg_territory'] = X['Region'] + X['Territory']
  X = X.drop(columns = 'reg_territory')
  X = X.drop(columns = 'Territory')
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
    X[col] = X[col].astype(np.int64) // 10 ** 9
  X_timedeltas = X.select_dtypes(include="timedelta64")
  for col in X_timedeltas:
    X[col] = X[col].astype(np.int64) // 10 ** 9
  return X

def prefix_columns(X):
  columns_to_prefix = [
  "Region",
  "Territory",
  ]
  for col in columns_to_prefix:
    X[col] = X[col].apply(lambda x: col + "_" +x)
  return X

def fill_nones(X):
  X["Source "] = X["Source "].replace({"None": "Source_None"})
  X["Account_Type"] = X["Account_Type"].replace({"None": "Account_Type_None"})
  return X

def get_factor_estim_periodo(X, currency, date_in_row):
  date_window_begin = date_in_row - (np.timedelta64(30, "D").astype(np.int64) // 10 ** 9)
  date_window_end = date_in_row + (np.timedelta64(30, "D").astype(np.int64) // 10 ** 9)
  #print('buscando para: ', currency, date_in_row, date_window_begin, date_window_end)
  
  mask = ((X['Last_Modified_Date'] >= date_window_begin) | (X['Last_Modified_Date'] >= date_window_end)) & (X['ASP_Currency'] == currency) & (X['ASP_max'] > 0)
  #mask = (df['Last_Modified_Date'] > date_window_begin) & (df['Last_Modified_Date'] <= date_window_end)
  sdf = X.loc[mask]
  factor = sdf['ASP_(converted)_max'].mean() / sdf['ASP_max'].mean() 
  #print(factor, sdf['ASP_(converted)_max'].mean(), sdf['ASP_max'].mean() )
  #print(sdf[['ASP_Currency', 'ASP_(converted)_max', 'ASP_max']].head(10))
  #sub_df = df.loc[interval:'ASP_max']
  #print(sub_df)
  #print(sub_df.mean)

  # busca el valor pronedio de asp y asp_convert para $currency
  # dentro de una cierta ventana de tiempo entorno a $date_in_row
  
  return factor

def define_factor(X, a, b, currency, date_in_row):
  if (a == 0) or (a == np.nan) or  (b == 0) or (b == np.nan):
    return get_factor_estim_periodo(X, currency, date_in_row)
  else:
    return a / b


""" Unify all currencies to Dollar."""    
def unify_coins(X):
  X["ASP_max"] = X.groupby("Opportunity_ID")["ASP"].transform("max")
  X["ASP_(converted)_max"] = X.groupby("Opportunity_ID")["ASP_(converted)"].transform("max")
  X["rel_cnv_currency"] = X.apply(lambda x: define_factor(X, x["ASP_(converted)_max"], x['ASP_max'], x['ASP_Currency'], x['Last_Modified_Date']) , axis=1)
  X["Total_Amount_Sum"] = X["Total_Amount_Sum"] * X["rel_cnv_currency"]
  X = X.drop(["ASP_max", "ASP", "ASP_(converted)_max", "ASP_(converted)", "rel_cnv_currency", "ASP_Currency"], axis=1)
  return X
    

def binary_columns(X):
  X["Brand"] = X["Brand"].apply(lambda v: 1 if v=="None" else 0)
  X["Product_Type"] = X["Product_Type"].apply(lambda v: 1 if v=="None" else 0)
  X["Size"] = X["Size"].apply(lambda v: 1 if v=="None" else 0)
  X["Product_Category_B"] = X["Product_Category_B"].apply(lambda v: 1 if v=="None" else 0)
  X["Price"] = X["Price"].apply(lambda v: 1 if v=="None" else 0)
  X["Currency"] = X["Currency"].apply(lambda v: 1 if v=="None" else 0)
  return X