
# Data Analysis and Wrangling Libraries
import pandas as pd
import numpy as np
import random as rnd

# Visualization Libraries
import seaborn as sns
import matplotlib.pyplot as plt

# Machine Learning Libraries
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron, SGDClassifier
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv('2019_Crash_1_Database.csv')
train, test = train_test_split(df, test_size=0.2)

print (train.shape, test.shape)
for item in train.columns.values:
    print ("\t\t'%s'," % (item))

Drop = [
    'route',
    'milepoint',
    'num_tot_kil',
#    'num_tot_inj',
    'crash_date',
    'f_harm_ev_cd1',
    'm_harm_ev_cd1',
    'man_coll_cd',
    'crash_type',
    'surf_cond_cd',
    'crash_num',
    'parish_cd',
#    'crash_hour',
    'intersection',
    'invest_agency_cd',
    'travel_dirs',
    'prior_movements',
    'crash_year',
    'csect',
    'logmile',
    'lrs_id',
    'lrs_logmile',
    'adt',
#    'alcohol',
    'veh_type_cd1',
    'veh_type_cd2',
    'quadrant',
    'spotted_by',
    'intersection_id',
#    'severity_cd',
    'city_cd',
#    'roadway_departure',
#    'lane_departure',
    'road_rel_cd',
    'hwy_class',
    'contributing_factor',
    'location_type',
    'veh_severity_cd',
    'ORIG_LATITUDE',
    'ORIG_LONGITUDE',
    'DOTD_LATITUDE',
    'DOTD_LONGITUDE',
    'parish_cd.1',
    'hwy_type_cd',
    'pri_hwy_num',
    'bypass',
    'milepost',
    'pri_road_name',
    'pri_dist',
    'pri_measure',
    'pri_dir',
    'inter_road',
#    'dr_age_1',
#    'dr_age_2',
#    'dr_sex_1',
#    'dr_sex_2',
    'pri_contrib_fac_cd',
    'sec_contrib_fac_cd',
    'vision_obscure_1',
    'vision_obscure_2',
    'movement_reason_1',
    'movement_reason_2',
    'ped_actions_1',
    'ped_actions_2',
    'veh_lighting_1',
    'veh_lighting_2',
    'traff_cntl_cond_1',
    'traff_cntl_cond_2',
    'pri_road_dir',
    'lighting_cd',
#    'num_veh',
    'crash_time',
    'dr_cond_cd1',
    'dr_cond_cd2',
    'veh_cond_cd1',
    'veh_cond_cd2',
#    'Unnamed: 76',
]
train = train.drop(Drop, axis=1)
test = test.drop(Drop, axis=1)
print (train.head())

# Change categorical to ordinal
print (train['severity_cd'].value_counts())
#mapping = {'A':5, 'B':4, 'C':3, 'D':2, 'E':1}
mapping = {'A':1, 'B':0, 'C':0, 'D':0, 'E':0}
# Replace blanks with zero
for dataset in [train, test]:
    dataset['severity_cd'] = dataset['severity_cd'].map(mapping)
    dataset['severity_cd'] = dataset['severity_cd'].fillna(0)
    dataset['severity_cd'] = dataset['severity_cd'].astype(int)

# For Yes/No questions, replace blanks with the mode.
mapping = {'Yes':1, 'No':0}
for dataset in [train, test]:
    for col in ['roadway_departure','lane_departure']:
        dataset[col] = dataset[col].map(mapping)
        m = dataset[col].dropna().mode()
        print (m)
        dataset[col] = dataset[col].fillna(m)
        dataset[col] = dataset[col].astype(int)

for dataset in [train, test]:
    for col in ['crash_hour']:
        dataset[col] = pd.to_numeric(dataset[col], errors='coerce')
        m = dataset[col].dropna().mean()
        m = round(m,0)
        dataset[col] = dataset[col].fillna(m)
        dataset[col] = dataset[col].astype(int)

for dataset in [train, test]:
    for col in ['dr_age_1','dr_age_2']:
#        dataset[col] = pd.qcut(dataset[col], 10, duplicates='drop')
#       print (dataset[col].value_counts())
        dataset[col] = dataset[col].fillna(0)
        dataset[col] = pd.cut(dataset[col], bins=[-1,20,23,27,33,38,46,55,66,201], labels=[1,2,3,4,5,6,7,8,9])
        dataset[col] = dataset[col].astype(int)

