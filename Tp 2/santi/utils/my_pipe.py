import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import MissingIndicator
from sklearn.impute import SimpleImputer
from sklearn.model_selection import KFold
from sklearn.metrics import log_loss
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

def add_columns(X, columnA, columnB):
  X[f"add_{columnA}_{columnB}"] = X[columnA] + X[columnB]
  return X

def substract_columns(X, columnA, columnB):
  X[f"sub_{columnA}_{columnB}"] = X[columnA] - X[columnB]
  return X

def drop_columns(X, columns):
  X.drop(columns, inplace=True, axis=1)
  return X
  
def impute_columns(X, columns, strategy):
  imputer = ColumnTransformer([("imputer", SimpleImputer(strategy=strategy), columns)],remainder="passthrough")
  imputed = pd.DataFrame(imputer.fit_transform(X))
  imputed.columns = X.columns
  imputed.index = X.index
  return imputed

def one_hot_columns(X, columns):
  onehotter = OneHotEncoder(handle_unknown="ignore", sparse=False)
  onehotted = pd.DataFrame(onehotter.fit_transform(X[columns]))
  onehotted.index = X.index
  dropped_X = X.drop(columns, axis=1)
  X = pd.concat([dropped_X,onehotted], axis=1)
  return X

def label_columns(X, columns):
  labeler = LabelEncoder()
  for col in columns:
    X[col] = labeler.fit_transform(X[col])
  return X

class MyPipeline:
  def __init__(self, X_train, X_test, y_train, y_test):
    # Sets
    self.X_train = X_train
    self.y_train = y_train
    self.X_test = X_test
    self.y_test = y_test

    # Meta Data
    versions_results = pd.read_csv("log_file.csv")
    self.version = versions_results["version"].max() + 1

    # Preprocessing
    self.columns_to_remove = []

    self.columns_to_impute = {}
    self.columns_to_extend_imputation = set()

    self.columns_to_label = {}
    self.columns_to_one_hot = []

    self.columns_to_substract = []
    self.columns_to_add = []
    self.functions_to_apply = []

    # Model
    self.model = None
    self.prediction = []
    self.error = None
    self.folds = 1


  """ Receives a list of columns to impute and a strategy and adds them to the pipeline."""
  def apply_imputation(self, columns, strategy):
    if strategy in self.columns_to_impute:
      self.columns_to_impute[strategy].extend(columns)
    else:
      self.columns_to_impute[strategy] = columns

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
    self.folds = k


  """ Sets the model used."""
  def set_model(self, model):
    self.model = model


  """ Execute all the preprocessing."""
  def preprocess(self):
    for strat,cols in self.columns_to_impute.items():
      self.X_train = impute_columns(self.X_train, cols, strat)
      self.X_test = impute_columns(self.X_test, cols, strat)
    
    self.X_train = label_columns(self.X_train, self.columns_to_label)
    self.X_test = label_columns(self.X_test, self.columns_to_label)

    self.X_train = one_hot_columns(self.X_train, self.columns_to_one_hot)
    self.X_test = one_hot_columns(self.X_test, self.columns_to_one_hot)

    for cols in self.columns_to_add:
      self.X_train = add_columns(self.X_train, *cols)
      self.X_test = add_columns(self.X_test, *cols)

    for function in self.functions_to_apply:
      self.X_train = function(self.X_train)
      self.X_test = function(self.X_test)

    self.X_train = drop_columns(self.X_train, self.columns_to_remove)
    self.X_test = drop_columns(self.X_test, self.columns_to_remove)

    self.X_train.reset_index(drop=True, inplace=True)
    self.X_test.reset_index(drop=True, inplace=True)
    self.y_train.reset_index(drop=True, inplace=True)
    self.y_test.reset_index(drop=True, inplace=True)


  """ Train the model."""
  def train(self):
    self.model.fit(self.X_train, self.y_train)


  """ Generate the prediction."""
  def predict(self):
    self.prediction = self.model.predict_proba(self.X_test)


  """ Score the model."""
  def score(self):
    if self.folds == 1:
      prediction = self.model.predict_proba(self.X_train)
      self.error = log_loss(self.y_train, prediction)
    else:
      self.X_train.reset_index(drop=True, inplace=True)
      self.y_train.reset_index(drop=True, inplace=True)
      folds = KFold(n_splits=self.folds)
      errors = []
      for train_index, test_index  in folds.split(self.X_train):
        X_train = self.X_train.loc[train_index,:] 
        y_train = self.y_train.loc[train_index]
        X_test = self.X_train.loc[test_index,:]
        y_test = self.y_train.loc[test_index]
        self.model.fit(X_train,y_train)
        prediction = self.model.predict_proba(X_test)
        try:
          errors.append(log_loss(y_test, prediction))
        except ValueError:
          raise ValueError("Todos los valores de y_true son iguales")

      self.error = sum(errors) / len(errors)


  """ Print the model information."""
  def output(self):     
    with open(f"full_results/v{self.version}", "w+") as result_file:
      result_file.write(f"Versión {self.version} - XGBoost\n")
      result_file.write("\n")
      result_file.write(f"Puntaje Estimado: {self.error}\n")
      result_file.write("\n")
      result_file.write("Hiperparametros:\n")
      result_file.write(f"Folds: {self.folds}\n")
      result_file.write("\n")
    
    with open("log_file.csv", "a+") as log_file:
      log_file.write(f"{self.version},{self.error:.3f}\n")
