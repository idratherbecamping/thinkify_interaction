# Thinkify Chat Backend

This is a simple FastAPI backend that connects to OpenAI's API to generate jokes based on user input.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file:
```bash
cp .env.example .env
```

3. Add your OpenAI API key to the `.env` file:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Running the Server

Start the server with:
```bash
python main.py
```

The server will run on `http://localhost:8000`

## API Endpoint

- POST `/chat`
  - Request body: `{"message": "your message here"}`
  - Response: `{"response": "AI's joke response"}`

## Frontend Integration

To integrate with your Thinkify frontend, make POST requests to `http://localhost:8000/chat` with the user's message. The response will contain the AI's joke. 