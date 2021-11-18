from transformers import AutoTokenizer
import torch
from datasets import Dataset
import pandas as pd
from transformers import AutoModelForQuestionAnswering, TrainingArguments, Trainer
from transformers import default_data_collator
import torch
import numpy as np
import streamlit as st
import requests
import os
API_KEY = os.environ['API_KEY_ST']


def jurassic():
    st.subheader(
        "Jurassic-1: Give a Policy and a Question.. Get an answer !")
    with st.form(key='my_form'):
        context = st.text_area('Enter the Privacy Policy', height=300)
        question = st.text_area('Enter the Question')
        get_answer = st.form_submit_button('Get the answer!')
        if get_answer:
            with st.spinner("Finding an Answer..."):
                context = context.replace("\n", "")
                question = question.replace("\n", "")
                prompt = f"Answer the Question based upon the Context.\nContext: {context}\nQuestion: {question}\nAnswer:\n"
                res = requests.post(
                    "https://api.ai21.com/studio/v1/j1-large/complete",
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    json={
                        "prompt": prompt,
                        "numResults": 1,
                        "maxTokens": 64,
                        "stopSequences": ["."],
                        "topKReturn": 0,
                        "temperature": 0.7
                    }
                )
                answer = res.json()["completions"][0]["data"]["text"]
            st.success("Answer!")
            st.write(answer)
