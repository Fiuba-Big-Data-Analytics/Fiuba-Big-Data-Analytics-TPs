import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import MissingIndicator
from sklearn.impute import SimpleImputer
from sklearn.model_selection import KFold
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import log_loss
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

def to_date(X, column):
  X[column] = pd.to_datetime(X[column], format="%m/%d/%Y")
  X[column] = X[column].astype(np.int64) // 10 ** 9 
  return X

def add_columns(X, columnA, columnB):
  X[f"add_{columnA}_{columnB}"] = X[columnA] + X[columnB]
  return X

def substract_columns(X, columnA, columnB):
  X[f"sub_{columnA}_{columnB}"] = X[columnA] - X[columnB]
  return X
  
def impute_columns(X, columns, strategy, fill_value=None):
  imputer = SimpleImputer(strategy=strategy, fill_value=fill_value)
  imputed = pd.DataFrame(imputer.fit_transform(X[columns]))
  imputed.columns = columns
  imputed.index = X.index
  dropped_X = X.drop(columns, axis=1)
  X = pd.concat([imputed,dropped_X], axis=1)
  return X

def one_hot_columns(X, columns):
  onehotter = OneHotEncoder(handle_unknown="ignore", sparse=False)
  onehotted = pd.DataFrame(onehotter.fit_transform(X[columns]))
  onehotted.index = X.index
  onehotted.columns = onehotter.get_feature_names()
  dropped_X = X.drop(columns, axis=1)
  X = pd.concat([dropped_X,onehotted], axis=1)
  return X

def label_columns(X, columns):
  labeler = LabelEncoder()
  for col in columns:
    X[col] = labeler.fit_transform(X[col])
  return X

def drop_columns(X, columns):
  existing_columns = [col for col in columns if col in X]
  X = X.drop(existing_columns, axis=1)
  return X

""" Prints the feature importance, undoing OneHot, without knowledge of original cardinality."""
def output_importances(fimps, results_file):
  fimp_list = []
  fimp_dict = {}
  for feature, importance in fimps.items():
    if feature[0] != "x": # OneHotEncoder adds an x at the beginning, so this is not categorical
      fimp_list.append((feature, importance))
    else:
      sufix_pos = -1
      while feature[sufix_pos] != "_":
        sufix_pos -= 1
      feat_name = feature[3:sufix_pos]
      if feat_name in fimp_dict:
        fimp_dict[feat_name].append(importance)
      else:
        fimp_dict[feat_name] = [importance]
  for feature, importances in fimp_dict.items():
    importance = sum(importances) / len(importances)
    fimp_list.append((feature, importance))
  fimp_list.sort(key=lambda x: -x[1])
  for f in fimp_list:
    results_file.write(f"{f[0]}: {f[1]:.3f}\n")


