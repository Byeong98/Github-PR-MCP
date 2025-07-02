import asyncio
from mcp_server import mcp


if __name__ == "__main__":
    asyncio.run(mcp.run(transport='stdio'))
