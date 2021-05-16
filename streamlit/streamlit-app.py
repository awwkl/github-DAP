import streamlit as st
import utils
import pickle
import numpy as np

# setup code
utils.setup()
top_tokens = utils.get_top_tokens()
load_clf = pickle.load(open('files/rnd_clf.pkl', 'rb'))

# page layout code
st.header('Programming Language Classifier :rocket:')

# take in user's input source code
input_code = st.text_area("Code Input for Prediction", "Enter your code here.", height=350)
input_tokens = utils.tokenize(input_code)
input_vector = utils.vectorize(input_tokens)

# predict language
predict_vector = np.array(input_vector).reshape(1, -1)
y_pred = load_clf.predict(predict_vector)
lang_dict = {
    '.html': 'HTML',
    '.java': 'Java',
    '.py': 'Python',
    '.c': 'C',
    '.cpp' :'C++',
    '.rb': 'Ruby',
    '.php': 'PHP'
}
lang_pred = lang_dict[y_pred[0]]

if len(input_code) < 100:
    st.write("Please provide at least 100 characters for the model to predict accurately")
else:
    st.write(f"Predicted Language: **{lang_pred}**")

st.write("""
***
Data Associate Project (DAP) of SMU Business Intelligence & Analytics (SMUBIA)
* Contributors: Aw Khai Loong, Felice Png, Lee Yu Hao, Yap Bing Yu
* Mentor: Yar Khine Phyo
* Check out our github at [GitHub Link](https://github.com/sky-aw/github-DAP) 
""")