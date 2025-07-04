import subprocess
from pathlib import Path
import urllib.parse
import os


class GitUtils:
    def __init__(self):
        self.git_root = os.getcwd()

    def get_root_path(self):
        """ 현재 프로젝트 루트 경로 반환 """

        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=True,
                cwd=self.git_root
            )
            git_root = Path(result.stdout.strip())
            print(f"Git 루트 발견: {git_root}")
            return git_root
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Git 저장소가 아님: {e}")
            return None

    def get_branch_changes(self):
        """현재 브랜치의 변경사항을 가져오는 함수"""
        try:
            # 현재 브랜치명
            current_branch = subprocess.check_output(
                ['git', 'branch', '--show-current'],
                text=True,
                cwd=self.git_root
            ).strip()

            # 변경된 파일 목록
            changed_files = subprocess.check_output(
                ['git', 'diff', '--name-only', 'HEAD'],
                text=True,
                cwd=self.git_root
            ).strip().split('\n')

            # 스테이징된 파일들
            staged_files = subprocess.check_output(
                ['git', 'diff', '--name-only', '--staged'],
                text=True,
                cwd=self.git_root
            ).strip().split('\n')

            # main과의 차이점
            commits_ahead = subprocess.check_output(
                ['git', 'rev-list', '--count', 'main..HEAD'],
                text=True,
                cwd=self.git_root
            ).strip()

            return {
                'current_branch': current_branch,
                'changed_files': [f for f in changed_files if f],
                'staged_files': [f for f in staged_files if f],
                'commits_ahead': commits_ahead
            }

        except subprocess.CalledProcessError as e:
            return f"Git 명령어 실행 오류: {e}"

    def perform_push(self, branch_name):
        """Git 푸시 실행"""
        try:
            result = subprocess.run([
                "git", "push", "origin", branch_name
            ], capture_output=True, text=True, check=True, cwd=self.git_root)

            return f"푸시 완료: origin/{branch_name}"

        except subprocess.CalledProcessError as e:
            return f"Git 푸시 실패: {e.stderr}"

    def git_url_info(self):
        """현재 저장소 주소 반환"""

        try:
            result = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                capture_output=True, text=True, check=True,
                cwd=self.git_root
            )
            remote_url = result.stdout.strip().replace('.git', '')

            return remote_url
        except subprocess.CalledProcessError as e:
            return f"Git 브랜치 이름 조회 실패: {e.stderr}"

    def get_branch_name(self):
        """현재 브랜치 이름 가져오기"""

        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True, text=True, check=True,
                cwd=self.git_root
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Git 브랜치 이름 조회 실패: {e.stderr}"

    def github_pr_url(self, github_url, head_branch, title, body, base_branch="main"):
        """GitHub PR 생성 URL 만들기"""

        # URL 인코딩
        encoded_title = urllib.parse.quote(title)
        encoded_body = urllib.parse.quote(body)

        base_url = f"{github_url}/compare/{base_branch}...{head_branch}"
        pr_url = f"{base_url}?quick_pull=1&title={encoded_title}&body={encoded_body}"

        return pr_url
