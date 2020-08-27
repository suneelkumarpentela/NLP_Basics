import pandas as pd
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize,RegexpTokenizer 
from collections import Counter
  
  
df = pd.read_csv("output2.csv")
#print(df["Linkedin_Profile_Text"].loc[0])
stop_words = set(stopwords.words('english'))

V= []
for i in range(50):
    tokenizer = RegexpTokenizer(r'\w+')

    tokens = tokenizer.tokenize(df["Linkedin_Profile_Text"].loc[i])
    #word_tokens = word_tokenize(df["Linkedin_Profile_Text"].loc[0])
    #print(word_tokens)
    filtered_sentence = [w for w in tokens if not w in stop_words] 
    #df["Linkedin_Profile_Text"].loc[i]
    split_sentence = ' '.join(filtered_sentence)
    V.append(split_sentence)

#print(split_sentence)
  
from sklearn.feature_extraction.text import TfidfVectorizer
#for the sentence, make sure all words are lowercase or you will run #into error. for simplicity, I just made the same sentence all #lowercase
firstV= "Data Science is the sexiest job of the 21st century"
secondV= "machine learning is the key for data science"
#calling the TfidfVectorizer
vectorizer= TfidfVectorizer()
#fitting the model and passing our sentences right away:
vectors = vectorizer.fit_transform(V)# [ V[0],V[49] ] )
names = vectorizer.get_feature_names()
data = vectors.todense().tolist()

df1 = pd.DataFrame(data,columns = names)


#print(len(vectorizer.get_feature_names()))

df["Essential Words"] = ""
j = 0
for i in df1.iterrows():
    df["Essential Words"].loc[j] = list((i[1].sort_values(ascending=False)[:15]).keys())
    j+=1

#print(i[1].sort_values(ascending=False)[:15])
#print(df.head)
df.to_csv("output3.csv",index =False)


  
# print(word_tokens) 
# print(filtered_sentence) 




