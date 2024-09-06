import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    def clean_date(date_str):
        match = re.match(r'(\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}\s(?:AM|PM))', date_str)
        if match:
            return match.group(1)
        else:
            return None

    df['cleaned_date'] = df['message_date'].apply(clean_date)
    df['message_date'] = pd.to_datetime(df['cleaned_date'], format='%m/%d/%y, %I:%M %p', errors='coerce')
    df.drop(columns=['cleaned_date'], inplace=True)
    users = []
    message_texts = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            message_texts.append(entry[2])
        else:
            users.append('group_notifications')
            message_texts.append(entry[0])
    df['users'] = users
    df['message'] = message_texts
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['message_date'].dt.year
    df['date'] = df['message_date'].dt.date
    df['day_name']=df['message_date'].dt.day_name()
    df['month_num'] = df['message_date'].dt.month
    df['day'] = df['message_date'].dt.day
    df['month'] = df['message_date'].dt.month_name()
    df['hours'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute

    # hour to period function
    period = []
    for hour in df[['day_name', 'hours']]['hours']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str("00") + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df




