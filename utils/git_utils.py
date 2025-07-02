import subprocess
from pathlib import Path

def get_root_path():
    """ 현재 프로젝트 루트 경로 반환 """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
            # cwd 지정하지 않으면 MCP 서버 실행 위치에서 시작
        )
        git_root = Path(result.stdout.strip())
        print(f"Git 루트 발견: {git_root}")
        return git_root
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git 저장소가 아님: {e}")


def get_branch_changes():
    """현재 브랜치의 변경사항을 가져오는 함수"""
    try:
        # 현재 브랜치명
        current_branch = subprocess.check_output(
            ['git', 'branch', '--show-current'], 
            text=True
        ).strip()
        
        # 변경된 파일 목록
        changed_files = subprocess.check_output(
            ['git', 'diff', '--name-only', 'HEAD'], 
            text=True
        ).strip().split('\n')
        
        # 스테이징된 파일들
        staged_files = subprocess.check_output(
            ['git', 'diff', '--name-only', '--staged'], 
            text=True
        ).strip().split('\n')
        
        # main과의 차이점
        commits_ahead = subprocess.check_output(
            ['git', 'rev-list', '--count', 'main..HEAD'], 
            text=True
        ).strip()
        
        return {
            'current_branch': current_branch,
            'changed_files': [f for f in changed_files if f],
            'staged_files': [f for f in staged_files if f],
            'commits_ahead': commits_ahead
        }
        
    except subprocess.CalledProcessError as e:
        return f"Git 명령어 실행 오류: {e}"