from mcp.server.fastmcp import FastMCP
from utils.git_utils import GitUtils
from typing import Annotated
from pydantic import Field
import json
import os

mcp = FastMCP("github-pr-mcp")
git_util = GitUtils()


@mcp.tool()
async def test_root_path() -> str:
    """프로젝트 루트 경로 테스트"""
    try:
        root_path = os.getcwd()
        return json.dumps({"status": "success",
                           "root_path": root_path})
    except Exception as e:
        return json.dumps({"status": "error",
                           "message": str(e)})


@mcp.tool()
async def create_template() -> str:
    """프로젝트의 PR 템플릿을 가져옵니다."""
    from utils.template_utils import read_pr_template

    try:
        template = read_pr_template()
        return json.dumps({"status": "success",
                           "template": template})
    except Exception as e:
        return json.dumps({"status": "error",
                           "message": str(e)})


@mcp.tool()
async def create_change_git() -> str:
    """현재 브랜치의 코드 변경사항을 가져옵니다."""

    try:
        changes = git_util.get_branch_changes()
        return json.dumps({"status": "success",
                           "changes": changes})
    except Exception as e:
        return json.dumps({"status": "error",
                           "message": str(e)})


@mcp.tool()
async def get_branch_name() -> str:
    """현재 브랜치 이름을 가져옵니다."""
    try:
        branch_name = git_util.get_branch_name()
        return json.dumps({"status": "success",
                           "branch_name": branch_name})
    except Exception as e:
        return json.dumps({"status": "error",
                           "message": str(e)})


@mcp.tool(description="GitHub PR URL 생성")
async def create_github_pr_url( 
    github_url: Annotated[str, Field(
        description="https://github.com/<owner>/<repo> 형식",
        pattern=r"^https://github\.com/.+/.+$"
    )],
    head_branch: Annotated[str, Field(description="머지 대상 브랜치")],
    title: Annotated[str, Field(description="PR 제목")],
    body: Annotated[str, Field(description="PR 본문")],
    base_branch: Annotated[str, Field(description="기준 브랜치")] = "main",
) -> str:

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
