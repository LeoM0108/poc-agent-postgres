# server.py
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import psycopg, os

load_dotenv(".env")
DB_DSN = os.getenv("DSN")
print(DB_DSN)
if not DB_DSN:
    raise RuntimeError("Faltou DSN no .env ou no ambiente")

mcp = FastMCP("postgres_tools") 

# -------------------------------------------------------------------
# TOOLS
# -------------------------------------------------------------------
@mcp.tool()
def describe_schema(table: str | None = None) -> dict:
    """
    Lista tabelas/colunas do schema public (ou só da tabela informada).
    """
    sql = """
        SELECT table_name, column_name, data_type
          FROM information_schema.columns
         WHERE table_schema = 'public' {extra}
         ORDER BY table_name, ordinal_position
    """.format(extra="AND table_name = %s" if table else "")
    with psycopg.connect(DB_DSN) as conn, conn.cursor() as cur:
        cur.execute(sql, (table,) if table else ())
        rows = cur.fetchall()

    out: dict[str, list[dict[str, str]]] = {}
    for tbl, col, typ in rows:
        out.setdefault(tbl, []).append({"column": col, "type": typ})
    return out


@mcp.tool()
def query(sql: str) -> list[list]:
    """
    Executa um SELECT e devolve as linhas.  
    Bloqueia UPDATE/DELETE/INSERT por segurança.
    """
    if not sql.lower().lstrip().startswith("select"):
        raise ValueError("Somente SELECT é permitido.")
    with psycopg.connect(DB_DSN) as conn, conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()

# -------------------------------------------------------------------
# Execução direta  →  `python server.py`
# -------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run(
        transport="sse",     # → roda um servidor HTTP/SSE em localhost:8000
    )