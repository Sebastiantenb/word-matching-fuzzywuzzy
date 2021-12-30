import streamlit as st

import pandas as pd

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

#title
st.title('Word Similarity Matching')  #Title of the webapp

#text
st.markdown('Need to match 2 lists of words or sentences? Need to match them despite spelling mistakes or minor differences in spelling? Then upload or copy one set of words as "Base Key Words" and the other set as "Match Key Words"')

#input strings
string_base_words = st.sidebar.text_area('Base Key Words', '''
     seperate words by comma, apple, banana, peach, (...)
     ''')
string_match_word = st.sidebar.text_area('Match Key Words', '''
     seperate words by comma, apple, banana, peach, (...)
     ''')
#st.write('Sentiment:', run_sentiment_analysis(txt))
#string_base_words = "Apple, Pear, Banana, Orange, Peach"
#string_match_word = "apple, Bear, Bannana, Orange, Peaches, Banaan"

#string to list
list_base_word = string_base_words.split(",")
list_match_word = string_match_word.split(",")

#list to dataframe
df_base_word = pd.DataFrame(list_base_word, columns = ["base_word"])
df_match_word = pd.DataFrame(list_match_word, columns = ["match_word"])

#CSV upload
uploaded_file = st.sidebar.file_uploader("Upload CSV of Base Words")
if uploaded_file is not None:
     # To read file as bytes:
     bytes_data = uploaded_file.getvalue()
     st.write(bytes_data)
# Can be used wherever a "file-like" object is accepted:
     df_base_word = pd.read_csv(uploaded_file)
     df_base_word.columns = ['base_word']
     st.write(df_base_word)

uploaded_file = st.sidebar.file_uploader("Upload CSV of Match Words")
if uploaded_file is not None:
     # To read file as bytes:
     bytes_data = uploaded_file.getvalue()
     st.write(bytes_data)
# Can be used wherever a "file-like" object is accepted:
     df_base_word = pd.read_csv(uploaded_file)
     df_match_word.columns = ['match_word']
     st.write(df_match_word)

# Create a function that takes two lists of strings for matching
def match_name(name, list_names, min_score=0):
    # -1 score incase we don't get any matches
    max_score = -1
    # Returning empty name for no match as well
    max_name = ""
    # Iterating over all names in the second list
    for name2 in list_names:
        #Finding fuzzy match score
        score = fuzz.ratio(str.lower(name), str.lower(name2))
        # Checking if we are above our threshold and have a better score
        if (score > min_score) & (score > max_score):
            max_name = name2
            max_score = score
    return (max_name, max_score)

#slider for matching value
match_percentage = st.slider('Word Similarity Ratio', 0, 100, 85)

# List for dicts for easy DataFrame creation
dict_list = []
# iterating over df with more strains
for name in df_base_word.base_word:
    # Use our method to find best match, we can set a threshold here
    match = match_name(name, df_match_word.match_word, match_percentage)
    
    # New dict for storing data
    dict_ = {}
    dict_.update({"strain" : name})
    dict_.update({"name" : match[0]})
    dict_list.append(dict_)
    
df_matched_table = pd.DataFrame(dict_list)

df_matched_table

@st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')

csv = convert_df(df_matched_table)

st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name='matched_words.csv',
     mime='text/csv',
 )