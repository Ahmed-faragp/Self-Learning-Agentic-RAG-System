from fastapi import FastAPI
from pydantic import BaseModel
from graph import app as graph_app   # your compiled LangGraph
from rag import add_document_to_chroma

app = FastAPI()




class QueryRequest(BaseModel):
    question: str


class TeachRequest(BaseModel):
    function_name: str
    code: str
    explanation: str




def init_state(question: str):
    return {
        "question": question,
        "context": "",
        "prompt": [],
        "memory_summary": "",
        "memory_messages": [],
        "response": "",
        "mode": "",
        "similarity_score": 0.0,
        "is_confident": False
    }




@app.post("/query")
def query(req: QueryRequest):
    state = init_state(req.question)

    result = graph_app.invoke(state)

    return {
        "mode": result.get("mode", ""),
        "response": result.get("response", "")
    }


@app.post("/teach")
def teach(req: TeachRequest):
    add_document_to_chroma(
        req.function_name,
        req.code,
        req.explanation
    )

    return {
        "message": "Knowledge added successfully"
    }