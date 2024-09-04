import openai

import openai_responses
from openai_responses import OpenAIMock


@openai_responses.mock()
def test_create_chat_completion(openai_mock: OpenAIMock):
    openai_mock.chat.completions.create.response = {
        "choices": [
            {
                "index": 0,
                "finish_reason": "stop",
                "message": {"content": "Hello! How can I help?", "role": "assistant"},
            }
        ]
    }

    client = openai.Client(api_key="sk-fake123")
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI customer support assistant. "},
            {"role": "user", "content": """Customer Inquiry: how do I reset my password?

Relevant Support Tickets:

Ticket 1:
Q: How do I reset my password?
A: You can reset your password by following these steps:
1. Go to the login page
2. Click on the 'Forgot Password' link
3. Enter your email address
4. Check your email for a password reset link
5. Click the link and enter a new password
If you have any issues, please don't hesitate to contact us.
Tags: password, reset, login"""},
        ],
    )

    assert len(completion.choices) == 1
    assert completion.choices[0].message.content == "Hello! How can I help?"
    assert openai_mock.chat.completions.create.route.call_count == 1