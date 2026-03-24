from typing import TypedDict 
from langgraph.graph  import START , END, StateGraph
from rag import add_document_to_chroma, classify_intent, generate_prompt, get_memory_messages,multiline_input,client
from chroma_vdb import retrieve_with_confidence
from memory import load_memory_from_file,conversation, save_memory_to_file



class Agentstate(TypedDict):
    context: str
    prompt : list[dict]
    mode: str
    memory_summary: str
    response: str
    question: str
    memory_messages: list[dict]
    similarity_score: float
   
def retrieval_node(state: Agentstate) -> Agentstate:
    load_memory_from_file()
    context, score = retrieve_with_confidence(state['question'])
    state['context'] = "\n\n".join(context)
    state['similarity_score'] = score
    return state

def learning_node(state: Agentstate) -> Agentstate:
    state["response"] = "I don't know this yet. Please POST to /teach with function_name, code, explanation."
    return state

def intent_classification_node(state: Agentstate) -> Agentstate:

    state['mode'] = classify_intent(state['question'])
    return state

def explanation_node(state: Agentstate) -> Agentstate:
    
    state['prompt'] = generate_prompt("explanation", state['question'], state['context'], state['memory_summary'])
    return state

def generation_node(state: Agentstate) -> Agentstate:
    
    state['prompt'] = generate_prompt("generation", state['question'], state['context'], state['memory_summary'])
    return state



def response_generation_node(state: Agentstate) -> Agentstate:
   
    load_memory_from_file()
    state["memory_summary"] = conversation.memory.buffer
    state['memory_messages'] = get_memory_messages()
    messages = state['memory_messages'] + state['prompt']
    response = client.chat.completions.create(
         model="meta-llama/llama-3-8b-instruct", 
         messages=messages
            )
    conversation.memory.save_context({"input": state['question']}, {"output": response.choices[0].message.content})
    save_memory_to_file()
    state['response'] = response.choices[0].message.content
    return state


graph = StateGraph(Agentstate)
graph.add_node( "retrieval",retrieval_node)
graph.add_edge(START, "retrieval")
graph.add_node( "intent_classification",intent_classification_node)
graph.add_node( "learning",learning_node)
graph.add_conditional_edges(
    "retrieval",
    
        lambda state: "learning" if state["similarity_score"] > 0.7 else "intent_classification"
    
)
graph.add_node( "explanation",explanation_node)
graph.add_node( "generation",generation_node)
graph.add_conditional_edges(
    "intent_classification",
    
        lambda state: "explanation" if state["mode"] == "explanation" else "generation"
    
)
graph.add_node( "response_generation",response_generation_node)
graph.add_edge("explanation", "response_generation")
graph.add_edge("generation", "response_generation")
graph.add_edge("response_generation", END)
graph.add_edge("learning", END)


app = graph.compile()
app.invoke({
    "question": "...",
    "context": "",
    "prompt": [],
    "memory_summary": "",
    "memory_messages": [],
    "response": "",
    "mode": "",
    "similarity_score": 0.0,
    "is_confident": False
})
print(app.get_graph().draw_mermaid())