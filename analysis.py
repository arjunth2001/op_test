import streamlit as st


def analysis():
    st.subheader(
        "Analysis")
    st.write("""
    # How does Privacy Policies of Forbes 500 Companies differ from the top Indian Startups?
    To put our classification model to use we collected the privacy policies of [Forbes Fortune 500 Companies](https://fortune.com/fortune500/) and of
    [Top 300 Indian Startups](https://www.failory.com/startups/india#toc-10-gomechanic). We clean the text, segment the HTML and pass each segment of the document to classify it for
    one of the FTC Guidelines from the [OPP115 Dataset](https://usableprivacy.org/static/files/swilson_acl_2016.pdf). We then plot the distribution of percentages
    for each of these guidelines as shown below""")
    c1, c2 = st.columns((2, 1))
    with c1:
        st.image("images/ftc_implementations.png", use_column_width=True)
    st.write("""
    ##### **We observe that most of the guidelines follow a similar distribution except for International and Specific Audiences which is found higher in Forbes 500 Policies which makes sense. But why are the Indian Startups not worrying about international Audiences?**
    
    ### Now we plot the word count distributions for Forbes and Indian Startup Documents.
    """)
    c1, c2 = st.columns(2)
    with c1:
        st.image("images/words.png", use_column_width=True)
    with c2:
        st.image("images/words_count.png", use_column_width=True)
    st.write("""
    ##### **We observe that most of the time they follow a similar distribution but generally the Forbes 500 Documents are lengthier.**
    ### Dale–Chall readability index
    Next we plot [Dale–Chall readability index](https://en.wikipedia.org/wiki/Dale%E2%80%93Chall_readability_formula) distributions for both categories.
    Higher the index, tougher is the text to read and more age and education required.
    """)
    c1, c2 = st.columns(2)
    with c1:
        st.image("images/readabilty.png", use_column_width=True)
    with c2:
        st.image("images/readabilty_count.png", use_column_width=True)
    st.write("""
    ##### **We observe that Indian Policies are generally easier to read, owing to the simple english being used. But with this there might be reduction in information covered which needs to be studied. It could be that the Indian Policies are not conveying the same level of information as much as the foreign policies making them easier to comprehend but with a tradeoff.**
    """)
