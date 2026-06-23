from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
chain = None
class Query(BaseModel):
    x : str
@app.post("/")
def prompt(query : Query):
    from rag_pipeline import llm_answer, build_chain
    chain = build_chain()
    result = llm_answer(query.x,  chain)
    return {"answer":result}