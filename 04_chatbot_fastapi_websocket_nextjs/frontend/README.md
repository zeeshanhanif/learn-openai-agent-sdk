# Chatbot Frontend

This is a Next.js frontend for the WebSocket-based chatbot application.

## Features

- Real-time chat interface using WebSockets
- Beautiful responsive UI with Tailwind CSS
- Dark mode support
- Connection status indicator
- Auto-scrolling messages
- Timestamp display for messages

## Getting Started

### Prerequisites

- Node.js 20.x or later
- npm or yarn

### Installation

1. Clone the repository
2. Navigate to the frontend directory:
   ```
   cd 04_chatbot_fastapi_websocket_nextjs/frontend
   ```
3. Install dependencies:
   ```
   npm install
   ```

### Running the Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Usage

1. Start the FastAPI backend server first (see backend README for instructions)
2. Open the frontend application in your browser
3. Wait for the WebSocket connection to be established
4. Start chatting with the bot

## Project Structure

- `app/` - Contains the main Next.js application pages
- `components/` - React components for the chat interface
  - `ChatHeader.tsx` - Header component with connection status
  - `MessageList.tsx` - Component to display messages
  - `ChatInput.tsx` - Input area for sending messages
  - `ConnectingOverlay.tsx` - Loading overlay while connecting

## Configuration

The WebSocket URL is currently set to `ws://localhost:8000/ws`. To change this, modify the WebSocket URL in `app/page.tsx`.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
