from pathlib import Path
from utils.git_utils import GitUtils

def read_pr_template():
    git_util = GitUtils()
    root_path = git_util.get_root_path()
    template_paths =  Path(root_path, ".github/PULL_REQUEST_TEMPLATE.md")
    
    try:
        with open(template_paths, 'r', encoding='utf-8') as f:
            return f.read()  # 템플릿 반환 
    except FileNotFoundError:
        # 템플릿 파일이 없는 경우
        return "PR 템플릿 파일을 찾을 수 없습니다. .github/pull_request_template.md 파일을 생성해주세요."