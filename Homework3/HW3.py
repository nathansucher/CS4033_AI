import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_text
from sklearn.metrics import classification_report, confusion_matrix

dataset = pd.read_excel("C:/Users/Nathan/OneDrive - University of Cincinnati/4th Year CompE/AIPrinciplesAndApplications/CS4033_AI/Homework3/HW3Data.xlsx", "Sheet1")

x = dataset.drop('Class', axis=1)
y = dataset['Class']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.70)

classifier = DecisionTreeClassifier()
classifier = classifier.fit(x_train, y_train)

graph = export_text(classifier)
# print(graph)
print(classifier.tree_.max_depth)

y_pred = classifier.predict(x_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
