#  Self-Learning Coding Agent (LangGraph + RAG + FastAPI + Docker)

An AI-powered coding assistant that combines **Retrieval-Augmented Generation (RAG)**, **LangGraph-based control flow**, **persistent memory**, and **self-learning capabilities**.

Unlike basic RAG systems, this agent can **learn new code dynamically** when it fails to retrieve relevant context.

---

#  Features

##  1. Semantic Code Retrieval

* Uses **ChromaDB** with embeddings (`all-MiniLM-L6-v2`)
* Preloaded with HumanEval dataset
* Retrieves top-k relevant code examples

---

##  2. LangGraph Control Flow

* Structured execution using **LangGraph**
* Clear nodes:

  * Retrieval
  * Learning
  * Intent Classification
  * Generation / Explanation
  * Response
* Conditional routing based on:

  * Retrieval confidence
  * User intent

---

##  3. Self-Learning System

If no relevant context is found:

* Agent switches to **learning mode**
* Prompts user to provide:

  * function name
  * code
  * explanation
* Stores knowledge in vector database (ChromaDB)

---

##  4. Persistent Memory

* Uses conversation memory
* Stored in `memory.json`
* Maintains context across sessions

---

##  5. FastAPI Deployment

* REST API interface
* Endpoints:

  * `POST /query` → Ask questions
  * `POST /teach` → Teach new functions

---

##  6. Dockerized Application

* Fully containerized using Docker
* Easy to run anywhere

---

#  Architecture

```
User Request
     ↓
FastAPI (/query)
     ↓
LangGraph
     ↓
Retrieval Node
     ↓
Confidence Check
 ┌───────────────┐
 │               │
 ↓               ↓
Learning     Intent Classification
                 ↓
        ┌──────────────┐
        ↓              ↓
   Generation     Explanation
        ↓              ↓
        └──────→ Response Node
                     ↓
                 API Response
```

---

#  Project Structure

```
.
├── app.py                 # FastAPI application
├── graph.py               # LangGraph workflow
├── rag.py                 # Core RAG logic
├── chroma_vdb.py          # Vector database
├── memory.py              # Memory handling
├── prompt_sys.py          # Prompt templates
├── routing.py             # Intent classification
├── requirements.txt
├── Dockerfile
├── memory.json
└── chroma_db/
```

---

#  Installation (Local)

```bash
git clone <your-repo>
cd deployment

pip install -r requirements.txt
```

---

#  Environment Setup

Create `.env` file:

```
OPENROUTER_API_KEY=your_api_key_here
```

---

#  Run Locally

```bash
uvicorn app:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

#  API Usage

##  Query

```http
POST /query
```

```json
{
  "question": "How do I reverse a linked list?"
}
```

---

##  Teach (Learning Mode)

```http
POST /teach
```

```json
{
  "function_name": "reverse_list",
  "code": "def reverse_list(...): ...",
  "explanation": "Reverses a linked list"
}
```

---

#  Docker Setup

##  Build Image

```bash
docker build -t rag-assistant .
```

---

##  Run Container

```bash
docker run -p 8000:8000 rag-assistant
```

---

##  Access API

```
http://127.0.0.1:8000/docs
```

---

#  Notes

* HumanEval dataset does **not include complex structures like linked lists**
* Retrieval may return unrelated results → handled via learning mode
* Docker rebuild required when dependencies change

---

#  Key Concepts Demonstrated

* Retrieval-Augmented Generation (RAG)
* Graph-based AI workflows (LangGraph)
* Stateful AI systems
* API-based AI deployment
* Containerization with Docker

---



#  Summary

This project demonstrates a **production-style AI system** that:

* Retrieves knowledge
* Reasons about confidence
* Learns dynamically
* Exposes functionality via API
* Runs in a containerized environment

---

#  Author

Built as part of an NLP Internship task.
