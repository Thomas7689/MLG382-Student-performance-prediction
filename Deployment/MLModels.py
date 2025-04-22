import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from category_encoders.target_encoder import TargetEncoder
from skopt import BayesSearchCV
from skopt.space import Real, Integer
from xgboost import XGBClassifier
import os



def ReadFile():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, '../Project 1/Student_performance_data.csv')
    df = pd.read_csv(file_path)
    df.drop(columns='StudentID', inplace=True)
    return df

def TrainModel(dataFrame, TrainOnColumns, typeOfModel, testSize = 0.2):
    categorical_columns = ['Gender', 'Ethnicity', 'ParentalEducation', 'Tutoring', 'ParentalSupport', 'Extracurricular', 'Sports', 'Music', 'Volunteering', 'GradeClass']
    for col in categorical_columns:
        dataFrame[col] = dataFrame[col].astype('category')
    targetColumn = dataFrame['GradeClass']
    otherColumns = dataFrame.drop(columns=targetColumn.name)
    otherColumns = otherColumns[TrainOnColumns]
    xTrain, xTest, yTrain, yTest = train_test_split(otherColumns, targetColumn, test_size=testSize, stratify=targetColumn, random_state=1)

    match typeOfModel:
        case 'XGBoost':
            estimators = [('encoder', TargetEncoder()),
              ('clf', XGBClassifier(random_state = 1))] #XGBRegressor for regression problem
            pipe = Pipeline(steps=estimators)
            searchSpace = {
            'clf__max_depth': Integer(2, 6),
            'clf__learning_rate': Real(0.001, 1.0, prior='log-uniform'),
            'clf__subsample': Real(0.5, 1.0),
            'clf__colsample_bytree': Real(0.5, 1.0),
            'clf__colsample_bylevel': Real(0.5, 1.0),
            'clf__colsample_bynode': Real(0.5, 1.0),
            'clf__reg_alpha': Real(0.0, 10.0),
            'clf__reg_lambda': Real(0.0, 10.0),
            'clf__gamma': Real(0.0, 10.0)
            }
            model = BayesSearchCV(pipe, searchSpace, cv=5, n_iter=20, scoring='roc_auc_ovr', random_state=1, refit=True)
            model.fit(xTrain, yTrain)
        case 'Random Forest':
            RFModel = RandomForestClassifier(random_state=1)
            searchSpace = {
                'max_depth': Integer(2, 6),
                'ccp_alpha': Real(0.0, 10.0),
                'n_estimators': Integer(10, 1000),
                'min_samples_split': Integer(2, 10),
                'min_samples_leaf': Integer(2, 10),
            }
            model = BayesSearchCV(estimator=RFModel, search_spaces=searchSpace, n_iter=20, cv=5, random_state=1)
            model.fit(xTrain, yTrain)
        case 'Logistic Regression':
            model = LogisticRegression(max_iter=2000)
            model.fit(xTrain, yTrain)   
        case 'Neural Network':
            model = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(5, 3), random_state=1, max_iter = 2000)
            model.fit(xTrain, yTrain)
    return model