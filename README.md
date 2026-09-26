# CoursePilot

一个面向大学生的本地课程资料 RAG 助手。上传 PDF、PPTX 或 TXT 后，可检索问答、生成章节测验，并以简化贝叶斯知识追踪（BKT）展示掌握度和复习顺序。

## 功能

- 解析 PDF（逐页）、PPTX（逐张幻灯片）和 UTF-8/GB18030 TXT；扫描版 PDF 不含 OCR。
- 识别标题与段落切分资料，将片段和来源元数据持久化到 ChromaDB。
- 基于本地 SentenceTransformers 检索，并通过 OpenAI 兼容 LLM 生成带文件/章节/位置引用的回答。
- 针对所选章节生成 3 道单选题和 2 道简答题；简答由 LLM 自动评分。
- 用 SQLite 保存答题历史，并以 BKT 给出知识点掌握概率与最优复习顺序。

## 快速开始

创建虚拟环境、安装依赖后，编辑项目中的 `.euv` 并填写模型服务信息：

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Windows PowerShell 可使用：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

应用默认在 `http://localhost:8501` 提供服务。

首次载入时，`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` 会下载到本机模型缓存，因此需要网络连接。若公司网络限制下载，请预先缓存该模型，或在 `.euv` 中改为可用的 SentenceTransformers 模型名称。

## 环境变量

| 变量 | 用途 |
| --- | --- |
| `LLM_API_KEY` | 模型服务的 API Key，问答、生成题目和简答评分均需要。 |
| `LLM_BASE_URL` | 模型服务的 OpenAI 兼容 Chat Completions API 基础 URL。 |
| `LLM_MODEL` | 服务商要求的模型标识。 |
| `DATA_DIR` | ChromaDB 和 SQLite 的本地保存目录，默认 `data`。 |
| `EMBEDDING_MODEL` | SentenceTransformers 模型名。 |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | 文本切分长度和重叠长度。 |
| `BKT_INITIAL` / `BKT_GUESS` / `BKT_SLIP` / `BKT_LEARN` | BKT 参数。 |

只需要修改 `.euv` 中的三项 `LLM_*` 配置即可切换 OpenAI、DeepSeek、Qwen、智谱、Moonshot、OpenRouter 或任意 OpenAI 兼容服务。对于原生 API 不兼容 Chat Completions 的模型，请填入 LiteLLM 等兼容网关的地址。旧的 `.env` 文件和 `OPENAI_*` 变量仍然可用。
没有配置 `LLM_API_KEY` 时，资料上传和本地数据看板仍可用；LLM 相关操作会给出配置提示，而不会生成虚构结果。

## Docker

```bash
docker build -t coursepilot .
docker run --rm -p 8501:8501 --env-file .euv -v "${PWD}/data:/app/data" coursepilot
```

打开 `http://localhost:8501`。Docker 镜像使用 Python 3.11；`data/` 挂载卷用于保存向量索引和答题记录。

## 开发验证

```bash
pytest -q
```

测试不调用真实 LLM 或嵌入服务。
