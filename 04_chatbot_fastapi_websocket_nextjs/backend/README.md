# FastAPI WebSocket Chat with Next.js UI and OpenAI Integration

This project demonstrates a real-time chat application built with:
- **FastAPI** for the backend WebSocket API
- **OpenAI** for AI-powered chat responses
- **Next.js** for a beautiful, responsive frontend UI

## Project Structure

```
├── src/
│   └── chatbot_fastapi_websocket_nextjs/
│       ├── agent.py   # OpenAI Agent integration
│       ├── app.py     # FastAPI application with WebSocket endpoint
│
├── frontend/          # Next.js frontend application
│   ├── app/           # Next.js pages and layouts
│   ├── components/    # React components for chat UI
│   ├── public/        # Static assets
│   └── ...            # Next.js config files
│
├── pyproject.toml     # Python project configuration
└── README.md          # Project documentation
```

## Setup and Installation

### Backend

1. Create a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install the project in development mode:
   ```bash
   pip install -e .
   ```

3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Running the Application

### Backend

Start the FastAPI server:
```bash
python -m chatbot_fastapi_websocket_nextjs
```

Or with uvicorn directly:
```bash
uvicorn chatbot_fastapi_websocket_nextjs.app:app --reload
```

The server will run at http://localhost:8000.

### Frontend

Start the Next.js development server:
```bash
cd frontend
npm run dev
```

The frontend will be available at http://localhost:3000.

## Features

- Real-time bidirectional communication via WebSockets
- AI-powered responses using OpenAI's API
- Beautiful and responsive chat UI with:
  - Message history with user/assistant styling
  - Connection status indicator
  - Smooth scrolling and animations
  - Input with send button and enter key support
  - Auto-reconnection on disconnection

## API Documentation

The FastAPI server provides:
- WebSocket endpoint at `/ws` for real-time chat
- Documentation at `/docs` (Swagger UI) and `/redoc` (ReDoc)

## Message Format

Messages are sent over WebSockets using JSON:

```json
{
  "type": "message",
  "content": "Your message here"
}
```

## License

This project is open-source. Feel free to use and modify as needed.
