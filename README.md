# 🏞️ Ella Tourism Information Assistant


<img width="559" height="326" alt="image" src="https://github.com/user-attachments/assets/18eac88e-a495-4e07-851a-c9499955d98b" />


A multi-agent RAG application that answers traveler questions about **Ella, Sri Lanka** -
attractions, hotels, transport, and local culture  built to satisfy an assignment
brief requiring: 2+ agents, 3+ agentic design patterns, 2+ LLMs, a RAG system with
20+ documents, a Streamlit UI, and a live deployment.

---

## 1. Problem & Scope

Tourists researching Ella have to piece together information from scattered blogs,
outdated guidebooks, and inconsistent forum posts. This assistant provides a single
place to ask natural-language questions and get grounded, source-backed answers.

**Users:** Independent travelers planning a visit to Ella.
**Knowledge base source:** 22 original reference documents written for this project,
covering attractions, hotels, transport, and culture (see `/data`).

---

## 2. System Architecture

<img width="600" height="700" alt="image-1" src="https://github.com/user-attachments/assets/d59aec52-97a7-4188-8295-bbef90d1b14d" />
                              ##draw.io

### Why two agents, not one?
Splitting query understanding from answer generation lets us use a small, fast,
cheap model for the simple classification step, and reserve the larger reasoning
model for the harder job of synthesizing multiple retrieved chunks into a coherent,
accurate answer. This is also the cleanest way to demonstrate genuine
**agent-to-agent structured communication**: Agent 1 emits a JSON message that
Agent 2 consumes as its input.

### Sequence Diagram - Agent-to-Agent Communication 

<img width="1000" height="700" alt="image" src="https://github.com/user-attachments/assets/7f38b229-d287-4c49-926b-b5a777531895" />
                                               ##draw.io


## 3. Agentic Design Patterns (3 required, 4 implemented)

| # | Pattern | Where it lives | What it does |
|---|---------|----------------|--------------|
| 1 | **Routing** | `agents/router_agent.py` | Classifies the question into `attractions / hotels / transport / culture / general` so retrieval can be filtered to the right slice of the knowledge base. |
| 2 | **Planning** | `agents/router_agent.py` | Rewrites vague user phrasing ("how do I get there?") into a clear, standalone search query before it's handed off. |
| 3 | **Tool Use** | `agents/answer_agent.py` | Agent 2 explicitly calls `rag/retriever.py`'s `retrieve()` function as a tool to fetch grounding context, rather than answering from memory. |
| 4 | **Reflection** | `agents/answer_agent.py` | After drafting an answer, the agent re-reads its own draft against the retrieved source chunks, checks for unsupported claims or missing details, and produces a corrected final answer. |



---

## 4. Model Selection & Justification

| Task | Model | Provider | Why this model |
|------|-------|----------|-----------------|
| Query routing & rewriting | `llama-3.1-8b-instant` | Groq | Classification is a low-complexity task; Groq's inference speed keeps the UI snappy, and an 8B model is more than capable of a 5-way classification + one-sentence rewrite. Cheapest tier of the pipeline. |
| Answer generation + reflection | `gpt-4o-mini` | OpenRouter | Needs to synthesize 4 retrieved chunks into a coherent answer and then critique its own output — a task that benefits from stronger reasoning and larger context handling than the router step. (Swappable for `anthropic/claude-3.5-sonnet` via OpenRouter if higher quality is preferred over cost.) |

This satisfies the "2+ different LLMs" requirement, and the two providers (Groq +
OpenRouter) are combined explicitly, as permitted by the brief.

**Trade-off notes:**
- Latency: Groq's speed offsets the extra round-trip of a 2-agent pipeline.
- Cost: routing/classification tokens are cheap and frequent; reasoning tokens are
  more expensive but used only once per user question.
- Context window: both models comfortably handle the ~2-4k tokens of retrieved
  context used here.

---

## 5. RAG Pipeline

```
data/*.txt  (22 documents: attractions, hotels, transport, culture)
     │
     ▼  RecursiveCharacterTextSplitter (chunk_size=500, overlap=80)
     │
     ▼  HuggingFaceEmbeddings ("all-MiniLM-L6-v2", local & free)
     │
     ▼  Chroma vector store (persisted to /chroma_db)
     │
     ▼  similarity_search(query, filter=category, k=4)
     │
     ▼  passed as context to Agent 2
```

Embeddings run locally via `sentence-transformers` so ingestion works without an
extra paid API key — only the two LLM calls (routing + answering) cost API credits.

---

## 6. Project Structure

