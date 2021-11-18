import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from helpers import sum_clean_text
import torch
from tqdm import tqdm
sum_model = "arjunth2001/priv_sum"


def summary():
    st.subheader("Privacy Policy Summarizer")
    with st.form(key='my_form'):
        text = st.text_area('Enter the Privacy Policy', height=300)
        left_column, right_column = st.columns(2)

        min_length = left_column.number_input(
            'Minimum words', value=30, min_value=30, max_value=500)
        max_length = right_column.number_input(
            'Maximum words', value=512, min_value=300, max_value=512)

        summarize = st.form_submit_button('Summarize this Policy!')
        if summarize:
            with st.spinner("Summarizing..."):
                texts = text.split('\n')
                output = " "
                texts = [t for t in texts if len(t.split()) > 100]
                # st.success(len(texts))
                if len(texts) == 0:
                    texts = [text]
                for text in tqdm(texts):
                    with torch.no_grad():
                        tokenizer = AutoTokenizer.from_pretrained(sum_model)
                        model = AutoModelForSeq2SeqLM.from_pretrained(
                            sum_model)
                        preprocess_text = sum_clean_text(
                            text.strip().replace("\n", ""))
                        t5_prepared_Text = "summarize: "+preprocess_text
                        tokenized_text = tokenizer.encode(
                            t5_prepared_Text, return_tensors="pt")
                        summary_ids = model.generate(tokenized_text,
                                                     num_beams=4,
                                                     no_repeat_ngram_size=2,
                                                     min_length=min_length,
                                                     max_length=max_length,
                                                     early_stopping=True)
                        output += tokenizer.decode(
                            summary_ids[0], skip_special_tokens=True)
            st.success("Summarized Policy")
            st.write(output)
