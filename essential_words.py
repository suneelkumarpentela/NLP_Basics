import pandas as pd
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize,RegexpTokenizer 
from collections import Counter
  
  
df = pd.read_csv("output2.csv")
stop_words = set(stopwords.words('english'))

V= []

#Removing punctuations
for i in range(50):
    tokenizer = RegexpTokenizer(r'\w+')

    tokens = tokenizer.tokenize(df["Linkedin_Profile_Text"].loc[i])
    filtered_sentence = [w for w in tokens if not w in stop_words] 
    split_sentence = ' '.join(filtered_sentence)
    V.append(split_sentence)
  
from sklearn.feature_extraction.text import TfidfVectorizer

#calling the TfidfVectorizer
vectorizer= TfidfVectorizer()

#fitting the model and passing our sentences right away:
vectors = vectorizer.fit_transform(V)
names = vectorizer.get_feature_names()
data = vectors.todense().tolist()

df1 = pd.DataFrame(data,columns = names)


df["Essential Words"] = ""
j = 0
for i in df1.iterrows():
    df["Essential Words"].loc[j] = list((i[1].sort_values(ascending=False)[:15]).keys())
    j+=1

#creating a new csv file with all columns required
df.to_csv("output3.csv",index =False) 







