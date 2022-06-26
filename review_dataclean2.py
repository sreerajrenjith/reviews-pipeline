import pandas as pd
import numpy as np
import wordcloud
from nltk.corpus import stopwords
import nltk
import string
#from final_amazon import prod_name
#df = pd.read_csv(f'{prod_name}.csv')
df = pd.read_csv(f'reviews.csv')
df.head(5)
null_values=df.isna().sum()
null_values=pd.DataFrame(null_values,columns=['null'])
sum_tot=len(df)
null_values['percent']=null_values['null']/sum_tot*100
round(null_values,3).sort_values('percent',ascending=False)
df= df.dropna()
df.shape
# nltk.download('omw-1.4')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
stop = stopwords.words('english')
df['stopwords'] = df['comment'].apply(lambda x: len([x for x in x.split() if x in stop]))
df[['comment','stopwords']].head()
def count_punct(text):
    count = sum([1 for char in text if char in string.punctuation])
    return count

df['punctuation'] = df['comment'].apply(lambda x: count_punct(x))
df[['comment','punctuation']].head()
df['hastags'] = df['comment'].apply(lambda x: len([x for x in x.split() if x.startswith('#')]))
df[['comment','hastags']].head()
df.hastags.loc[df.hastags != 0].count()
df['upper'] = df['comment'].apply(lambda x: len([x for x in x.split() if x.isupper()]))
df[['comment','upper']].head()

#Data cleaning
df['comment'] = df['comment'].apply(lambda x: " ".join(x.lower() for x in x.split()))
df['comment'].head()
df['comment'] = df['comment'].apply(lambda x: " ".join(x.lower() for x in x.split()))
df['comment'] = df['comment'].str.replace('[^\w\s]','',regex=True)
df['comment'].head()
stop = stopwords.words('english')
df['comment'] = df['comment'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
df['comment'].sample(10)
freq = pd.Series(' '.join(df['comment']).split()).value_counts()[:20]
freq
# Adding common words from our document to stop_words
# add_words = ["br", "get", "also"]
# stop_words = set(stopwords.words("english"))
# stop_added = stop_words.union(add_words)
# df['comment'] = df['comment'].apply(lambda x: " ".join(x for x in x.split() if x not in stop_added))
# df['comment'].sample(10)
def remove_url(text): 
    url = re.compile(r'https?://\S+|www\.\S+')
    return url.sub(r'', text)
# remove all urls from df
import re
import string
df['comment'] = df['comment'].apply(lambda x: remove_url(x))
def remove_html(text):
    html=re.compile(r'<.*?>')
    return html.sub(r'',text)
# remove all html tags from df
df['comment'] = df['comment'].apply(lambda x: remove_html(x))
def remove_emoji(text): 
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)
df['comment'] = df['comment'].apply(lambda x: remove_emoji(x))

from textblob import TextBlob
df['comment'][:5].apply(lambda x: str(TextBlob(x).correct()))

from nltk.stem import WordNetLemmatizer 

# Init the Wordnet Lemmatizer
lemmatizer = WordNetLemmatizer()
df['comment'] = df['comment'].apply(lambda x: lemmatizer.lemmatize(x))

def avg_word(sentence):
    words = sentence.split()
    return (sum(len(word) for word in words)/(len(words)+0.000001))
df['avg_word'] = df['comment'].apply(lambda x: avg_word(x)).round(1)
df[['comment','avg_word']].head()
print(df.sample(5))
#df.to_csv(f'{prod_name}_cleaned.csv')
df.to_csv('data_cleaned.csv')
print("data cleaning done!")