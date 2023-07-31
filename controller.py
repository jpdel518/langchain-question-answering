import pytube
import whisper

import schemas
import utils
from database import crud
from datetime import datetime
from sqlalchemy.orm import Session

from langchain.embeddings.openai import OpenAIEmbeddings # 文章と文章の関連を出す
from langchain.text_splitter import CharacterTextSplitter # 文字ベースでテキストを分解
from langchain.vectorstores.faiss import FAISS
from langchain.chains import VectorDBQAWithSourcesChain
from langchain import OpenAI

import openai
import faiss # 類似の画像やテキストを検索するためのインデックスを作成


def transcribe_from_youtube(data: schemas.CreatingTranscription, db: Session):
    db_datas = crud.fetch_transcription(db, data.url)

    if len(db_datas) > 0:
        utils.logger.info("already transcribed")
        return

    video = pytube.YouTube(data.url)
    utils.logger.info(video.title)
    utils.logger.info(video.streams.get_highest_resolution().filesize / 1024 / 1024)

    # 文字起こしするためにオーディオだけ取得する
    audio = video.streams.get_audio_only()

    # オーディオをテンポラリー領域に保存
    audio.download(output_path="gpt4_na.mp3")

    # whisperを使って文字起こし
    model = whisper.load_model("small")
    transcription = model.transcribe(
        f"gpt4_na.mp3/{video.title}.mp4")

    # どんなキーがトップの階層に来ているか確認
    utils.logger.info(transcription.keys())

    # texts = []
    # start_times = []

    for segment in transcription["segments"]:
        text = segment["text"]
        start = segment["start"]

        start_datetime = datetime.utcfromtimestamp(start)
        formatted_start_time = start_datetime.strftime("%H:%M:%S")

        d = schemas.Transcription(
            url=data.url,
            text=text,
            start=formatted_start_time
        )

        crud.create_transcription(db, d)

        # texts.append(text)
        # start_times.append(formatted_start_time)


def get_distinct_transcriptions(db: Session):
    data = crud.distinct_transcription(db)
    urls = []
    for d in data:
        urls.append(d[0])
    utils.logger.info(urls)
    return urls


def generate_question_answer(data: schemas.AskingTranscription, db: Session):
    text_splitter = CharacterTextSplitter(chunk_size=1500, separator="\n")

    db_datas = crud.fetch_transcription(db, data.url)

    docs = []
    metadatas = []
    # whisperで取得した字幕をloopさせる
    for db_data in db_datas:
        splits = text_splitter.split_text(db_data.text)
        docs.extend(splits)
        metadatas.extend([{"source": db_data.start}] * len(splits))
    embeddings = OpenAIEmbeddings()

    # テキストと属性データを格納
    store = FAISS.from_texts(docs, embeddings, metadatas=metadatas)

    # \n区切りで字幕にindexをつけている
    faiss.write_index(store.index, "docs.index")

    chain = VectorDBQAWithSourcesChain.from_llm(llm=OpenAI(temperature=0), vectorstore=store)

    # YouTubeの内容からQuestionAnswering
    answer = chain({"question": data.question})

    return answer
