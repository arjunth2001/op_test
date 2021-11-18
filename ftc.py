import streamlit as st
from helpers import *
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer


def ftc():
    st.subheader("FTC Guideline Extractor")
    st.write("Given a privacy policy and the FTC Guidelines you are interested in, the tool outputs relevant paragraphs")
    with st.form(key='my_form'):
        text = st.text_area('Enter the Privacy Policy', height=300)
        option = st.multiselect(
            "For which all guidelines would you like to extract paragraphs for?", options=['First Party Collection/Use',
                                                                                           'Third Party Sharing/Collection',
                                                                                           'International and Specific Audiences',
                                                                                           'Data Security',
                                                                                           'User Choice/Control',
                                                                                           'User Access, Edit and Deletion',
                                                                                           'Data Retention',
                                                                                           'Policy Change',
                                                                                           'Do Not Track'])
        paras = text.split("\n")
        extract = st.form_submit_button('Extract!')
        if extract:
            if option == []:
                st.warning("Please select at least one guideline")
            else:
                with st.spinner("Loading..."):
                    name = "arjunth2001/priv_ftc"
                    model = AutoModelForSequenceClassification.from_pretrained(
                        name)
                    tokenizer = AutoTokenizer.from_pretrained(name)
                    pipe = pipeline('text-classification',
                                    model=model, tokenizer=tokenizer)
                    outs = pipe(paras)
                    relevant_paragraphs = []
                    for i, para in enumerate(paras):
                        out = outs[i]["label"]
                        if out in option:
                            relevant_paragraphs.append(para)
                st.success("Done!")
                if len(relevant_paragraphs) == 0:
                    st.warning("No relevant paragraphs found")
                else:
                    st.write(
                        "The following paragraphs are relevant to the selected guidelines:")
                    for para in relevant_paragraphs:
                        st.write(para)
