import pandas as pd

df = pd.read_csv("data.csv")

df = df.dropna()

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

df["winner"] = le.fit_transform(df["winner"])

df.corrwith(df["winner"])

x = df.drop(columns = ["winner"])
y = df["winner"]

from sklearn.model_selection import train_test_split
x_train, x_test , y_train, y_test = train_test_split(x,y,test_size = 0.2)


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBClassifier

model = Pipeline([("ht", OneHotEncoder()), ("cc", RandomForestClassifier(n_estimators = 120, max_depth = 50))])



clff = RandomForestClassifier(n_estimators = 120, max_depth = 50)

model.fit(x_train,y_train)
y_pred = model.predict(x_test)

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
accuracy_score(y_test,y_pred)
cm = confusion_matrix(y_test,y_pred)

a = le.inverse_transform([3])
a[0]
