# FastAPI WebSocket Demo

A simple FastAPI application with RESTful endpoints and WebSocket support.

## Features

- RESTful API for CRUD operations on items
- Real-time updates via WebSocket
- In-memory data storage for demonstration

## Installation

```bash
# Navigate to the project directory
cd 03_demo_fastapi_websocket

# Install dependencies using pip
uv sync
```

## Running the Application

```bash
# Run the application using the installed script
uv run app
```

The server will start at http://0.0.0.0:8000

## API Endpoints

- `GET /` - Welcome message
- `GET /items` - List all items
- `GET /items/{item_id}` - Get a specific item
- `POST /items` - Create a new item
- `PUT /items/{item_id}` - Update an existing item
- `DELETE /items/{item_id}` - Delete an item

## WebSocket

Connect to the WebSocket at `ws://localhost:8000/ws` to receive real-time updates when items are created, updated, or deleted.

## API Documentation

FastAPI automatically generates API documentation:

- Swagger UI: http://localhost:8000/docs
