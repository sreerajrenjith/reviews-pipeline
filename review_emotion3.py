#https://www.geeksforgeeks.org/emotion-classification-using-nrc-lexicon-in-python/
from nrclex import NRCLex
#from final_amazon import prod_name
import pandas as pd
#df = pd.read_csv(f'{prod_name}_cleaned.csv')
df = pd.read_csv('data_cleaned.csv')
for index, row in df.iterrows():
    text=row['comment']
    emotion=NRCLex(text)
    print(emotion.top_emotions)