class MyPipeline:
  def __init__(self, X_train, X_test):
    # Sets
    self.X_train = X_train
    self.X_test = X_test
    self.y_train = None
    self.X_valid = None
    self.y_valid = None

    # Meta Data
    versions_results = pd.read_csv("../log_file.csv")
    self.version = versions_results["version"].max() + 1

    # Preprocessing
    self.pre_functions_to_apply = []
    self.columns_to_date = []

    self.columns_to_filter = []
    self.columns_to_remove = []

    self.columns_to_impute = {}
    self.columns_to_extend_imputation = set()

    self.columns_to_label = set()
    self.columns_to_one_hot = []

    self.columns_to_substract = []
    self.columns_to_add = []
    self.functions_to_apply = []

    # Model
    self.model = None
    self.params = {}
    self.target = "Stage"
    self.prediction = []
    self.error = None
    self.folds = 1


  def apply_pre_function(self, function):
    self.pre_functions_to_apply.append(function)

  def apply_column_filter(self, columns):
    self.columns_to_filter.extend(columns)


  def apply_to_date(self, columns):
    self.columns_to_date.extend(columns)


  """ Receives a list of columns to impute and a strategy and adds them to the pipeline."""
  def apply_imputation(self, columns, strategy, fill_value=None):
    key_cols = tuple(columns)
    self.columns_to_impute[key_cols] = (strategy,fill_value)

  """ Receives a list of columns to label and adds them to the pipeline."""
  def apply_labeling(self, columns):
    self.columns_to_label.update(columns)

  
  """ Receives a list of columns to one hot and adds them to the pipeline."""
  def apply_one_hot(self,columns):
    self.columns_to_one_hot.extend(columns)


  """ Receives two columns to add and adds them to the pipeline."""
  def apply_add_columns(self, columnA, columnB):
    self.columns_to_add.append((columnA, columnB))


  """ Receives two columns to substract and adds them to the pipeline."""
  def apply_substract_columns(self, columnA, columnB):
    self.columns_to_substract.append((columnA, columnB))


  """ Receives a list of columns to remove and adds them to the pipeline."""
  def apply_remove_columns(self, columns):
    self.columns_to_remove.extend(columns)

  
  """ Receives a function to call and adds them to the pipeline."""
  def apply_function(self, function):
    self.functions_to_apply.append(function)


  """ Sets the amount of folds for cross-validation scoring."""    
  def set_folds(self, k):
    self.folds = KFold(n_splits=k)


  """ Sets the amount of time folds for cross-validation scoring."""    
  def set_time_folds(self, k):
    self.folds = TimeSeriesSplit(n_splits=k)

  """ Sets the model used."""
  def set_model(self, model):
    self.model = model


  def set_params(self, params):
    self.params = params


  """ Execute all the preprocessing."""
  def preprocess(self):
    self.X_train = drop_columns(self.X_train, self.columns_to_filter)
    self.X_test = drop_columns(self.X_test, self.columns_to_filter)

    for function in self.pre_functions_to_apply:
      self.X_train = function(self.X_train)
      self.X_test = function(self.X_test)
    
    for col in self.columns_to_date:
      self.X_train = to_date(self.X_train, col)
      self.X_test = to_date(self.X_test, col)

    for cols, strat in self.columns_to_impute.items():
      self.X_train = impute_columns(self.X_train, list(cols), strat[0], strat[1])
      self.X_test = impute_columns(self.X_test, list(cols), strat[0], strat[1])
              
    self.X_train = label_columns(self.X_train, self.columns_to_label)
    self.X_test = label_columns(self.X_test, self.columns_to_label)

    self.X_train = one_hot_columns(self.X_train, self.columns_to_one_hot)
    self.X_test = one_hot_columns(self.X_test, self.columns_to_one_hot)

    for function in self.functions_to_apply:
      self.X_train = function(self.X_train)
      self.X_test = function(self.X_test)

    self.X_train = drop_columns(self.X_train, self.columns_to_remove)
    self.X_test = drop_columns(self.X_test, self.columns_to_remove)

    self.X_train.to_csv("train_pre.csv")
    self.X_test.to_csv("test_pre.csv")

    self.X_train.reset_index(drop=True, inplace=True)
    self.X_test.reset_index(drop=True, inplace=True)

    return


  """ Train the model."""
  def train(self, verbose=False):
    self.y_train = self.X_train[self.target]
    self.X_train = self.X_train.drop(self.target, axis=1)
    ids = self.X_train["Opportunity_ID"]
    self.X_train = self.X_train.drop("Opportunity_ID", axis=1)
    if verbose: print("Fitting... 0%")
    self.model.fit(self.X_train, self.y_train)
    self.X_train["Opportunity_ID"] = ids
    if verbose: print("Fitting... 100%")

  """ Train an XGB model."""
  def train_xgb(self, verbose=False):
    self.y_train = self.X_train[self.target]
    self.X_train = self.X_train.drop(self.target, axis=1)

    valid_size = int(len(self.X_train.index) * 0.20)
    self.X_valid = self.X_train.tail(valid_size)
    self.X_train = self.X_train.drop(self.X_train.tail(valid_size).index)

    self.y_valid = self.y_train.tail(valid_size)
    self.y_train = self.y_train.drop(self.y_train.tail(valid_size).index)

    if verbose: print("Fitting... 0%")
    self.model = self.model.fit(
      self.X_train, self.y_train,
      early_stopping_rounds=3,
      eval_set=[(self.X_valid, self.y_valid)],
      verbose=verbose
    )
    if verbose: 
      print(f"Score: {self.model.best_score} --- Iter: {self.model.best_iteration} --- ntree-limit: {self.model.best_ntree_limit}")

  """ Generate the prediction."""
  def predict(self):
    self.prediction = self.model.predict_proba(self.X_test)


  """ Score the model."""
  def score(self, verbose=False):
    if self.folds == 1:
      prediction = self.model.predict_proba(self.X_train)
      self.error = log_loss(self.y_train, prediction)
    else:
      self.X_train.reset_index(drop=True, inplace=True)
      self.y_train.reset_index(drop=True, inplace=True)
      errors = []
      for train_index, test_index  in self.folds.split(self.X_train):
        X_train = self.X_train.loc[train_index,:] 
        y_train = self.y_train.loc[train_index]
        X_test = self.X_train.loc[test_index,:]
        y_test = self.y_train.loc[test_index]
        #ids = X_train["Opportunity_ID"]
        #X_train = X_train.drop("Opportunity_ID", axis=1)
        self.model.fit(X_train,y_train)
        #X_train["Opportunity_ID"] = ids
        
        prediction = self.model.predict_proba(X_test)
        try:
          errors.append(log_loss(y_test, prediction))
          if verbose: print(f"FOLD {len(errors)} --- Score: {errors[-1]}")
        except ValueError:
          raise ValueError("Todos los valores de y_true son iguales")

      self.error = sum(errors) / len(errors)
    if verbose: print(f"Score: {self.error}")


  def score_2(self):
    self.y_train = self.X_train[self.target]
    self.X_train = self.X_train.drop(self.target, axis=1)

    valid_size = int(len(self.X_train.index) * 0.20)
    self.X_valid = self.X_train.tail(valid_size)
    self.X_train = self.X_train.drop(self.X_train.tail(valid_size).index)

    self.y_valid = self.y_train.tail(valid_size)
    self.y_train = self.y_train.drop(self.y_train.tail(valid_size).index)

    self.model.fit(self.X_train, self.y_train)
    predictions = self.model.predict_proba(self.X_valid)
    error = log_loss(self.y_valid, predictions)
    print(error)

  def score_xgb(self, verbose=False):
    self.error = self.model.best_score
    if verbose: print(f"Score: {self.error}")

  def grid_search(self, gs, verbose=False):
    pass

  """ Print the model information."""
  def output(self):     
    with open(f"../full_results/v{self.version}", "w+") as result_file:
      result_file.write(f"Versión {self.version} - XGBoost\n")
      result_file.write("\n")
      result_file.write(f"Puntaje Estimado: {self.error}\n")
      result_file.write("\n")
      result_file.write(f"Folds: {self.folds}\n")
      result_file.write("\n")
      result_file.write("Hiperparametros:\n")
      for param,value in self.params.items():
        result_file.write(f"{param}: {value}\n")
      result_file.write("\n")

      output_importances(self.model.get_booster().get_score(importance_type="gain"), result_file)

    
    with open("../log_file.csv", "a+") as log_file:
      log_file.write(f"{self.version},{self.error:.3f}\n")

  """ Write a file to submit."""
  def submit(self):
    submit_file_name = f"../submits/v{self.version}.csv"

    df = pd.DataFrame(columns=["Opportunity_ID", "Target"])
    df["Opportunity_ID"] = self.X_test["Opportunity_ID"].astype(np.int64)
    df["Target"] = self.prediction
    df = df.sort_values(by=["Opportunity_ID"])
    df.to_csv(submit_file_name, index=False)