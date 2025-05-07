# Chainlit Demo Application

A chat interface demo built with Chainlit, showcasing how to create interactive AI assistants with streaming responses.

## Features

- Interactive chat interface with Chainlit
- Streaming responses for real-time feedback
- Message history and context management
- Proper environment configuration
- Easy deployment

## Overview

This application demonstrates how to build a chat interface using Chainlit, which provides a user-friendly UI for interacting with large language models. The application generates responses to user queries in real-time.

## Setup Instructions

### Prerequisites

- Python 3.9+

### Installation

1. Navigate to the project directory:
   ```
   cd 02_demo_chainlit
   ```

2. Create and activate a virtual environment:
   ```
   # Using uv (recommended)
   uv venv

   # Or using standard venv
   python -m venv .venv
   
   # Activate on Windows
   .venv\Scripts\activate
   
   # Activate on macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```
   # Using uv
   uv pip install -e .
   
   # Or using pip
   pip install -e .
   ```

## Running the Application

To start the Chainlit application:

```bash
uv run app
```

The application will be available at http://localhost:8000 in your web browser.
And Chat interface will be available at http://localhost:8000/chainlit in your web browser.

## Project Structure

- `src/` - Source code directory
  - `app.py` - Main application file
  - Additional modules and utilities
- `.chainlit/` - Chainlit configuration
- `chainlit.md` - Welcome message for the chat interface
- `pyproject.toml` - Project dependencies and configuration

## Usage

1. Open the application in your web browser
2. Enter your query or question in the chat input
3. The AI will respond with streaming text in real-time
4. Continue the conversation as needed


