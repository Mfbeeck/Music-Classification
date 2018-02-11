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
    classes = pd.DataFrame(train_data.playlist_name.value_counts()).reset_index()
    classes.columns = ['playlist', 'track_count']
    classes.sort_values(by="track_count", ascending=False, inplace=True)
    samples_num = classes.iloc[0,:].track_count
    new_train = train_data[train_data.playlist_name == classes.iloc[0,:].playlist]
    for playlist in list(classes.playlist)[1:]:
        df = train_data[train_data.playlist_name == playlist]
        rsamples = resample(df, n_samples = samples_num)
        new_train = pd.concat([new_train, rsamples])
    new_train.playlist_name.value_counts()
    # Up Sampled Train Data
    new_X = new_train.iloc[:, 1:].reset_index(drop=True)
    new_scaled_x = scale(new_X)
    new_y = new_train.iloc[:, 0].reset_index(drop=True)
    # Test Data
    test_X = test_data.iloc[:, 1:].reset_index(drop=True)
    test_scaled_x = scale(test_X)
    test_y = test_data.iloc[:, 0].reset_index(drop=True)

    # Unclassified dataset
    unclass_set_x = unclass_set
    unclass_scaledx = scale(unclass_set)
    # Searching for optimal value of K for KNN
    k_range = list(range(1, 25))
    k_scores = []
    for k in k_range:
        knn = KNeighborsClassifier(n_neighbors=k)
        scores = cross_val_score(knn, new_scaled_x, new_y, cv=10, scoring='accuracy')
        k_scores.append(scores.mean())
    optimal_k_val = (k_range[k_scores.index(max(k_scores))])

    classifiers = [KNeighborsClassifier(n_neighbors=optimal_k_val), LogisticRegression(), GaussianNB(), SVC(), DecisionTreeClassifier(), RandomForestClassifier()]
    accuracies = []
    knn = KNeighborsClassifier(n_neighbors=optimal_k_val).fit(new_scaled_x, new_y)
    logreg = LogisticRegression().fit(new_scaled_x, new_y)
    gnb = GaussianNB().fit(new_X, new_y)
    svc = SVC(probability=True).fit(new_scaled_x, new_y)
    # dtc = DecisionTreeClassifier().fit(new_scaled_x, new_y)
    # rf = RandomForestClassifier().fit(new_scaled_x, new_y)

    classifiers = [knn, logreg, gnb, svc]

    accuracies.append(("KNN(" + str(optimal_k_val) + " neighbors)", 0 , "{:.3f}".format(accuracy_score(test_y, knn.predict(test_scaled_x)))))
    accuracies.append(("Logistic Regression", 1, "{:.3f}".format(accuracy_score(test_y, logreg.predict(test_scaled_x)))))
    accuracies.append(("Gaussian NB", 2, "{:.3f}".format(accuracy_score(test_y, gnb.predict(test_X)))))
    accuracies.append(("SVC", 3, "{:.3f}".format(accuracy_score(test_y, svc.predict(test_scaled_x)))))
    # accuracies.append(("Decision Tree", 4, "{:.3f}".format(accuracy_score(test_y, dtc.predict(test_scaled_x)))))
    # accuracies.append(("Random Forest", 5, "{:.3f}".format(accuracy_score(test_y, rf.predict(test_scaled_x)))))
    reg_scores = sorted(accuracies, key=lambda x: x[2], reverse=True)

    # Applying winning fit to predict
    fit = classifiers[reg_scores[0][1]]
    predictions = list(fit.predict(unclass_scaledx))
    predprobs = fit.predict_proba(unclass_scaledx).max(axis=1)

    json_data = {}
    json_data["predprobs"] = predprobs.tolist()
    json_data["predictions"] = predictions
    json_data["model"] = reg_scores[0][0]
    json_data["model_acc"] = reg_scores[0][2]
    json_data = json.dumps(json_data)

    return json_data

sys.stdout.write(classify(sys.argv[1]))
