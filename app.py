import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
st.sidebar.title("WhatsApp Chat Analyser")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df= preprocessor.preprocess(data)
    #fetch unique users
    user_list = df["users"].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user= st.sidebar.selectbox("Show analysis wrr", user_list)
# via this analysis will start
    if st.sidebar.button("Show Analysis"):
    #stats Area
        num_messages,words,num_media_messages,num_links=helper.fetch_stats(selected_user,df)
        st.title("top statistics")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
   #timeline
        st.title("monthly analysis")
        timeline=helper.monthly_timeline(selected_user, df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        plt.show()
        st.pyplot(fig)
    #daily timeline

        st.title("daily analysis")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        plt.show()
        st.pyplot(fig)

   #activity map
    st.title('Activity map')
    col1,col2=st.columns(2)
    with col1:
        st.header("most busy day")
        busy_day=helper.week_activity_map(selected_user,df)
        fig,ax=plt.subplots()
        ax.bar(busy_day.index,busy_day.values)
        plt.xticks(rotation='vertical')

        st.pyplot(fig)

    with col2:
        st.header("most busy months")
        busy_month = helper.month_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values,color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)







        # finding the busiest users in group(group level)
        if selected_user== 'Overall':
            st.title('Most Busy Users')
            x,new_df=helper.most_busy_users(df)
            fig,ax=plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

    #wordcloud
    st.title("word cloud")
    df_wc=helper.create_wordcloud(selected_user,df)
    fig,ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)
    #most common words

    most_common_df=helper.most_common_words(selected_user,df)
    fig,ax=plt.subplots()
    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation='vertical')
    st.title('most common words')
    st.pyplot(fig)
    # st.dataframe(most_common_df)

    # emoji_df=helper.emoji_helper(selected_user,df)
    # st.dataframe(emoji_df)