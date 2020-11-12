import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Import the data from the excel file
dataset = pd.read_excel("C:/Users/Nathan/OneDrive - University of Cincinnati/4th Year CompE/AIPrinciplesAndApplications/CS4033_AI/Homework3/HW3Data.xlsx", "Sheet1")

# Create the X and y datasets
X = dataset.drop('Class', axis=1)
y = dataset['Class']

# Split the data for training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

# Create decision tree and fit training data to tree
classifier = DecisionTreeClassifier(min_impurity_split=0.1)
classifier = classifier.fit(X_train, y_train)

# Export tree to dot file with graphviz
tree.export_graphviz(classifier, out_file = 'tree.dot')

# Use test data to predict y and compare to actual data
y_pred = classifier.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Plot 70x70 grid
for x in range(71):
    for y in range(71):
        x_y = [[x, y]]
        out = classifier.predict(x_y)
        if out == 0:
            plt.plot(x, y, 'o', color='red')
        elif out == 1:
            plt.plot(x, y, 'o', color='black')

plt.show()

# Plot data
x_plot = dataset['X'].tolist()
y_plot = dataset['Y'].tolist()
classes = dataset['Class'].tolist()

class_plot = []
for c in classes:
    if c == 0:
        class_plot.append('red')
    elif c == 1:
        class_plot.append('black')

for i in range(len(x_plot)):
    plt.plot(x_plot[i], y_plot[i], 'o', color=class_plot[i])

plt.show()





