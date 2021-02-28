import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import log_loss
from sklearn.model_selection import cross_val_score

class EasyPipeline:
  # Meta-Data
  # version -> int
  
  # Preprocessing
  # columns_to_remove -> pd.Series
  # columns_to_impute -> pd.Series
  # columns_to_extend_imputation -> set
  # columns_to_label -> pd.Series
  # columns_to_one_hot -> pd.Series

  def __init__(self, x_train, x_test, y_train, y_test):
    # Tests
    self.x_train = x_train
    self.y_train = x_train
    self.x_test = x_test
    self.y_test = y_test

    # Meta Data
    versions_results = pd.read_csv("results.csv")
    self.version = versions_results["version"].max()

    # Preprocessing
    self.columns_to_remove = []

    self.columns_to_impute = {}
    self.columns_to_extend_imputation = set()

    self.columns_to_label = []
    self.columns_to_one_hot = []

    # Model
    self.folds = 1
    self.prediction = []

    
  def remove_column(self, column):
    self.columns_to_remove.append(column)


  def impute_column(self, column, strategy, extend=False):
    self.columns_to_impute[column] = strategy
    if (extend):
      self.columns_to_extend_imputation.add(column)


  def label_column(self, column):
    self.columns_to_label.append(column)


  def one_hot_column(self, column):
    self.columns_to_one_hot.append(column)

  def set_folds(self, k):
    self.folds = k


  def build_preprocessor(self):
    transformers = []

    for col, strat in self.columns_to_impute.items():
      imputer = SimpleImputer(strategy=strat)
      estimator_name = "imp" + col
      transformers.append((estimator_name, imputer, col))

    return transformers
  

  def fit(self):
    preprocessor_transformers = self.build_preprocessor()

    preprocessor = ColumnTransformer(transformers=preprocessor_transformers, remainder="passthrough")
    model = DecisionTreeRegressor(random_state=0)

    self.pipeline = Pipeline(steps=[("preprocessor", preprocessor),("model", model)])
    self.pipeline.fit(self.x_train, self.y_train)


  def predict(self):

    """
    if self.folds == 1:
      prediction = self.pipeline.predict(self.x_train)
      #print(self.y_train.head())
      log_loss(self.y_train, prediction)
    else:
      predicted_scores = -1 * cross_val_score(self.pipeline, self.x_train, self.y_train, cv=self.folds, scoring="neg_log_loss")
      self.score = predicted_scores.mean()"""


  
  def output(self): 
    print(self.prediction)
    
    with open(f"../full_results/v{self.version}", "w+") as result_file:
      result_file.write(f"Versión {self.version} - XGBoost\n")
      result_file.write("\n")
      result_file.write(f"Puntaje Estimado: {self.score}\n")
      result_file.write("\n")
      result_file.write("Hiperparametros:\n")
      result_file.write(f"Folds: {self.folds}\n")
      result_file.write("\n")

    
