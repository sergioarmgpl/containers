import pandas as pd
from sklearn import tree
from joblib import dump

df = pd.read_csv("safety_rules.csv",sep=',', header='infer', encoding='latin-1')
df = df.drop(['object'], axis=1)
df.head()

feature_cols = ["n"]
X = df.loc[:, feature_cols]
y = df.warning_level

clf = tree.DecisionTreeRegressor()
model = clf.fit(X, y)

dump(clf, 'safety_rules.model') 

#a = model.predict([[6]])
#print(a[0])