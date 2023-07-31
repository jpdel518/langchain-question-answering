import json

import streamlit as st
import requests

st.title('YouTube Question Answering System')
page = st.sidebar.selectbox('Choose your page', ['transcription', 'question'])

if page == 'transcription':
    st.markdown('### モデルを作成したいYouTube URLを入力してください')

    # フォームを作成
    with st.form(key='youtube'):
        youtube_url: str = st.text_input('YouTube URL')
        data = {
            'url': youtube_url,
        }
        submit = st.form_submit_button(label='モデル作成')

    if submit:
        res = requests.post('http://localhost:8000/transcript', data=json.dumps(data))
        if res.status_code == 200:
            st.success('モデルを作成しました')
        else:
            st.write(res.status_code)
            st.json(res.json())

elif page == 'question':
    urls = requests.get('http://localhost:8000/transcript').json()
    st.markdown('### モデル作成済みのYouTube URLを選択してください')
    url = st.selectbox('YouTube URL', urls)

    st.markdown('### 質問を入力してください')
    with st.form(key='question'):
        question: str = st.text_input('質問')
        submit = st.form_submit_button(label='回答を作成')

    if submit:
        data = {
            'url': url,
            'question': question,
        }
        res = requests.post('http://localhost:8000/question', data=json.dumps(data))
        if res.status_code == 200:
            st.success('回答結果が返ってきました')
            body = res.json()['answer']
            st.markdown('#### 回答')
            st.write(body['answer'])
            st.markdown('#### 回答の情報ソース')
            st.write(body['sources'])
        else:
            st.write(res.status_code)
            st.json(res.json())
