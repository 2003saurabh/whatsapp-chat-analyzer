from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

extractor=URLExtract()
def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df = df[df['users'] == selected_user]
    # fetch the total number of messages
    num_messages = df.shape[0]
    # fetch the number of media messages
    words=[]
    for message in df['message']:
        words.extend(message.split())
    # fetch number of media messages
    num_media_messages=df[df['message']=="<Media omitted>\n"].shape[0]

    # fetch number of links shared

    links = []
    for i in df['message']:
        links.extend(extractor.find_urls(i))
    return num_messages, len(words),num_media_messages,len(links)

def most_busy_users(df):
    x=df['users'].value_counts().head()
    df=round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'users':'name','count':'percentage'})
    return x,df

# create word cloud
def create_wordcloud(selected_user, df):
    f = open('./stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # Ensure all messages are strings
    df['message'] = df['message'].astype(str)

    # Handle empty strings or NaN values (if any)
    df = df[df['message'].str.strip() != '']

    temp = df[df['users'] != 'group_notifications']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y=[]
        for wrd in message.lower().split():
            if wrd not in stop_words:
                y.append(wrd)
        return " ".join(y)
    # Generate the word cloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc

def most_common_words(selected_user,df):
    f = open('./stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notifications']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for msg in temp['message']:
        for wrd in msg.lower().split():
            if wrd not in stop_words:
                words.append(wrd)

    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

# Emoji analysis
def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    emojis = []
    for msg in df['message']:
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

# Monthly Timeline
def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

# daily Timeline
def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('date').count()['message'].reset_index()
    return daily_timeline

# week activity map
def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()

# month activity map
def monthly_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

# activity heatmap
def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    user_heatmap=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)

    return user_heatmap

