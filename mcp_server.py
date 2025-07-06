from mcp.server.fastmcp import FastMCP
from utils.git_utils import GitUtils
from typing import Annotated
from pydantic import Field, HttpUrl
import json
import os

mcp = FastMCP("github-pr-mcp")
git_util = GitUtils()


@mcp.tool(description=(
    "GitHub Compare URL(→ PR 작성 화면)을 **즉시** 생성합니다. "
    "필요 값이(repo, head, title, body) 준비되면 반드시 이 툴을 호출하세요."
))
async def create_github_pr_url(
    github_url: Annotated[str, Field(
        description="https://github.com/<owner>/<repo> 형식",
        pattern=r"^https://github\.com/.+/.+$"
    )],
    head_branch: Annotated[str, Field(
        description="PR 원본 브랜치 ",
        examples=["feature/login-ui"]
    )],
    title: Annotated[str, Field(description="PR 제목")],
    body: Annotated[str, Field(description="PR 본문")],
    base_branch="main",
) -> HttpUrl:
    """
    repo, head, title, body 네 줄만 입력 -> 툴 자동 호출 -> 예) repo=https://github.com/acme/api …
    """
    try:
        pr_url = git_util.github_pr_url(github_url,
                                        head_branch,
                                        title,
                                        body,
                                        base_branch)
        return f"[PR 바로가기]({pr_url})"
    except Exception as e:
        return f"PR URL 생성 중 오류 : {str(e)}"