for dataset in [train, test]:
    for col in ['dr_sex_1','dr_sex_2']:
        dataset[col] = np.where(dataset[col] == 'F', 0, 1)
        
for x in ['num_tot_inj', 'crash_hour', 'alcohol', 'roadway_departure', 'lane_departure']:
    print (x)
    print (train[[x, 'severity_cd']].groupby([x], as_index=False).mean().sort_values(by='severity_cd', ascending=False))
    print ('-*'*40)

print (train.info())
print ()
print (train['dr_age_1'].value_counts())

##############
#
# Model
#
##############

X_train = train.drop('severity_cd', axis=1)
Y_train = train['severity_cd']

X_test = test.drop('severity_cd', axis=1)
scaler = preprocessing.StandardScaler().fit(X_train)
X_scaled = scaler.transform(X_train)
print (X_train.shape, Y_train.shape, X_test.shape)

##### Logistic Regression
alg = LogisticRegression(max_iter=1000)
alg.fit(X_scaled, Y_train)
Y_pred = alg.predict(X_test)
acc_log = round(alg.score(X_scaled, Y_train)*100,2)
print ("Logistic Regression: ", acc_log)

coeff = pd.DataFrame(train.columns.delete(0))
coeff.columns = ['Feature']
coeff['Correlation'] = pd.Series(alg.coef_[0])
T = coeff.sort_values(by='Correlation', ascending=False)
print (T)
print ('-0'*40)

##### Support Vector Machines
#alg = SVC()
#alg.fit(X_scaled, Y_train)
#Y_pred = alg.predict(X_test)
acc_svc = 0
#acc_svc = round(alg.score(X_scaled, Y_train)*100,2)
#print ("Support Vector Machines: ", acc_svc)

##### k-Nearest Neighbors
alg = KNeighborsClassifier(n_neighbors=3)
alg.fit(X_scaled, Y_train)
Y_pred = alg.predict(X_test)
acc_knn = round(alg.score(X_scaled, Y_train)*100,2)
print ("k-Nearest Neighbors: ", acc_knn)

##### Gaussian Naive Bayes
alg = GaussianNB()
alg.fit(X_scaled, Y_train)
Y_pred = alg.predict(X_test)
acc_gaussian = round(alg.score(X_scaled, Y_train)*100,2)
print ("Gaussian: ", acc_gaussian)

####### Perceptron
alg = Perceptron()
alg.fit(X_scaled, Y_train)
Y_pred = alg.predict(X_test)
acc_perceptron = round(alg.score(X_scaled, Y_train)*100,2)
print ("Perceptron: ", acc_perceptron)

######### Linear Support Vector Classifier
alg = LinearSVC()
alg.fit(X_scaled, Y_train)
Y_pred = alg.predict(X_test)
acc_linearSVC = round(alg.score(X_scaled, Y_train)*100,2)
print ("Linear SVC: ", acc_linearSVC)

########## Stochastic Gradient Descent Classifier
alg = SGDClassifier()
alg.fit(X_scaled, Y_train)
Y_pred = alg.predict(X_test)
acc_sgdc = round(alg.score(X_scaled, Y_train)*100,2)
print ("SGD Classifier: ", acc_sgdc)

######### Decision Tree Classifier
alg = DecisionTreeClassifier()
alg.fit(X_scaled, Y_train)
Y_pred = alg.predict(X_test)
acc_decision_tree = round(alg.score(X_scaled, Y_train)*100,2)
print ("Decision Tree Classifier: ", acc_decision_tree)

######### Random Forest Classifier
alg = RandomForestClassifier()
alg.fit(X_scaled, Y_train)
Y_pred = alg.predict(X_test)
acc_random_forest = round(alg.score(X_scaled, Y_train)*100,2)
print ("Random Forest Classifier: ", acc_random_forest)

models = pd.DataFrame({
    'Model':[
        'Support Vector Machines',
        'k-Nearest Neighbors',
        'Logistic Regression',
        'Random Forest',
        'Naive Bayes',
        'Perceptron',
        'Stochastic Gradient Descent',
        'Linear SVC',
        'Decision Tree',
        ],
    'Score':[
        acc_svc, acc_knn, acc_log, acc_random_forest, acc_gaussian,
        acc_perceptron, acc_sgdc, acc_linearSVC, acc_decision_tree
        ]
    })
T = models.sort_values(by='Score', ascending=False)
print (T)
T = T.to_latex()
write  = open("Table.tex", "w")
write.write("%s\n" % (T))
write.close()
