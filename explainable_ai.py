from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers_interpret import SequenceClassificationExplainer
import streamlit as st
from streamlit import components


def explain():
    st.subheader("Can we explain the predictions of a Transformer?")
    st.write("This tool tries to explain why a certain prediction was made by our model for a certain guideline")
    html = None
    with st.form(key='my_form'):
        text = st.text_area(
            'Enter the section you want to get predictions for', height=300)
        explain = st.form_submit_button('Explain!')
        if explain:
            with st.spinner('Loading...'):
                model_name = "arjunth2001/priv_ftc"
                model = AutoModelForSequenceClassification.from_pretrained(
                    model_name)
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                cls_explainer = SequenceClassificationExplainer(
                    model,
                    tokenizer)
                words = cls_explainer(text)
                html = cls_explainer.visualize()
    if html != None:
        raw_html = html._repr_html_()
        components.v1.html(raw_html, scrolling=True)
