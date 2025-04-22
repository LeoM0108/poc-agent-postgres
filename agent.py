import asyncio, os
from dotenv import load_dotenv
from agents import Agent, Runner            # núcleo do SDK
from agents.mcp import MCPServerSse         # cliente SSE p/ MCP

load_dotenv(".env")                         # carrega OPENAI_API_KEY

SYSTEM_PROMPT = """
Você é o DataAnswer‑Bot.

• Se não souber o esquema, chame describe_schema primeiro.
• Quando tiver SQL pronto, chame query.
• Responda em PT‑BR, só com a informação solicitada (sem SQL).
"""

# URL do endpoint SSE que seu server.py expõe
SSE_URL = "http://localhost:8000/sse"


async def main() -> None:
    # abre conexão com o servidor MCP
    async with MCPServerSse(name="Postgres MCP", params={"url": SSE_URL}) as server:

        # cria o agente e registra o servidor
        bot = Agent(
            name="DataAnswerBot",
            instructions=SYSTEM_PROMPT,
            mcp_servers=[server],
        )

        # loop de perguntas
        while True:
            try:
                q = input("Pergunta > ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not q:
                continue

            result = await Runner.run(starting_agent=bot, input=q)
            print("→", result.final_output)


if __name__ == "__main__":
    asyncio.run(main())