import pandas as pd
from pipeline.my_pipe import MyPipeline
from util_functions import *

xgb_params = {
    "max_depth":3,
    "learning_rate":0.1,
    "n_estimators":100,
    "objective":'binary:logistic',
    "booster":'gbtree',
    "n_jobs":1,
    "nthread":None,
    "gamma":0,
    "min_child_weight":1,
    "max_delta_step":0,
    "subsample":1,
    "colsample_bytree":1,
    "colsample_bylevel":1,
    "reg_alpha":0,
    "reg_lambda":1,
    "scale_pos_weight":1,
    "base_score":0.5,
    "random_state":0,
    "seed":None,
    "missing":None,
    "use_label_encoder":False,
    "eval_metric":"logloss"
  } 

# Columnas Borradas al Comienzo
columns_filtered = [
    #"Quote_Expiry_Date", 
    #"Last_Modified_Date",
    #"Prod_Category_A",
    #"Account_Created_Date",
    #"Last_Activity",
    #
    "Price",                  # Empty
    "ID",                     # Useless
    "Submitted_for_Approval", # Empty
    "Opportunity_Name",       # Useless
    "Sales_Contract_No",      # Leakage
  ]

# Columnas Borradas al final
columns_removed = [
    "Opportunity_Created_Date",     # Leakage
    "Planned_Delivery_Start_Date",  # Engineered
    "Planned_Delivery_End_Date",    # Engineered
    "Total_Taxable_Amount",         # Replaced
    "Account_Name"                  # High Cardinality
  ]

columns_to_label = [
  "Quote_Type"
]

columns_to_one_hot = [
    "Region",
    "Bureaucratic_Code",
    "Billing_Country",
    "Account_Owner",
    "Opportunity_Owner",
    "Account_Type",
    "Opportunity_Type"
  ]

def preprocess(pipe, X):
  # Remove ignored columns
  pipe.apply_column_filter(columns_filtered)

  # Change types to correct value
  preprocess_dates(pipe)

  # Apply data filling
  impute_all(pipe, X, set(columns_filtered))
  pipe.apply_labeling(columns_to_label)
  pipe.apply_one_hot(columns_to_one_hot)

  # Apply various functions
  pipe.apply_function(preprocess_amounts)
  pipe.apply_function(preprocess_delivery_dates)
  pipe.apply_function(sort_by_dates)
  pipe.apply_function(dates_to_timestamp)
  pipe.apply_function(groupby_opp_id)  
  pipe.apply_function(drop_datetimes)
  pipe.apply_function(drop_categoricals)


  pipe.apply_remove_columns(columns_removed)


def main():
  X_train = pd.read_csv("../Datos/Train_TP2_Datos_2020-2C.csv")
  X_test = pd.read_csv("../Datos/Test_TP2_Datos_2020-2C.csv")

  X_train = X_train.loc[(X_train["Stage"] == "Closed Won")|(X_train["Stage"] == "Closed Lost"),:]
  X_train["Stage"] = X_train['Stage'].apply(lambda x: 1 if x == 'Closed Won' else 0)

  pipe = MyPipeline(X_train, X_test)

  preprocess(pipe, X_train)
  set_xgb_model(pipe, xgb_params)
  pipe.set_folds(20)

  pipe.preprocess()
  pipe.train()
  pipe.predict()

  pipe.score(verbose=True)
  #pipe.output()
  #pipe.submit()
  print("TODO OK")

main()
