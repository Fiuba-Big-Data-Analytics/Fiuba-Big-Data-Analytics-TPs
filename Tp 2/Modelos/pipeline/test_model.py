from utils.my_pipe import MyPipeline
from sklearn.model_selection import train_test_split
import pandas as pd

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

def add_one(X):
  X["mascota"] = X["mascota"] + 1
  return X

def main():
  X = pd.DataFrame(columns=['mascota', 'edad', 'sexo', 'estado'], data=[
  [1,50,1,'feliz'],
  [0,5,1,'triste'],
  [1,80,1,'triste'],
  [float("NaN"),80,1,'feliz'],
  [0,25,1,'feliz'],
  [1,39,1,'feliz'],
  [0,20,1,'triste'],
  [1,40,1,'feliz'],
  [0,78,1,'triste'],
  [1,25,1,'feliz'],
  [1,50,1,'triste'],
  [0,5,1,'triste'],
  [1,80,1,'triste'],
  [float("NaN"),80,1,'feliz'],
  [0,25,1,'feliz'],
  [1,39,1,'feliz'],
  [0,20,1,'triste'],
  [1,40,1,'feliz'],
  [0,78,1,'triste'],
  [1,25,1,'feliz']
  ])

  Y = X["estado"].apply(lambda x: 1 if x == 'feliz' else 0)
  X = X.drop("estado", axis=1)
  
  X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2, random_state=2)

  pipe = MyPipeline(X_train, X_test, Y_train, Y_test)

  pipe.set_model(RandomForestClassifier(random_state=0))
  pipe.set_folds(4)

  pipe.apply_imputation(["mascota"], "mean")
  pipe.apply_add_columns("mascota", "edad")
  pipe.apply_remove_columns(["mascota"])
  pipe.apply_function(add_one)

  pipe.preprocess()
  pipe.train()
  pipe.predict()
  pipe.score()
  pipe.output()

main()