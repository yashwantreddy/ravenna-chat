from fastapi import FastAPI
from app.models.schemas import CustomerInquiry, ChatbotResponse
from app.search.bm25_search import BM25Searcher
from app.utils.openai_helper import generate_response
from langsmith import traceable

app = FastAPI()
bm25_searcher = BM25Searcher()

@traceable
@app.post("/chat", response_model=ChatbotResponse)
async def chat(inquiry: CustomerInquiry):
    relevant_tickets, scores = bm25_searcher.search(inquiry.question)
    
    if not bm25_searcher.is_query_supported(scores):
        return ChatbotResponse(response="I'm sorry, but I couldn't find any relevant information to answer your question. It would be best to contact our human support team for assistance with this inquiry. They'll be able to provide you with more specific and accurate information. Is there anything else I can help you with?")
    
    response = generate_response(inquiry.question, relevant_tickets)
    return ChatbotResponse(response=response)

@app.get("/")
async def health_check():
    return {"status": "ok"}