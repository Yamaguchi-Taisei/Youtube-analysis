import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
import streamlit as st
import json

# 秘密鍵の読み込み
with open('secret.json') as f:
    secret = json.load(f)

api_service_name = "youtube"
api_version = "v3"
api_key = secret['KEY']

# YouTube API クライアントの構築
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=api_key)


def video_search(youtube, q='東海オンエア', max_result=50):
    request = youtube.search().list(
        part="id, snippet",
        order="viewCount",
        type='video',
        maxResults=max_result,
        q=q
    )
    response = request.execute()

    items_id = []
    items = response['items']
    for item in items:
        item_id = {
            'video_id': item['id']['videoId'],
            'channel_id': item['snippet']['channelId']
        }
        items_id.append(item_id)

    df_video = pd.DataFrame(items_id)
    return df_video


def get_results(df_video, threshold=5000):
    channel_ids = df_video['channel_id'].unique().tolist()

    subscriber_request = youtube.channels().list(
        id=','.join(channel_ids),
        part="statistics",
        fields='items(id, statistics(subscriberCount))'
    )
    subscriber_list = subscriber_request.execute()

    subscribers = []
    for item in subscriber_list['items']:
        subscriber = {
            'channel_id': item['id'],
            'subscriber_count': int(item['statistics']['subscriberCount'])
        }
        subscribers.append(subscriber)

    df_subscribers = pd.DataFrame(subscribers)

    # df_video と df_subscribers をマージ
    df = pd.merge(left=df_video, right=df_subscribers,
                  left_on='channel_id', right_on='channel_id')

    # サブスクライバー数が閾値未満のデータを抽出
    df_extracted = df[df['subscriber_count'] < threshold]

    # ビデオ情報を取得
    video_ids = df_extracted['video_id'].tolist()
    video_request = youtube.videos().list(
        id=','.join(video_ids),
        part="snippet, statistics",
        fields='items(id, snippet(title), statistics(viewCount))'
    )
    videos_list = video_request.execute()

    videos_info = []
    items = videos_list['items']
    for item in items:
        video_info = {
            'video_id': item['id'],
            'title': item['snippet']['title'],
            'view_count': item['statistics']['viewCount']
        }
        videos_info.append(video_info)

    df_videos_info = pd.DataFrame(videos_info)

    # ビデオ情報とチャンネル情報をマージ
    results = pd.merge(left=df_extracted, right=df_videos_info, on='video_id')

    # 必要な列だけを選択
    results = results[['video_id', 'title',
                       'view_count', 'subscriber_count', 'channel_id']]

    return results


# Streamlit
st.title('YouTube分析アプリ')
st.sidebar.write('## クエリの閾値の設定')
st.sidebar.write('### クエリの入力')
query = st.sidebar.text_input('検索クエリを入力してください', 'ツムツム')

st.sidebar.write('### 閾値の設定')
threshold = st.sidebar.slider('登録者の閾値', 100, 10000, 5000)

st.write('### 選択中のパラメータ')
st.markdown(f"""
- 検索クエリ: {query}
- 登録者数の閾値: {threshold}
""")


df_video = video_search(youtube, q=query, max_result=50)
results = get_results(df_video, threshold=threshold)

st.write('### 検索結果', results)

# 動画再生
video_id = st.text_input('動画IDを入力してください')
url = f'https://www.youtube.com/watch?v={video_id}'

if st.button('ビデオ表示'):
    if len(video_id) > 0:
        try:
            st.video(url)
        except Exception as e:
            st.error(f'動画が存在しないようです: {e}')
