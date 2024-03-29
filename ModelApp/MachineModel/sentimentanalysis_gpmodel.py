# -*- coding: utf-8 -*-
"""SentimentAnalysis_GPModel.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N9CfbzUwAg6jaWMqD49dllvjrJHzI4s6
"""

#python version: 3.11.0
#pip3 install django
#pip3 install djangorestframework
#python -m pip install Pillow
#pip3 install emoji --upgrade 
#pip3 install PyArabic
#pip3 install nltk
#pip3 install -U scikit-learn
#pip3 install pandas
#pip3 install django-cors-headers


import re
import nltk
import emoji
import numpy as np
import pandas as pd
import pyarabic.araby as araby
from nltk.corpus import stopwords
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score
from sklearn.svm import SVC

nltk.download('stopwords')
nltk.download('punkt')

#reading the dataset
df = pd.read_csv('ModelApp/MachineModel/Sentiment_Dataset.csv')
df.head()

#Preprocessing Functions
def remove_emoji(text):
    return emoji.demojize(text)

def cleaning(text):
 Arabic_numbers = ['٤','١','٢','٣','٥','٦','٧','٨','٩','٠']
 special_character = ['؟','،','?',',','!','.',':','"','""','‘‘','‘','؛','↓',"'", '‰',
                      '`','€',';','ç','ı','À','@','٬','~᷂','٫','◕','.','ـ',''
                      '=','#','$','%','^','&','*','()',')','(','\\','/','~','¦'
                      '((', '_', '"','"', '…','-','×','ツ','+','÷','٪','ლ', '{', '}', '[',']', '<', '>','|']
 #remove emojis
 text= remove_emoji(text)
 #replace special characters with whitespaces
 for word in range(0, len(special_character)):
     text = text.replace(special_character[word], ' ')
 #replace arabic numbers with whitespaces
 for word in range(0, len(Arabic_numbers)):
     text = text.replace(Arabic_numbers[word], ' ')
 #remove english words letters and numbers
 text = re.sub(r'[0-9a-zA-Z]+',' ', text)
 return text

def stop_word_removal(text):
  stop_words = set(stopwords.words("arabic"))
  words = araby.tokenize(text)
  text = " ".join([w for w in words if not w in stop_words])
  return text

def normalization(text):
  text = re.sub("[إأٱآا]", "ا", text)
  text = re.sub("ى", "ي", text)
  text = re.sub("ة", "ه", text)
  #remove extra whitespace
  text = re.sub('\s+', ' ', text)
  #remove tashkeel
  text = araby.strip_tashkeel(text)
  return text

def pre_processing(text):
 #Cleaning
 text = cleaning(text)
 #stop words removal
 text = stop_word_removal(text)
 #Normalization
 text = normalization(text)
 #stop words removal
 text = stop_word_removal(text)
 return text

def process_text(text):
    stemmer = nltk.ISRIStemmer()
    word_list = nltk.word_tokenize(text)
    #stemming
    word_list = [stemmer.suf32(w) for w in  word_list]
    return ' '.join(word_list)

#pre_processing the review column
df['Review']  = df['Review'].apply(lambda x:pre_processing(x))

#Stemming the review column
df['Review']  = df['Review'].apply(lambda x:process_text(x))


#remove tabs and new lines from the text 
df['Review'] = df.Review.str.replace("\xa0"," ") 
df['Review'] = df.Review.str.replace("\n"," ")
df['Review'] = df['Review'].replace("\t"," ", regex=True)

# check for nulls 
df['Review'].isnull().sum()
#remove blanks by replacing them with Nan
df['Review'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# drop nans
df.dropna(subset=['Review'], inplace=True)

# drop duplicates 
df=df.drop_duplicates(subset=['Review'])



# Split the data into training and test sets
x_train, x_test, y_train, y_test = train_test_split(df['Review'], df['Classification'], test_size=0.2, random_state=42)


# The Chosen Model (SVM Model)

# Create a pipeline with TF-IDF vectorizer and MultiClass SVM classifier
pipe = make_pipeline(TfidfVectorizer(), SVC(kernel='linear', C=1, decision_function_shape='ovr')) #Use linear kernel function, The C parameter controls the trade-off between maximizing the margin and minimizing the classification error.
                                                                                                  #The decision_function_shape parameter is set to 'ovr' (one-vs-rest) to allow the SVM to handle multi-class classification.

# Train the model on the training set
pipe.fit(x_train, y_train)

# Make predictions on the test set
prediction = pipe.predict(x_test)

# Evaluate the model using F1 score
print("F1 Score -> ", f1_score(y_test, prediction, average='micro')*100)

def prediction(text):
  text = pre_processing(text)
  text = process_text(text)
  list = [text]
  prediction = pipe.predict(list)
  return prediction

#print(prediction("  مش وحش  "))