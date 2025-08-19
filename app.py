from fastapi import FastAPI, Request
import uvicorn
from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")

@app.post("/blogs")
async def generate_blog(request:Request):
    data =await request.json()
    topic = data.get("topic", "")
    
    # calling llm object
    llm_obj = GroqLLM()
    llm = llm_obj.get_llm()
    graph_obj = GraphBuilder(llm)
    if not topic:
        return {"error": "No topic provided"}
    else:
        graph = graph_obj.setup_graph(usecase="topic")
        state = graph.invoke({"topic":topic})
    return {"data":state}

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000)
