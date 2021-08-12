import pickle
import numpy as np
import pandas as pd

global __model

with open('static/diabetes_detector.pickle','rb') as f:
    __model = pickle.load(f)

def predict(l):
    l = pd.DataFrame(l, columns =['Glucose', 'BloodPressure','Insulin','BMI','Age'])
    val = __model.predict_proba(l[0:1])
    return list(val[0])[1]

#print(predict([[89,40,0,23.3,56]]))