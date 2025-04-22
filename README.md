# Postgres Agent with MCP and OpenAI

This project provides a simple agent that connects to a PostgreSQL database and allows natural language queries using OpenAI's API. It uses a custom MCP (Multi-Component Protocol) server to expose database tools, and an agent that interacts with the server via SSE (Server-Sent Events).

## Features

- **Describe database schema:** List tables and columns in your PostgreSQL database.
- **Run safe SQL queries:** Execute only `SELECT` statements for security.
- **Natural language interface:** Ask questions in natural language and get answers from the database.
- **OpenAI integration:** Uses OpenAI's API for language understanding.

## Requirements

- Python 3.10+
- A PostgreSQL database (connection string required)
- OpenAI API key

## Installation

1. **Clone the repository:**

2. **Create and activate a virtual environment:**

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**

   Create a `.env` file in the project root with the following content:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   DSN=your_postgres_connection_string
   ```

   **Note:** Never commit your `.env` file. It is already included in `.gitignore`.

## Usage

### 1. Start the MCP server

This exposes the database tools via HTTP/SSE.

```bash
python server.py
```

The server will run on `http://localhost:8000/sse`.

### 2. Run the agent

In another terminal (with the virtual environment activated):

```bash
python agent.py
```

You can now type questions about your database in natural language. The agent will use the tools to answer your questions.

## Security

- Only `SELECT` queries are allowed for safety.
