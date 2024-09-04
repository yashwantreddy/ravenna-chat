from pydantic import BaseModel

class CustomerInquiry(BaseModel):
    question: str

class ChatbotResponse(BaseModel):
    response: str