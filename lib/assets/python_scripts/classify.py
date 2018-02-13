import pandas as pd
import sys
from io import StringIO
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import scale
from sklearn import metrics
from sklearn.utils import resample
import json

def classify(spotify_id):
    filename = "/Users/matiasbeeck/Documents/metis/metisgh/project3/autoclassify/public/" + spotify_id + "tracks.csv"
    # track_list = pd.read_csv(StringIO(trackscsv.replace(u'\u201c', '"').replace('\\', '')), keep_default_na=True)
    track_list = pd.read_csv(filename, keep_default_na=True)
    train_set = (track_list[track_list.unclassified == False]).drop_duplicates(subset=['track_id'], keep="first", inplace=False).reset_index(drop=True)[['playlist_name', 'duration', 'explicit', 'acousticness',\
                                                             'danceability', 'energy', 'instrumentalness', 'key',\
                                                             'liveness', 'loudness', 'mode', 'speechiness', 'tempo',\
                                                             'valence', 'pop', 'rap', 'dance_pop', 'pop_rap',\
                                                             'postteen_pop', 'hip_hop', 'rock', 'trap_music',\
                                                             'modern_rock', 'latin', 'edm', 'tropical_house',\
                                                             'southern_hip_hop', 'rnb', 'classic_rock']]
    unclass_set = track_list[track_list.unclassified == True].sort_values(by="id", ascending=True)[['duration', 'explicit', 'acousticness',\
                                                             'danceability', 'energy', 'instrumentalness', 'key',\
                                                             'liveness', 'loudness', 'mode', 'speechiness', 'tempo',\
                                                             'valence', 'pop', 'rap', 'dance_pop', 'pop_rap',\
                                                             'postteen_pop', 'hip_hop', 'rock', 'trap_music',\
                                                             'modern_rock', 'latin', 'edm', 'tropical_house',\
                                                             'southern_hip_hop', 'rnb', 'classic_rock']]

    train_data, test_data = train_test_split(train_set, test_size=0.4, random_state=42)

    # Original train set
    train_x = train_data.iloc[:, 1:].reset_index(drop=True)
    train_y = train_data.iloc[:, 0].reset_index(drop=True)
    scaled_train_x = scale(train_x)

    # Holdout (test-set)
    test_x = test_data.iloc[:, 1:].reset_index(drop=True)
    test_scaled_x = scale(test_x)
    test_y = test_data.iloc[:, 0].reset_index(drop=True)

    # Unclassified dataset
    unclass_set_x = unclass_set
    unclass_scaled_x = scale(unclass_set_x)

    # Finding biggest class
    classes = pd.DataFrame(train_data.playlist_name.value_counts()).reset_index()
    classes.columns = ['playlist', 'track_count']
    classes.sort_values(by="track_count", ascending=False, inplace=True)

    # Searching for optimal value of K for KNN on train data
    k_range = list(range(1, classes.loc[0,'track_count']//2))
    train_scores = []
    for k in k_range:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(scaled_train_x,train_y)
        train_scores.append(accuracy_score(test_y, knn.predict(test_scaled_x)))
    optimal_k_val = (k_range[train_scores.index(max(train_scores))])

    classifiers = [KNeighborsClassifier(n_neighbors=optimal_k_val), LogisticRegression(), GaussianNB(), SVC(), DecisionTreeClassifier(), RandomForestClassifier()]
    accuracies = []
    knn = KNeighborsClassifier(n_neighbors=optimal_k_val).fit(scaled_train_x, train_y)
    logreg = LogisticRegression().fit(scaled_train_x, train_y)
    gnb = GaussianNB().fit(train_x, train_y)
    svc = SVC(probability=True).fit(scaled_train_x, train_y)
    dtc = DecisionTreeClassifier().fit(scaled_train_x, train_y)
    rf = RandomForestClassifier().fit(scaled_train_x, train_y)

    classifiers = [knn, logreg, gnb, svc, dtc]

    accuracies.append(("KNN(" + str(optimal_k_val) + " neighbors)", 0 , "{:.3f}".format(accuracy_score(test_y, knn.predict(test_scaled_x)))))
    accuracies.append(("Logistic Regression", 1, "{:.3f}".format(accuracy_score(test_y, logreg.predict(test_scaled_x)))))
    accuracies.append(("Gaussian NB", 2, "{:.3f}".format(accuracy_score(test_y, gnb.predict(test_x)))))
    accuracies.append(("SVC", 3, "{:.3f}".format(accuracy_score(test_y, svc.predict(test_scaled_x)))))
    accuracies.append(("Decision Tree", 4, "{:.3f}".format(accuracy_score(test_y, dtc.predict(test_scaled_x)))))
    accuracies.append(("Random Forest", 5, "{:.3f}".format(accuracy_score(test_y, rf.predict(test_scaled_x)))))
    reg_scores = sorted(accuracies, key=lambda x: x[2], reverse=True)

    # Applying winning fit to predict
    fit = classifiers[reg_scores[0][1]]
    if reg_scores[0][1] == 2:
        predictions = list(fit.predict(unclass_set_x))
        predprobs = fit.predict_proba(unclass_set_x).max(axis=1)
    else:
        predictions = list(fit.predict(unclass_scaled_x))
        predprobs = fit.predict_proba(unclass_scaled_x).max(axis=1)

    json_data = {}
    json_data["predprobs"] = predprobs.tolist()
    json_data["predictions"] = predictions
    json_data["model"] = reg_scores[0][0]
    json_data["model_acc"] = reg_scores[0][2]
    json_data = json.dumps(json_data)

    return json_data

sys.stdout.write(classify(sys.argv[1]))
