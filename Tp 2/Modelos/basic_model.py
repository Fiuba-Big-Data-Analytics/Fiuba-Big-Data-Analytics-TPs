import pandas as pd
from pipeline.my_pipe import MyPipeline
from sklearn.ensemble import RandomForestClassifier
from util_functions import *

def preprocess(pipe, X):
  pipe.apply_column_filter([
    "Quote_Expiry_Date", 
    "Last_Modified_Date",
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
    "Total_Taxable_Amount",
    "ID",
    ]
  pipe.apply_remove_columns(columns_to_remove)


def main():
  X_train = pd.read_csv("../Datos/Train_TP2_Datos_2020-2C.csv")
  X_test = pd.read_csv("../Datos/Test_TP2_Datos_2020-2C.csv")

  X_train = X_train.loc[(X_train["Stage"] == "Closed Won")|(X_train["Stage"] == "Closed Lost"),:]
  X_train["Stage"] = X_train['Stage'].apply(lambda x: 1 if x == 'Closed Won' else 0)

  pipe = MyPipeline(X_train, X_test)

  preprocess(pipe, X_train)
  pipe.set_model(RandomForestClassifier(max_depth=21, max_features=13, n_estimators=31,
                      random_state=123))
  pipe.set_folds(10)

  pipe.preprocess()
  pipe.train()
  pipe.predict()

  #pipe.score(verbose=True)
  #pipe.output()
  pipe.submit()
  print("TODO OK")

main()
