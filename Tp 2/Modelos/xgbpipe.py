import pandas as pd
import numpy as np
from pipeline.my_pipe import MyPipeline
from sklearn.ensemble import RandomForestClassifier

def apply_imputation_to_all(pipe, X):
  numerical_columns = list(X.select_dtypes(include=["float64", "int64"]).columns)
  numerical_columns.remove("ID")
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
  #print(X["Planned_Delivery_End_Date"])
  X["Planned_Delivery_Date_Diff"] = X['Planned_Delivery_End_Date'] - X['Planned_Delivery_Start_Date']
  return X

def sort_by_dates(X):
  X = X.sort_values(by="Opportunity_Created_Date")
  return X

def groupby_opp_id(X):
  X.drop_duplicates(subset="Opportunity_ID")
  return X

def dates_to_timestamp(X):
  X_dates = X.select_dtypes(include="datetime")
  for col in X_dates.columns:
    X[col] = X[col].astype(np.int64)
  X_timedeltas = X.select_dtypes(include="timedelta64")
  for col in X_timedeltas:
    X[col] = X[col].astype(np.int64)
  return X

def preprocess(pipe, X):
  pipe.apply_column_filter([
    "Quote_Expiry_Date", 
    "Last_Modified_Date",
    "ID",
    "Prod_Category_A",
    "Account_Created_Date",
    "Sales_Contract_No",
    "Opportunity_Name",
    "Last_Activity"
  ])
  preprocess_dates(pipe)
  apply_imputation_to_all(pipe, X)
  pipe.apply_labeling(["Quote_Type"])
  apply_one_hot_to_all(pipe, X)
  pipe.apply_function(preprocess_amounts)
  pipe.apply_function(preprocess_delivery_dates)
  pipe.apply_function(sort_by_dates)
  pipe.apply_function(dates_to_timestamp)
  pipe.apply_function(groupby_opp_id)
  columns_to_remove = [
    "Opportunity_Created_Date",
    "Planned_Delivery_Start_Date",
    "Planned_Delivery_End_Date",
    "Total_Taxable_Amount"
    ]
  pipe.apply_remove_columns(columns_to_remove)

def main():
  X_train = pd.read_csv("../Datos/Train_TP2_Datos_2020-2C.csv")
  X_test = pd.read_csv("../Datos/Test_TP2_Datos_2020-2C.csv")

  X_train = X_train.loc[(X_train["Stage"] == "Closed Won")|(X_train["Stage"] == "Closed Lost"),:]
  X_train["Stage"] = X_train['Stage'].apply(lambda x: 1 if x == 'Closed Won' else 0)

  y_train = X_train["Stage"]
  X_train = X_train.drop("Stage", axis=1)

  pipe = MyPipeline(X_train, X_test, y_train)

  preprocess(pipe, X_train)
  pipe.set_model(RandomForestClassifier(random_state=0))
  pipe.set_folds(10)

  pipe.preprocess()
  pipe.train()
  pipe.predict()

  pipe.score()
  pipe.output()

  print("TODO OK")

main()