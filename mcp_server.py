from mcp.server.fastmcp import FastMCP
from utils.git_utils import GitUtils
from typing import Annotated
from pydantic import Field
import json
import os

mcp = FastMCP("github-pr-mcp")
git_util = GitUtils()


@mcp.tool()
async def create_github_pr_url( 
    github_url: Annotated[str, Field(
        description="https://github.com/<owner>/<repo> 형식의 GitHub URL",
        pattern=r"^https://github\.com/.+/.+$"
    )],
    head_branch: Annotated[str, Field(description="머지 대상 브랜치")],
    title: Annotated[str, Field(description="PR 제목")],
    body: Annotated[str, Field(description="PR 본문")],
    base_branch: Annotated[str, Field(description="기준 브랜치")] = "main",
) -> str:
    """
    GitHub Compare URL을 생성해 ‘Create Pull Request’ 화면으로 바로 이동시킵니다.
    반드시 GitHub URL, 머지 대상 브랜치, PR 제목, PR 본문, 기준 브랜치를 받아야 합니다.
    """
    try:
        pr_url = git_util.github_pr_url(github_url,
                                        head_branch,
                                        title,
                                        body,
                                        base_branch)
        return json.dumps({"status": "success",
                           "pr_url": pr_url})
    except Exception as e:
        return json.dumps({"status": "error",
                           "message": str(e)})
