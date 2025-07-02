from mcp.server.fastmcp import FastMCP
import json

mcp = FastMCP("github-pr-mcp")

@mcp.tool()
async def create_template() -> str:
    """프로젝트의 PR 템플릿을 가져옵니다."""
    from .utils.template_utils import read_pr_template

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
    from .utils.git_utils import get_branch_changes

    try:
        changes = get_branch_changes()
        return json.dumps({"status": "success",
            "changes": changes})
    except Exception as e:
        return json.dumps({"status": "error",
            "message": str(e)})
    

@mcp.tool()
async def create_github_pr_url(title: str, body: str) -> str:
    """GitHub 프로젝트의 PR 생성 URL을 생성."""
    from .utils.git_utils import git_url_info, get_branch_name, github_pr_url, perform_push

    try:
        github_url = git_url_info()
        head_branch = get_branch_name()
        perform_push(head_branch) # 현재 브랜치를 원격 저장소에 푸시
        pr_url = github_pr_url(github_url, head_branch, title, body)
        return json.dumps({"status": "success",
            "pr_url": pr_url})
    except Exception as e:
        return json.dumps({"status": "error",
            "message": str(e)})
    