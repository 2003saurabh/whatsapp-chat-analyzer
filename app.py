import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn  as sns
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)

    # print the dataframe
    # st.dataframe(df)

    # fetch unique user
    user_list=df['users'].unique().tolist()
    user_list.remove('group_notifications')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user=st.sidebar.selectbox("show analysis wrt",user_list)
    if st.sidebar.button("Show Analysis"):

        # stats area
        st.title("Top Statistics")
        num_messages,words,num_media_messages,num_links=helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messgaes")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            x=helper.most_busy_users(df)
            st.title(num_links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['date'], daily_timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title("Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.subheader("weekly")
            busy_day=helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.subheader("Monthly")
            busy_month=helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # activity heatmap
        st.title("Weekly activity Heatmap")
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)



        # finding the most busiest users in the group(group level)
        if selected_user=='Overall':
            st.title("Most Busy Users")
            x,new_df=helper.most_busy_users(df)
            fig,ax=plt.subplots()

            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Word Cloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common used words
        st.title("Most Common used words")
        col1, col2 = st.columns(2)
        most_common_df=helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # emoji
        emoji_df=helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)


