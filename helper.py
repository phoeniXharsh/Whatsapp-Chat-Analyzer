from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import re

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user']== selected_user]
    
    #1: fetch number of messages
    num_msg = df.shape[0]

    #2: number of words
    words = []
    for message in df['messages']:
        words.extend(message.split(" ")) 

    # fetch no.of media messages
    num_media_msg = df[df['messages'] == '<Media omitted>\n'].shape[0]

    # fetch urls
    extractor = URLExtract()
    links= []
    for msg in df['messages']:
        links.extend(extractor.find_urls(msg))
    return num_msg, len(words), num_media_msg, len(links)

def fetch_busy_users(df):
    clean_df = df.drop(df.index[df['user'] == 'group_notification'], inplace = False)
    df_users = clean_df['user'].value_counts().head(10)
    df_percent = round(clean_df['user'].value_counts()/df.shape[0]*100, 2).reset_index().rename(columns= {'index':'name', 'user':'percent'})
    return df_users, df_percent

def remove_stop_words(message):

    f = open('stopwords_hinglish.txt', 'r')
    stop_words = f.read()

    y= []
    for word in message.lower().split():
        if word not in stop_words:
            y.append(word)
    return " ".join(y)

def create_wordcloud(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user']== selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    temp['messages'] = temp['messages'].apply(remove_stop_words)

    wc = WordCloud(width= 600,height= 400, min_font_size= 8, background_color = 'white')

    df_wc = wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):

    f = open('stopwords_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['user']== selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    temp['messages'] = temp['messages'].apply(remove_stop_words)

    # remove numbers from messages
    res = []
    for i in temp['messages']:
        digit = re.findall('[0-9]+', i)
        res.append(digit)

    num = [ele for ele in res if ele != []]

    words = []
    for msg in temp['messages']:
        for word in msg.lower().split():
            if word not in stop_words and num:
                words.append(word)

    word_count = pd.DataFrame(Counter(words).most_common(20))
    word_count.columns = ['words', 'frequency']
    return word_count

def emojis_helper(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user']== selected_user]

    emojis = []
    for msg in df['messages']:
        emojis.extend([c for c in msg if c in emoji.UNICODE_EMOJI_ENGLISH])

    emoji_df = pd.DataFrame(Counter(emojis).most_common()).head(10)
    emoji_df.columns = ['emoji', 'frequency']
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user']== selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()
    
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
        
    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user']== selected_user]
    
    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user']== selected_user]

    return df['day_name'].value_counts()
    

def month_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user']== selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap

def message_deleted(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    delete_df = df[df['messages'].str.contains("You deleted this message") | df['messages'].str.contains("This message was deleted")]
    total_messages_df = df.groupby('user', as_index=False).agg({"messages": 'count'})
    total_messages_df.rename(columns={"messages":"Total Messages"}, inplace=True)

    total_messages_df = total_messages_df.drop(total_messages_df.index[total_messages_df['user'] == 'group_notification'], inplace = False)
    
    analysis_df = delete_df.groupby("user", as_index=False)["messages"].count()
    analysis_df.rename(columns={"messages":  "Messages Deleted"}, inplace=True)
    analysis_df = analysis_df.merge(total_messages_df, on="user", how='outer')
    analysis_df.fillna(0, inplace=True)
    analysis_df["Messages Deleted"] = analysis_df["Messages Deleted"].astype(int)
    analysis_df["% Deleted"] = round(analysis_df["Messages Deleted"]/analysis_df["Total Messages"], 2)

    analysis_df.sort_values(by = ['Messages Deleted'], ascending = False, inplace = True)

    return analysis_df

def most_active_hours(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['number_of_message'] = [1] * df.shape[0]
    df['hours'] = df['date'].apply(lambda x: x.hour)
    time_df = df.groupby('hours').count().reset_index().sort_values(by = 'hours')
    
    return time_df

def most_active_day(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['Message count'] = [1] * df.shape[0]  
    df = df.groupby('date').sum().reset_index()
    df['Date'] = df['date'].dt.date
    top10days = df.sort_values(by="Message count", ascending=False).head(10)  
    top10days.reset_index(inplace=True)
    top10days.drop(columns="index", inplace=True)

    return top10days


