import streamlit as st

## Hide Footer and Hamburger Menu
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Prerequisties")

st.subheader("1. The time format of your smartphone should be in 12h format")
st.subheader("2. You need to have the exported chat data which you want to analyze. To export and download the chat data, follow the following steps")

st.header(" ")

st.markdown("Step 1: Go to WhatsApp in your smartphone and select the desired chat")
st.markdown("Step 2: Press the context menu in the top right corner")

st.markdown("Step 3: In the context menu, select the 'More' item")
st.image('step3.jfif', width=170)

st.markdown("Step 4: Click on 'Export chat' ")
st.image('step4.jfif', width=170)

st.markdown("Step 5: Choose the 'Without Media' option")
st.image('step5.jfif', width= 300)

st.markdown("Step 6: Save the file and upload it here")

