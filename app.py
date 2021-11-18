import streamlit as st

PAGES = ["Home", "Jurassic-1 Chat Bot", "Longitudinal Analysis and GDPR", "Comparing Forbes 500 vs Indian Startups", "FTC Paragraph Extractor", "Summarizer",
         "Question and Answering", "Explainable AI"]
PAGE_CONFIG = {'page_title': 'Online Privacy Project', 'layout': "wide"}
st.set_page_config(**PAGE_CONFIG)


def main():
    st.sidebar.title("Menu")
    selection = st.sidebar.radio("Go to", PAGES)
    if selection == "Home":
        from home import home
        home()
    elif selection == "Jurassic-1 Chat Bot":
        from jurassic import jurassic
        jurassic()
    elif selection == "Longitudinal Analysis and GDPR":
        from l_analysis import analysis
        analysis()
    elif selection == "Comparing Forbes 500 vs Indian Startups":
        from analysis import analysis
        analysis()
    elif selection == "FTC Paragraph Extractor":
        from ftc import ftc
        ftc()
    elif selection == "Summarizer":
        from summarizer import summary
        summary()
    elif selection == "Question and Answering":
        from qna import qna
        qna()
    elif selection == "Explainable AI":
        from explainable_ai import explain
        explain()
    st.sidebar.title("About")
    st.sidebar.info(
        """
        Made with ♥ by Team IIIT-H Analytica 
        as a part of Online Privacy Course M21.
"""
    )


if __name__ == "__main__":
    main()
