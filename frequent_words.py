import pandas as pd
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize,RegexpTokenizer 
from collections import Counter
  
  
df = pd.read_csv("output1.csv")
l = df.size
#print(df["Linkedin_Profile_Text"].loc[0])
stop_words = set(stopwords.words('english'))

tokenizer = RegexpTokenizer(r'\w+')
df["Frequent Words"] = ""

for i in range(l):
    tokens = tokenizer.tokenize(df["Linkedin_Profile_Text"].loc[i])
    #word_tokens = word_tokenize(df["Linkedin_Profile_Text"].loc[0])
    #print(word_tokens)
    filtered_sentence = [w for w in tokens if not w in stop_words] 
    #df["Linkedin_Profile_Text"].loc[i]
    split_sentence = ' '.join(filtered_sentence).split()
    #print(split_sentence)
    counter = Counter(split_sentence)
    frequent_words = counter.most_common(10)
    df["Frequent Words"].loc[i] =  frequent_words

df.to_csv("output2.csv",index =False)
  

  
# print(word_tokens) 
# print(filtered_sentence) 




