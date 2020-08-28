import pandas as pd
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize,RegexpTokenizer 
from collections import Counter
  
  
df = pd.read_csv("output1.csv")
l = df.size
stop_words = set(stopwords.words('english'))

tokenizer = RegexpTokenizer(r'\w+')
df["Frequent Words"] = ""

for i in range(l):
    tokens = tokenizer.tokenize(df["Linkedin_Profile_Text"].loc[i])
    filtered_sentence = [w for w in tokens if not w in stop_words] 
    split_sentence = ' '.join(filtered_sentence).split()
    counter = Counter(split_sentence)
    frequent_words = counter.most_common(10)
    df["Frequent Words"].loc[i] =  frequent_words

df.to_csv("output2.csv",index =False)
  


