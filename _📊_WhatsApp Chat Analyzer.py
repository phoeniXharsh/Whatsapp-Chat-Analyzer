import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
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


## Intro page

st.subheader("Welcome to Whatsapp Chat Analyzer!")
expander1 = st.expander("What this app can do?")
expander1.write("""
        1. It can show basic statistics of your WhatsApp chats.\n
        3. It shows visuals graphs of your personalised chats and provide meaningful insights in the conversaton.\n 
 """)
expander2 = st.expander("How to use it?")
expander2.write("""
        1. Read the prerequisites page present in the sidebar of this app.\n 
           (If you're using a smartphone, expand the sidebar by clicking on the top-left arrow button.)\n
        2. Follow the steps present in prerequistes and upload the file in the drag & drop region.
 """)

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis with respect  to", user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_msg, words, num_media_msg, links = helper.fetch_stats(selected_user, df)

        st.title("Top Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_msg)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Messages")
            st.title(num_media_msg)
        with col4:
            st.header("Links Shared")
            st.title(links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        matplotlib.rcParams['font.size'] = 12
        sns.set_style("darkgrid")
        fig, ax = plt.subplots(figsize= (18,9))
        ax.plot(timeline['time'], timeline['messages'], color = 'green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        matplotlib.rcParams['font.size'] = 12
        fig, ax = plt.subplots(figsize= (18,9))
        ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color = 'black')
        plt.xticks(rotation = 'horizontal')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Weekday")
            busy_day = helper.week_activity_map(selected_user, df)

            matplotlib.rcParams['font.size'] = 14
            fig = plt.figure(figsize= (10,8))
            sns.barplot(busy_day.index, busy_day.values, palette="Blues_r")
            plt.xticks(rotation= 'vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_day = helper.month_activity_map(selected_user, df)
            
            matplotlib.rcParams['font.size'] = 16
            fig = plt.figure(figsize= (11,9))
            sns.barplot(busy_day.index, busy_day.values, palette="BuPu_r")
            plt.xticks(rotation= 'vertical')
            st.pyplot(fig)

        # most active hour
        st.title("Most Active Hour")

        active_df = helper.most_active_hours(selected_user, df)
        matplotlib.rcParams['font.size'] = 8
        fig = plt.figure(figsize= (9,7))
        sns.barplot(active_df.hours,active_df.number_of_message,data = active_df,dodge=False)
        st.pyplot(fig)

        # heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        matplotlib.rcParams['font.size'] = 8
        fig,ax = plt.subplots(figsize = (9, 5))
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # Most Active Day
        col1, col2 = st.columns(2)
        with col1:
            st.title("Most Active Day")
            most_active_day = helper.most_active_day(selected_user, df)

            matplotlib.rcParams['font.size'] = 15
            fig = plt.figure(figsize= (14,10))
            sns.barplot(most_active_day['Date'], most_active_day['Message count'], palette="hls")
            st.pyplot(fig)
        
        # Most Busy Users
        with col2:
                if selected_user == 'Overall':
                    st.title("Most Busy Users")
                    df_users, df_percent= helper.fetch_busy_users(df)
                    matplotlib.rcParams['font.size'] = 12
                    fig = plt.figure(figsize= (10,6))
                    ax = sns.barplot(y =  df_users.values, x = df_users.index, palette="inferno")
                    def set_percentage(ax, index, value):
                        i=0
                        for p in ax.patches:
                            percentage = value[i]
                            x = p.get_x() + p.get_width() / 2 - 0.05
                            y = p.get_y() + p.get_height()
                            ax.annotate(percentage, (x, y), size = 12, ha= 'center')
                            i += 1
                    set_percentage(ax, df_percent['name'], df_percent['percent'])
                    plt.xticks(rotation = 'vertical')
                    st.pyplot(fig)

        # Word Cloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax= plt.subplots()
        ax.imshow(df_wc)
        plt.axis("off")
        plt.figure(facecolor= 'k')
        matplotlib.rcParams["axes.grid"] = False
        st.pyplot(fig)

        # most common words
        st.title("Most Common Words")

        most_common_df = helper.most_common_words(selected_user, df)

        fig = plt.figure(figsize= (10,8))
        sns.barplot(y =  most_common_df['words'], x = most_common_df['frequency'], palette="ocean")

        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # deleted messages
        st.title("Deleted Messages Analysis")
        deleted_df = helper.message_deleted(selected_user, df)

        fig = plt.figure(figsize= (16,8))
        sns.barplot(x = deleted_df['user'].head(10),y = deleted_df['Messages Deleted'].head(10) ,palette= "viridis")

        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # emoji analysis
        st.title("Emoji Analysis")
        st.markdown("Coming Soon...")
#        emoji_df = helper.emojis_helper(selected_user, df)
#
#        col1, col2 = st.columns(2)
#        with col1:
#            st.dataframe(emoji_df) 
#        with col2:
#            fig, ax = plt.subplots()
#            ax.pie(emoji_df['frequency'].head(), labels = emoji_df['emoji'].head(), autopct="%0.2f")
#            st.pyplot(fig)


        