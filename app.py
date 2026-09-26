import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import streamlit as st

from coursepilot.config import get_settings
from coursepilot.llm.client import LLMClient
from coursepilot.mastery.bkt import BKTParameters
from coursepilot.mastery.repository import MasteryRepository
from coursepilot.rag.embeddings import LocalEmbeddingFunction
from coursepilot.rag.service import RAGService
from coursepilot.rag.vector_store import VectorStore
from coursepilot.quiz.generator import QuizGenerator
from coursepilot.quiz.grader import QuizGrader
from coursepilot.ui.dashboard import render_dashboard
from coursepilot.ui.qa import render_qa
from coursepilot.ui.quiz import render_quiz
from coursepilot.ui.upload import render_upload

st.set_page_config(page_title="CoursePilot", page_icon="📚", layout="wide")


@st.cache_resource
def services():
    settings = get_settings()
    store = VectorStore(str(settings.chroma_dir), LocalEmbeddingFunction(settings.embedding_model))
    llm = LLMClient(settings)
    repository = MasteryRepository(settings.database_url, BKTParameters(settings.bkt_initial, settings.bkt_guess, settings.bkt_slip, settings.bkt_learn))
    return settings, store, RAGService(store, llm), QuizGenerator(store, llm), QuizGrader(llm), repository


settings, store, rag, generator, grader, repository = services()
st.title("📚 CoursePilot")
st.caption("上传课程资料，检索问答、完成测验并跟踪知识点掌握度。")
upload_tab, qa_tab, quiz_tab, dashboard_tab = st.tabs(["资料上传", "问答", "测验", "掌握度看板"])
with upload_tab:
    render_upload(store, settings)
with qa_tab:
    render_qa(rag)
with quiz_tab:
    render_quiz(generator, grader, repository, store.sections())
with dashboard_tab:
    render_dashboard(repository)
