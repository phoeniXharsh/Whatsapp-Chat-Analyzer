import streamlit as st
from PIL import Image

## Page configuration and customization
img = Image.open("whatsapp_image2.png")
st.set_page_config(page_title='Chat Analyzer', page_icon = img, layout = 'wide')

## Hide Footer and Hamburger Menu 
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
                visibility: visible;
                content: "Made with ❤️ by Harsh";
                display: block;
                padding: 5px;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Prerequisties")

st.subheader("1. The time format of your smartphone must be in 12h format. You can verify/change it in your phone's 'Date & Time' settings.")
st.subheader("2. The language of your smartphone must be English (USA). You can find it in the 'Languages & Input' tab in your phone's 'System' settings.")
st.markdown("Note: If you have changed any of the above settings in your smartphone, reboot your phone once before downloading the data from WhatsApp.")
st.subheader("3. You need to have the exported chat data which you want to analyze. To export and download the chat data, just follow the steps below:")

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

