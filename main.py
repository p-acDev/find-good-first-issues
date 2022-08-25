import streamlit as st
from find_good_first_issues import get_html_data, find_issues
from dotenv import load_dotenv
import os
load_dotenv('./config_env')

st.write("# Find *good first issues*")
st.info("This web app allows you to find good first issues if any to contribute to a repo based on the topic filter")


topic = st.text_input("Provide filter topic")

if topic and st.button("Find"):
    
    url = f"https://github.com/topics/{topic}"

    html_raw_data = get_html_data(url)

    good_first_issues = find_issues(html_raw_data)

    for repo, issues in good_first_issues.items():
        if issues != []:
            with st.expander(repo):
                for issue in issues:
                    st.write(issue)