# app/utils/openai_helper.py
from openai import OpenAI
from typing import List, Dict
from dotenv import load_dotenv
from langsmith.wrappers import wrap_openai
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY, organization='org-toeu6fWf7CJhd1mUZgEQoboM')
client = wrap_openai(client)

def generate_response(customer_inquiry: str, relevant_tickets: List[Dict]) -> str:
    # Compose the prompt
    prompt = f"""
Customer Inquiry: {customer_inquiry}

Relevant Support Tickets:
"""
    
    for i, ticket in enumerate(relevant_tickets, 1):
        prompt += f"""
Ticket {i}:
Q: {ticket['customer_question']}
A: {ticket['support_agent_response']}
Tags: {', '.join(ticket['tags'])}

"""
    
    prompt += """
Using the information from these relevant support tickets, please provide a concise and helpful response to the customer's inquiry. The response should:
1. Directly address the customer's question or concern
2. Be polite and professional
3. Include relevant details from the support tickets without directly quoting them

Important: If there is no relevant information in the tickets, please say so and offer to connect the customer with a human agent.

Your response:"""

    # Call the OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI customer support assistant. Your task is to provide a helpful response to a customer inquiry based on relevant information from previous support tickets."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.5,
    )

    # Extract and return the generated response
    return response.choices[0].message.content