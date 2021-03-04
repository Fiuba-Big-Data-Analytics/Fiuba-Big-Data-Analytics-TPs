import pandas as pd
from pipeline.my_pipe import MyPipeline
from util_functions import *

xgb_params = {
    "max_depth":4,
    "learning_rate":0.05,
    "n_estimators":250,
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
    #"Account_Created_Date",
    #
    "ID",                     # Useless
    "Submitted_for_Approval", # Empty
    "Opportunity_Name",       # Useless
    "Sales_Contract_No",      # Leakage
    "Last_Activity",          # No-Data
    "Prod_Category_A",        # No-Data
    "Account_Owner"           # Non-Representative Categories in Train-Set
    "Account_Name"            # Non-Representative Categories in Test-Set
    "Product_Name"            # Non-Representative Categories from Train-Set found in Test-Set
  ]

# Columnas Borradas al final
columns_removed = [
    "Opportunity_Created_Date",     # Leakage
    "Planned_Delivery_Start_Date",  # Engineered
    "Planned_Delivery_End_Date",    # Engineered
    "Total_Taxable_Amount",         # Replaced
    "Brand",                        # Anomalous
    "Product_Type",                 # Anomalous
    "Size",                         # Anomalous
    "Product_Category_B",           # Anomalous
    "Price",                        # Anomalous
    "Currency",                     # Anomalous
    "Last_Modified_Date",           # Engineered
    "Delivery_Year",                # Date
    "Pricing, Delivery_Terms_Quote_Appr",   # Checking
    "Pricing, Delivery_Terms_Approved",  # Checking
    "Bureaucratic_Code_0_Approved"  # Checking
    "Opportunity_ID"
  ]

#columns_to_label = [
#  "Quote_Type",
#]

columns_to_one_hot = [
    "Region",
    "Billing_Country",
    "Bureaucratic_Code",
    "Account_Type",
    "Opportunity_Type",
    "Delivery_Terms",
    "Product_Family",
    "Opportunity_Owner",
    "TRF",
  ] 

def preprocess(pipe, X):
  # Remove ignored columns
  pipe.apply_column_filter(columns_filtered)
  pipe.apply_pre_function(group_registers)
  pipe.apply_pre_function(prefix_columns)
  pipe.apply_pre_function(fill_nones)

  # Change types to correct value
  preprocess_dates(pipe)

  # Apply data filling
  impute_all(pipe, X, set(columns_filtered))
  #pipe.apply_labeling(columns_to_label)
  pipe.apply_one_hot(columns_to_one_hot)

  # Apply various functions
  pipe.apply_function(delete_old_registers)
  # 0.69 -> LOST -> 0.5 y LOST para Anomalos -> > 0.69 no es correcta la assumption / < 0.69 es parcialmente correcta
  #pipe.apply_function(delete_anomalous_registers)
  pipe.apply_function(insert_negotiation_length)
  pipe.apply_function(insert_client_age)
  pipe.apply_function(binary_quote_type)
  #pipe.apply_function(insert_trf_zero)
  pipe.apply_function(preprocess_amounts_blocks)
  pipe.apply_function(preprocess_delivery_dates)
  #pipe.apply_function(sort_by_dates)
  pipe.apply_function(unify_coins)
  pipe.apply_function(groupby_opp_id)
  pipe.apply_function(drop_categoricals)

  # Remove non-numerical columns
  pipe.apply_remove_columns(columns_removed)


def main():
  X_train = pd.read_csv("../Datos/Train_TP2_Datos_2020-2C.csv")
  X_test = pd.read_csv("../Datos/Test_TP2_Datos_2020-2C.csv")

  X_train = X_train.loc[(X_train["Stage"] == "Closed Won")|(X_train["Stage"] == "Closed Lost"),:]
  X_train["Stage"] = X_train['Stage'].apply(lambda x: 1 if x == 'Closed Won' else 0)
  
  pipe = MyPipeline(X_train, X_test)

  preprocess(pipe, X_train)
  set_xgb_model(pipe, xgb_params)
  pipe.set_time_folds(10)
  pipe.preprocess()
  pipe.train(verbose=True)
  #pipe.grid_search(verbose=True)
  pipe.predict()
  pipe.submit()
  pipe.score(verbose=True)
  #pipe.output()
  print("TODO OK")

main()

#0.47
#0.41

#0.5048
#0.416546