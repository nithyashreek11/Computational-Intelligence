# ex3.py
# KNN Classification

from sklearn.neighbors import KNeighborsClassifier

X = [[1], [2], [3], [6], [7], [8]]
y = ['A', 'A', 'A', 'B', 'B', 'B']

model = KNeighborsClassifier(n_neighbors=3)
model.fit(X, y)

prediction = model.predict([[5]])

print("Predicted Class:", prediction[0])
