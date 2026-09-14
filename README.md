# MIDA

Multi-document Intelligence & Discovery Assistant. Basically a RAG project — upload a document or drop in a website link and you can ask it questions or get a summary instead of reading the whole thing.

I made this to actually learn how RAG works instead of just watching another tutorial on it. Frontend is just Streamlit, didn't want to spend time on that part.

### what it does

- upload a pdf/docx/txt and it'll pull the text out
- or give it a url and it scrapes the page instead
- once something's loaded you can chat with it — it embeds your question, pulls the closest matching chunks from a chroma vector db, and feeds those to the model as context so it's not just hallucinating
- can also generate a summary. long docs get split into chunks, each chunk gets summarized, then those summaries get combined into one final summary (couldn't just dump the whole doc into one prompt, context limit)
- no doc loaded = it just acts like a normal chatbot

### stack

streamlit, groq (llama-3.3-70b-versatile), chromadb, sentence-transformers for embeddings, pymupdf for pdfs, python-docx, playwright + bs4 for scraping sites.

### structure

- `app.py` — landing page
- `pages/1_Research.py` — upload/url + summary button
- `pages/2_Chat.py` — chat, uses RAG search
- `pages/3_Documents.py` — also chat but dumps whole doc into the prompt instead of searching. kind of redundant with Chat honestly, need to fix that at some point
- `parsers/` — pdf/docx/txt/web extraction, one file each
- `services/llm_service.py` — groq call + system prompt
- `services/rag_service.py` — chunking, embedding, chroma search
- `services/summary_service.py` — the chunk-then-combine summarizer
- `vector_db/` — where chroma stores stuff, gets created on its own

### running it

need python 3.10+ and a groq api key (free at console.groq.com)

```
git clone https://github.com/Jaschrome/mida.git
cd mida
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

requirements.txt is missing a few things I forgot to add before pushing, so also run:

```
pip install groq chromadb sentence-transformers
playwright install firefox
```

make a `.env` file:

```
GROQ_API_KEY=your_key_here
```

then

```
streamlit run app.py
```

opens at localhost:8501, sidebar has the different pages.

### known issues

- requirements.txt out of date (see above)
- there's a test_gemini.py and an empty gemini_service.py in there, was going to add gemini as a second model option but never finished it, ignore those
- Chat and Documents pages overlap a lot, one uses RAG and one just shoves the whole doc in, should probably merge them
- vector db never gets cleared out between sessions so it just accumulates old documents over time

still pretty rough but it works. might keep adding to it.
