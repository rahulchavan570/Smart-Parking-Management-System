import pandas as pd
from sklearn.tree import DecisionTreeClassifier

def predict_parking(hour):
    # Historical Data: Hour of day vs. Is it usually full?
    # 0 = Available, 1 = Full
    data = {
        'hour': [0, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 23],
        'is_full': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }
    
    df = pd.DataFrame(data)

    # ML Algorithm
    X = df[['hour']] 
    y = df['is_full']
    
    model = DecisionTreeClassifier()
    model.fit(X, y) # AI training happens here

    prediction = model.predict([[hour]])
    return "FULL" if prediction[0] == 1 else "AVAILABLE"