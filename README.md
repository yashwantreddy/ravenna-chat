# Ravenna Chat API

This private project implements a chatbot API that uses BM25 search to find relevant support tickets and OpenAI's GPT-4o-mini to generate human-like responses. It's designed to assist customer support agents by providing AI-generated responses based on existing support ticket data.

## Deployed Endpoint

[https://ravenna-chat-laslqys9a-yash-jankays-projects.vercel.app/](https://ravenna-chat-laslqys9a-yash-jankays-projects.vercel.app/)

To make a request, send a POST request to the `/chat` endpoint with a JSON payload:

```json
{
  "question": "How do I reset my password?"
}
```


## Architecture

The application consists of the following main components:

![architecture](assets/arch.png)

1. Python App: FastAPI-based application that handles HTTP requests and orchestrates the chatbot logic.
2. Supabase: Database for storing and retrieving support tickets.
3. LangSmith: Used for traceability and debugging.
4. OpenAI's `GPT-4o-mini`: Used for generating responses.
5. Vercel: Used for hosting the API.

## Features

- `BM25` search for finding relevant support tickets
- Integration with OpenAI's `GPT-4o-mini` for generating responses
- Tag-based scoring to improve search relevance
- Configurable relevance threshold for determining when to use AI-generated responses
- FastAPI for high-performance API endpoints
- Comprehensive test suite using `pytest`

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/chatbot-api.git
   cd chatbot-api
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Start the FastAPI server:
   ```
   uvicorn app.main:app --reload
   ```

2. The API will be available at `http://localhost:8000`. You can access the interactive API documentation at `http://localhost:8000/docs`.

3. To use the chatbot, send a POST request to the `/chat` endpoint with a JSON payload:
   ```json
   {
     "question": "How do I reset my password?"
   }
   ```

4. The API will respond with a JSON object containing the generated response:
   ```json
   {
     "response": "To reset your password, please follow these steps..."
   }
   ```

## Configuration

You can adjust the BM25 search parameters in `app/main.py`:

```python
bm25_searcher = BM25Searcher(threshold=7.0, tag_boost=2.0)
```

- `threshold`: Minimum relevance score for a ticket to be considered
- `tag_boost`: Score boost applied for matching tags

## Testing

Run the test suite using pytest:

```
pytest
```

## Deployment

This application can be deployed to various cloud platforms. Here are general steps for deployment:

1. Ensure all dependencies are in `requirements.txt`
2. Set up environment variables on your hosting platform
3. Configure your hosting platform to run the FastAPI application

For specific deployment instructions, refer to your chosen hosting platform's documentation.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI](https://openai.com/)
- [rank_bm25](https://github.com/dorianbrown/rank_bm25)