```
ella-tourism-assistant/
├── app.py                     # Streamlit UI, orchestrates both agents
├── agents/
│   ├── router_agent.py        # Agent 1: Routing + Planning (Groq)
│   └── answer_agent.py        # Agent 2: Tool Use + Reflection (OpenRouter)
├── rag/
│   ├── ingest.py               # Builds the Chroma vector store
│   └── retriever.py            # retrieve() - the "tool" Agent 2 calls
├── data/
│   ├── attractions/            # 8 documents
│   ├── hotels/                 # 5 documents
│   ├── transport/               # 4 documents
│   └── culture/                 # 5 documents
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 7. Setup & Local Run

### Step 1 — Clone and install
```bash
git clone https://github.com/shashini2001/ella-tourism-assistant.git
cd ella-tourism-assistant
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2 — Get API keys (both free tiers available)
- Groq: https://console.groq.com/keys
- OpenRouter: https://openrouter.ai/keys

Copy `.env.example` to `.env` and fill in:
```
GROQ_API_KEY
OPENROUTER_API_KEY

```

### Step 3 — Build the knowledge base (run once)
```bash
python rag/ingest.py
```
This reads all files in `/data`, chunks them, embeds them, and saves a `chroma_db/`
folder. Re-run this any time you add or edit documents.

### Step 4 — Run the app
```bash
streamlit run app.py
```

---

## 8. Deployment (Streamlit Community Cloud)

1. Push this repo to GitHub (see commit strategy below).
2. **Important:** `chroma_db/` is git-ignored, so either:
   - (a) run `python rag/ingest.py` and remove `chroma_db/` from `.gitignore` so the
     built vector store is committed and available at deploy time, **or**
   - (b) add a one-time build step by calling `rag.ingest.build_vectorstore()` at
     app startup if `chroma_db/` doesn't exist yet.
   For a small, static 22-document knowledge base, option (a) is simplest.
3. Go to https://share.streamlit.io, connect your GitHub repo, and set `app.py` as
   the entry point.
4. Under **Settings → Secrets**, add:
   ```toml
   GROQ_API_KEY 
   OPENROUTER_API_KEY 

   ```
5. Deploy. Streamlit Cloud will install `requirements.txt` and launch the app.

---

## 9. Retrieval Quality Testing

Five sample questions were used to evaluate retrieval quality (run manually with
`show_debug` enabled in the sidebar to inspect retrieved chunks):

| # | Question | Retrieved docs relevant? | Notes / improvement ideas |
|---|----------|---------------------------|----------------------------|
| 1 | "What's the best time to visit Nine Arch Bridge?" | Yes — `nine_arch_bridge.txt` top result | Clean single-topic match |
| 2 | "How do I get from Kandy to Ella?" | Yes — `train_kandy_ella.txt`, `getting_to_ella.txt` | Category routing to "transport" worked correctly |
| 3 | "Where should I stay near Little Adam's Peak?" | Yes — `98_acres_resort.txt` | Cross-category question (hotels + attractions); router correctly picked "hotels" since that was the primary intent |
| 4 | "Is it safe to swim at Ravana Falls?" | Partial — `ravana_falls.txt` retrieved, but the doc only briefly mentions currents | Knowledge base could use a more detailed safety-specific document |
| 5 | "What should I wear when visiting a temple?" | Yes — `local_etiquette.txt` | Correctly routed to "culture" |

**Takeaway:** retrieval performs well for single-topic questions; cross-category
questions (e.g., "hike + hotel") depend heavily on the router picking the dominant
intent correctly. A possible improvement is letting Agent 1 return multiple
categories and merging retrieval results across them.

---

## 10. Git & Commit History Guidance

Suggested commit sequence (small, meaningful commits rather than one giant commit):

```
1. chore: scaffold project structure
2. feat: add knowledge base documents (attractions, hotels, transport, culture)
3. feat: implement RAG ingestion pipeline
4. feat: implement RAG retriever
5. feat: implement router agent (Groq)
6. feat: implement answer agent with reflection (OpenRouter)
7. feat: build Streamlit UI
8. docs: write README
9. chore: add requirements, .gitignore, .env.example
10. test: document retrieval quality evaluation
11. deploy: configure Streamlit Cloud secrets
```

Use a feature branch per component (e.g. `feature/router-agent`,
`feature/streamlit-ui`) and merge into `main` via pull requests to demonstrate
good workflow, as requested in the brief.

---

## 11. Limitations & Honest Caveats

- The knowledge base is a small, hand-written set of 22 documents for
  demonstration purposes — not a comprehensive or continuously updated source.
  Pricing, schedules, and hours mentioned in the documents are illustrative and
  should be verified independently before travel.
- No live weather or train-schedule API is integrated; this is a text-based RAG
  assistant, not a real-time data service.
- This is not a booking or safety-critical system.

 ---
 
## 12. Live Streamlit Community Cloud URL
  
  https://ella-tourism-assistant-5geelegesaumkducjf7tk8.streamlit.app/
  
 ---

---
## 13. Demo Video Link

 https://drive.google.com/file/d/1SucdqLzdqzb8lBX6RJjmbV_E_OM6LHsT/view?usp=sharing
 
---
