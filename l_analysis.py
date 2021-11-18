import streamlit as st


def analysis():
    st.subheader(
        "Analysis")
    st.write("""
    # How have Privacy Policies changed over the years?
    To put our classification model to use we ran it over the [Princeton Longitudinal Dataset](https://privacypolicies.cs.princeton.edu/) of Privacy Policies over time. We clean the text, segment the HTML and pass each segment of the document to classify it for
    one of the FTC Guidelines from the [OPP115 Dataset](https://usableprivacy.org/static/files/swilson_acl_2016.pdf). We then plot the distribution of percentages
    for each of these guidelines as shown below over the time.""")

    st.image("images/long.png", use_column_width=True)
    st.write("""
    ##### We observe that there is a spike in 2018 where there is an increase in the mention of text related to the guidelines. What is so special about 2018?
    ### We believe that it is because of the GDPR which was enacted in 2018.
    The General Data Protection Regulation (EU) 2016/679 [GDPR](https://en.wikipedia.org/wiki/General_Data_Protection_Regulation) is a regulation in EU law on data protection and privacy in the European Union (EU) and the European Economic Area (EEA). It also addresses the transfer of personal data outside the EU and EEA areas.
    The GDPR was adopted on 14 April 2016 and became enforceable beginning 25 May 2018. As the GDPR is a regulation, not a directive, it is directly binding and applicable, but does provide flexibility for certain aspects of the regulation to be adjusted by individual member states.
    The regulation became a model for many national laws outside the EU, including United Kingdom, Turkey, Mauritius, Chile, Japan, Brazil, South Korea, Argentina and Kenya. The California Consumer Privacy Act [CCPA](https://en.wikipedia.org/wiki/California_Consumer_Privacy_Act), adopted on 28 June 2018, has many similarities with the GDPR.""")
    st.write("""
    # Geographical variation based on GDPR? 
    ### We noticed that some companies keep different versions of their websites for different regions. Are the privacy policies different in these cases?
    ### Are same rules applicable to every person on the planet Earth? Or different ones for a person from a GDPR following region and a person from a NON GDPR area?
    To find this we collected the policies of 500 websites (one version from GDPR area and one from NON GDPR Region. Then we passed them through a sentence transformer to generate sentence embeddings. We then get
    the cosine similarity of such pairs and plot the bar garphs for the cosine similarity.)
    """)
    c1, c2 = st.columns((3, 1))
    with c1:
        st.image("images/simbar.png", use_column_width=True)
    st.write("""
    ##### **We observe that even though a large number of Documents are exact match, there are some documents which are showing differences. This suggests that these websites might be following different policies at different locations based upon the strictness of the laws**
    ## Conclusion
    ### **There needs to be a unified strict law like the GDPR throughout the world providing Privacy Law enactment which is beneficiary as shown by our analysis.**
    """)
