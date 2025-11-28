# Support Assistant — Full Beginner Project

This expanded project is a beginner-friendly Support Assistant chatbot built with Streamlit and OpenAI.
It answers user questions using a local FAQ file (`faqs.txt`). For near-matches it uses a lightweight
fuzzy search to find relevant FAQ entries; for other cases it uses the OpenAI API with strict instructions
to escalate when the FAQ doesn't contain an answer.

## What you'll find in this project
- `main.py` — Streamlit app (chat UI, FAQ upload, fuzzy FAQ search, OpenAI calls)
- `faqs.txt` — example FAQ knowledge base
- `requirements.txt` — Python deps
- `.env.example` — example environment variables
- `README.md` — this file

## How to run locally (step-by-step)
1. Create a Python 3.10+ virtual environment and activate it.
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux / macOS
   venv\Scripts\activate   # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your OpenAI API key:
   - Copy `.env.example` to `.env` and fill your key:
     ```
     OPENAI_API_KEY=sk-...
     ```

4. (Optional) Edit `faqs.txt` to add your organization's FAQs.

5. Run the app:
   ```bash
   streamlit run main.py
   ```

## Deployment suggestions
- Deploy to Streamlit Cloud or Render. Add a `requirements.txt` and point to `main.py`.
- Make sure to configure `OPENAI_API_KEY` in the deployment environment.

## Potential improvements
- Add vector search (Chroma/FAISS/Pinecone) for larger knowledge bases.
- Add user authentication and chat persistence (database).
- Add a small "handoff" UI for live agents.

## Notes for beginners
- This project keeps things intentionally simple. The fuzzy matching + instructing the model leads to more reliable results than relying on model “memory” alone.
