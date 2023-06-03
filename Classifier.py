from sklearn.pipeline import Pipeline
import pickle
import matplotlib.pyplot as plt
from skmultilearn.problem_transform import ClassifierChain
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from tkinter import *
from tkinter.messagebox import *
import numpy as np
import pandas as pd
import seaborn as sns
sns.set()

train_data = pd.read_csv('Train.csv')
test_data = pd.read_csv('Test.csv')

abstract_list_train = []
abstract_list_test = []
stemmer = PorterStemmer()
stop_words = stopwords.words('english')

# Remove StopWords and Stemming
def remove_stopwords(data=[]):
    data_list = []
    for name in data:
        words = word_tokenize(name)
        stem_word = ""
        for a in words:
            if a.lower() not in stop_words:
                stem_word += stemmer.stem(a) + ' '
        data_list.append(stem_word.lower())
    return data_list

# Remove Special Characters
def remove_special_character(data=[]):
    abstract_list_wo_sc = []
    special_characters = '''!()-—[]{};:'"\, <>./?@#$%^&*_~0123456789+=’‘'''
    for file in data:
        word_wo_sc = ""
        if len(file.split()) == 1:
            abstract_list_wo_sc.append(file)
        else:
            for a in file:
                if a in special_characters:
                    word_wo_sc += ' '
                else:
                    word_wo_sc += a
            abstract_list_wo_sc.append(word_wo_sc)
    return abstract_list_wo_sc


# Remove stopwords from Train Data
data_train = np.array(train_data['ABSTRACT'])
abstract_list_train = remove_stopwords(data_train)

# Remove stopwords from Test Data
data_test = np.array(test_data['ABSTRACT'])
abstract_list_test = remove_stopwords(data_test)

# Removing speaial characters from Train Data and Test Data
abstract_list_wo_sc_train = remove_special_character(abstract_list_train)
abstract_list_wo_sc_test = remove_special_character(abstract_list_test)

categories = ['Computer Science', 'Physics', 'Mathematics', 'Statistics']

x_train = abstract_list_wo_sc_train
y_train = train_data[categories]
x_test = abstract_list_wo_sc_test
y_test = test_data[categories]

print("There are ", len(x_train), " input training samples")
print("There are ", len(x_test), " input testing samples")
print("There are ", y_train.shape, " output training samples")
print("There are ", y_test.shape, " output testing samples")

# defining parameters for pipeline
parameters = Pipeline([('tfidf', TfidfVectorizer(
    stop_words=stop_words)), ('clf', ClassifierChain(MultinomialNB())),])

# train data
parameters.fit(x_train, y_train)

# predict
predictions = parameters.predict(x_test)

print('Accuracy = ', accuracy_score(y_test, predictions))
print('F1 score is ', f1_score(y_test, predictions, average="micro"))
print(classification_report(y_test, predictions))

# Confusion Matrix and HeatMap Generation
mat = confusion_matrix(np.asarray(y_test.values.argmax(
    axis=1)), np.asarray(predictions.argmax(axis=1)))
sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False ,xticklabels=categories, yticklabels=categories)
plt.xlabel('true label')
plt.ylabel('predicted label')
plt.show()

with open('Multi_naivebayes.pkl', 'wb') as picklefile:
    pickle.dump(parameters.named_steps['clf'], picklefile)
