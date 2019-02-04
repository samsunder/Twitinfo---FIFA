
import numpy as np
import pandas as pd
data = pd.read_csv('testoutlier2.csv', low_memory=False)

relevant_features = [
    "Likes",
    "RTs",
    "Followers"
]

data = data[relevant_features ]


data["RTs"] = np.log((data["RTs"] + 0.1).astype(float))
data["Likes"] = np.log((data["Likes"] + 0.1).astype(float))

data.loc[data['Followers'] > 50, "traffic_behaviour"] = 1
data.loc[data['Followers'] <= 50, "traffic_behaviour"] = -1

target = data['traffic_behaviour']

outliers = target[target == -1]
print('outliers count: \n',outliers)
print('outliers.shape: \n', outliers.shape)
print('outlier fraction: \n', outliers.shape[0]/target.shape[0])


from sklearn.model_selection import train_test_split
train_data, test_data, train_target, test_target = train_test_split(data, target, train_size = 0.8)
train_data.shape



from sklearn import svm

nu = 0.3
print("nu", nu)

model = svm.OneClassSVM(nu=nu, kernel='rbf', gamma=0.00005)
model.fit(train_data)



from sklearn import metrics
values_preds = model.predict(train_data)
values_targs = train_target


print("Training DataSET accuracy: ", 100 *  metrics.accuracy_score(values_targs, values_preds))
print("Training DataSET Precision: ",100 * metrics.precision_score(values_targs, values_preds))
print("Training DataSET Recall: ", 100 * metrics.recall_score(values_targs, values_preds))
print("Training DataSET f1: ", 100 * metrics.f1_score(values_targs, values_preds))

values_preds = model.predict(test_data)
values_targs = test_target

print("Test DataSet Accuracy: ", 100 * metrics.accuracy_score(values_targs, values_preds))
print("Test DataSet Precision: ", 100 * metrics.precision_score(values_targs, values_preds))
print("Test DataSet Recall: ", 100 * metrics.recall_score(values_targs, values_preds))
print("Test DataSet F1: ", 100 * metrics.f1_score(values_targs, values_preds))