import asyncio
from mcp_server import mcp

def main():
    asyncio.run(mcp.run(transport='stdio'))

if __name__ == "__main__":
    main()
    