# -*- coding: utf-8 -*-
"""Random_Forest_Ensemble_Stacking_RIP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-kdW_R9yoUeN3CvbJkmIZ33fi_snpRKq

#### Handling Imbalanced Dataset with Machine Learning
"""

import pandas as pd
df=pd.read_csv('ais_disabling_events_main_only_imp_col_csv.csv')
df.head()

df.shape

df['iuu_caught'].value_counts()

#### Independent and Dependent Features
X=df.drop("iuu_caught",axis=1)
y=df.iuu_caught

"""### One Hot Encoding"""

print(df['vessel_class'].unique())
print(df['Ocean List New whose false were in OG'].unique())

print(df['vessel_class'].value_counts())
print(df['Ocean List New whose false were in OG'].value_counts())

one_hot_encoded_data = pd.get_dummies(df, columns = ['vessel_class', 'Ocean List New whose false were in OG'])
print(one_hot_encoded_data.head())

#### Independent and Dependent Features
X=one_hot_encoded_data.drop("iuu_caught",axis=1)
y=one_hot_encoded_data.iuu_caught

"""#### SMOTETomek"""

y.value_counts()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=15, stratify=y)

from imblearn.over_sampling import SMOTE, ADASYN

# smote = SMOTE(sampling_strategy='minority')
adasyn = ADASYN(sampling_strategy='minority')
X_train, y_train = adasyn.fit_resample(X_train,y_train)

# y_sm.value_counts()

y_train.value_counts()

y_test.value_counts()

#Importing essential libraries
import matplotlib.pyplot as plt
from statistics import mean
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import plot_confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE

#Build SMOTE SRF model
SMOTE_SRF = RandomForestClassifier(n_estimators=150, random_state=0)
#Create Stratified K-fold cross validation
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
scoring = ('f1', 'recall', 'precision')
#Evaluate SMOTE SRF model
scores = cross_validate(SMOTE_SRF, X, y, scoring=scoring, cv=cv)
#Get average evaluation metrics
print('Mean f1: %.3f' % mean(scores['test_f1']))
print('Mean recall: %.3f' % mean(scores['test_recall']))
print('Mean precision: %.3f' % mean(scores['test_precision']))

#Randomly spilt dataset to test and train set
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, stratify=y)
#Train SMOTE SRF
SMOTE_SRF.fit(X_train, y_train)
#SMOTE SRF prediction result
y_pred = SMOTE_SRF.predict(X_test)
#Create confusion matrix
fig = plot_confusion_matrix(SMOTE_SRF, X_test, y_test, display_labels=['No IUU', 'IUU'], cmap='Greens')
plt.title('SMOTE + Standard Random Forest Confusion Matrix')
plt.show()

from sklearn.metrics import confusion_matrix , classification_report

print("Classification Report: \n", classification_report(y_test, y_pred))

from sklearn.ensemble import VotingClassifier
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier

# Define the models
xgb = XGBClassifier(random_state=42)
rf = RandomForestClassifier(random_state=42)

# Define the ensemble model
ensemble = VotingClassifier(estimators=[('xgb', xgb), ('rf', rf)], voting='soft')

# Fit the ensemble model on the training data
ensemble.fit(X_train, y_train)

# Evaluate the ensemble model on the test data
score = ensemble.score(X_test, y_test)

print(score)

from sklearn.metrics import classification_report

# Get the predictions for the test set
y_pred = ensemble.predict(X_test)

# Print the classification report
print(classification_report(y_test, y_pred))

from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.neural_network import MLPClassifier
import xgboost as xgb
from sklearn.metrics import classification_report

# Create the base models
rf = RandomForestClassifier(n_estimators=100)
xgb_clf = xgb.XGBClassifier(n_estimators=200)
ann = MLPClassifier(hidden_layer_sizes=(50,50))

# Create the meta-model
meta_model = MLPClassifier(hidden_layer_sizes=(50,50))

# Create the stacking classifier
stacking_clf = StackingClassifier(estimators=[('rf', rf), ('xgb', xgb_clf), ('ann', ann)], final_estimator=meta_model)

# Train the classifier
stacking_clf.fit(X_train, y_train)

# Make predictions
y_pred = stacking_clf.predict(X_test)

print(classification_report(y_test, y_pred))

from sklearn.metrics import confusion_matrix

# Print the confusion matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)