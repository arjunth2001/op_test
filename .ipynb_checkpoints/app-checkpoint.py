import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re
import torch
sum_model = "t5-small"
PAGES = ["OPP 115", "Summarize", "QnA"]


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def removePattern(text, pattern):

    r = re.findall(pattern, text)

    for i in r:

        text = re.sub(i, '', text)

    return text


def remove_urls(vTEXT):
    vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b',
                   '', vTEXT, flags=re.MULTILINE)
    return(vTEXT)


def sum_clean_text(text):
    if type(text) != str:
        return " "
    text = remove_urls(text)
    text = cleanhtml(text)
    text = removePattern(text, "@[\w]*")  # remove handles
    text = removePattern(text, "&[\w]*")  # remove &amp
    return text


def main():
    st.sidebar.title("Menu")
    selection = st.sidebar.radio("Go to", PAGES)
    if selection == "OPP 115":
        st.subheader("OPP 115 Classifaction and Visualisation")
        st.write("Under Construction")
    elif selection == "Summarize":
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
                        output = tokenizer.decode(
                            summary_ids[0], skip_special_tokens=True)
                st.success("Summarized Policy")
                st.write(output)
    elif selection == "QnA":
        st.subheader("QnA")
        st.write("Under Construction")
    st.sidebar.title("About")
    st.sidebar.info(
        """
        Made with ♥ by Team IIIT-H Analytica 
        as a part of Online Privacy Course M21.
"""
    )


if __name__ == "__main__":
    main()
