import subprocess
import urllib.parse
import re
import webbrowser
from datetime import datetime

def complete_pr_test():
    """완전한 PR 생성 테스트 (커밋 → 푸시 → URL 생성 → 브라우저 열기)"""
    
    print("🧪 완전한 PR 생성 테스트 시작...\n")
    print("=" * 60)
    
    # 1. Git 상태 확인
    print("1️⃣ Git 상태 확인")
    git_status = check_git_status()
    print(f"   {git_status}")
    
    # 2. GitHub 저장소 정보 확인
    print("\n2️⃣ GitHub 저장소 정보 확인")
    owner, repo = get_github_repo_info()
    if owner and repo:
        print(f"   ✅ Owner: {owner}")
        print(f"   ✅ Repo: {repo}")
    else:
        print("   ❌ GitHub 저장소 정보를 찾을 수 없습니다.")
        return
    
    # 3. 현재 브랜치 확인
    print("\n3️⃣ 현재 브랜치 확인")
    current_branch = get_current_branch()
    if current_branch:
        print(f"   ✅ 현재 브랜치: {current_branch}")
    else:
        print("   ❌ 브랜치 정보를 찾을 수 없습니다.")
        return
    
    # 4. 테스트 파일 생성 (변경사항 만들기)
    print("\n4️⃣ 테스트 변경사항 생성")
    test_file_created = create_test_changes()
    print(f"   {test_file_created}")
    
    # 5. 커밋 실행
    print("\n5️⃣ Git 커밋 실행")
    commit_result = perform_commit()
    print(f"   {commit_result}")
    
    # 6. 푸시 실행 (핵심!)
    print("\n6️⃣ Git 푸시 실행")
    push_result = perform_push(current_branch)
    print(f"   {push_result}")
    
    if "실패" in push_result:
        print("   ⚠️ 푸시 실패로 테스트 중단")
        return
    
    # 7. PR URL 생성
    print("\n7️⃣ GitHub PR URL 생성")
    test_pr_data = {
        "title": f"test: PR 테스트 ({datetime.now().strftime('%H:%M:%S')})",
        "body": f"""## 🧪 테스트 PR

**생성 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**브랜치**: {current_branch}
**목적**: PR 생성 테스트

## 변경사항
- 테스트 파일 추가
- PR URL 생성 테스트

## 체크리스트
- [x] 커밋 완료
- [x] 푸시 완료
- [x] URL 생성 완료"""
    }
    
    pr_url = create_github_pr_url(
        owner, repo, current_branch, 
        test_pr_data["title"], test_pr_data["body"]
    )
    
    print(f"   ✅ PR URL 생성 완료")
    print(f"   🔗 URL: {pr_url[:80]}...")
    
    # 8. URL 유효성 검증
    print("\n8️⃣ URL 유효성 검증")
    url_validation = validate_pr_url(pr_url)
    print(f"   {url_validation}")
    
    # 9. 브라우저 테스트
    print("\n9️⃣ 브라우저 열기 테스트")
    browser_test = test_browser_open(pr_url)
    print(f"   {browser_test}")
    
    # 10. 최종 결과
    print("\n" + "=" * 60)
    print("🎉 **테스트 완료!**")
    print(f"\n📋 **최종 결과**:")
    print(f"   🏠 저장소: {owner}/{repo}")
    print(f"   🌿 브랜치: {current_branch}")
    print(f"   📝 제목: {test_pr_data['title']}")
    print(f"   🔗 PR URL: {pr_url}")
    
    print(f"\n💡 **다음 단계**: GitHub에서 'Create pull request' 버튼이 활성화되어 있는지 확인하세요!")
    
    return pr_url

def check_git_status():
    """Git 상태 확인"""
    try:
        # Working directory 상태
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, check=True
        )
        
        # 브랜치 상태
        branch_status = subprocess.run(
            ["git", "status", "-b", "--porcelain"],
            capture_output=True, text=True, check=True
        )
        
        status_lines = status_result.stdout.strip().split('\n') if status_result.stdout.strip() else []
        
        if status_lines and status_lines[0]:
            return f"✅ {len(status_lines)}개 파일에 변경사항 있음"
        else:
            return "📭 변경사항 없음 (테스트 파일 생성 예정)"
            
    except subprocess.CalledProcessError as e:
        return f"❌ Git 상태 확인 실패: {e}"

def create_test_changes():
    """테스트용 변경사항 생성"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        test_filename = f"pr_test_{timestamp}.md"
        
        test_content = f"""# PR 테스트 파일

**생성 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**파일명**: {test_filename}

## 목적
GitHub PR 생성 테스트를 위한 파일입니다.

## 테스트 내용
- Git 커밋 테스트
- Git 푸시 테스트  
- PR URL 생성 테스트
- 브라우저 열기 테스트

## 참고사항
이 파일은 테스트 후 삭제해도 됩니다.
"""
        
        with open(test_filename, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        return f"✅ 테스트 파일 생성: {test_filename}"
        
    except Exception as e:
        return f"❌ 테스트 파일 생성 실패: {e}"

def perform_commit():
    """Git 커밋 실행"""
    try:
        # git add
        subprocess.run(["git", "add", "."], check=True)
        
        # git commit
        commit_message = f"test: PR 생성 테스트 ({datetime.now().strftime('%H:%M:%S')})"
        result = subprocess.run([
            "git", "commit", "-m", commit_message
        ], capture_output=True, text=True, check=True)
        
        return f"✅ 커밋 완료: {commit_message}"
        
    except subprocess.CalledProcessError as e:
        # 이미 커밋할 것이 없는 경우
        if "nothing to commit" in e.stderr:
            return "⚠️ 커밋할 변경사항 없음 (이미 커밋됨)"
        else:
            return f"❌ 커밋 실패: {e.stderr}"

def perform_push(branch_name):
    """Git 푸시 실행"""
    try:
        result = subprocess.run([
            "git", "push", "origin", branch_name
        ], capture_output=True, text=True, check=True)
        
        return f"✅ 푸시 완료: origin/{branch_name}"
        
    except subprocess.CalledProcessError as e:
        return f"❌ 푸시 실패: {e.stderr}"

def get_github_repo_info():
    """GitHub 저장소 정보 추출"""
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True, text=True, check=True
        )
        remote_url = result.stdout.strip()
        
        # GitHub URL 파싱
        patterns = [
            r'git@github\.com:([^/]+)/([^/.]+)(?:\.git)?',  # SSH
            r'https://github\.com/([^/]+)/([^/.]+)(?:\.git)?'  # HTTPS
        ]
        
        for pattern in patterns:
            match = re.search(pattern, remote_url)
            if match:
                return match.group(1), match.group(2)
        
        return None, None
        
    except subprocess.CalledProcessError:
        return None, None

def get_current_branch():
    """현재 브랜치 이름 가져오기"""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def create_github_pr_url(owner, repo, head_branch, title, body, base_branch="main"):
    """GitHub PR 생성 URL 만들기"""
    
    # URL 인코딩
    encoded_title = urllib.parse.quote(title)
    encoded_body = urllib.parse.quote(body)
    
    # GitHub PR 생성 URL 구성
    base_url = f"https://github.com/{owner}/{repo}/compare/{base_branch}...{head_branch}"
    
    # 쿼리 파라미터 추가
    params = [
        "quick_pull=1",
        f"title={encoded_title}",
        f"body={encoded_body}"
    ]
    
    return base_url + "?" + "&".join(params)

def validate_pr_url(url):
    """PR URL 유효성 검증"""
    try:
        from urllib.parse import urlparse, parse_qs
        
        parsed = urlparse(url)
        
        # GitHub 도메인 확인
        if parsed.netloc != "github.com":
            return "❌ GitHub 도메인이 아닙니다."
        
        # 경로 확인 (compare 포함)
        if "/compare/" not in parsed.path:
            return "❌ 올바른 compare URL이 아닙니다."
        
        # 쿼리 파라미터 확인
        query_params = parse_qs(parsed.query)
        
        required_params = ["quick_pull", "title", "body"]
        missing_params = [param for param in required_params if param not in query_params]
        
        if missing_params:
            return f"❌ 필수 파라미터 누락: {missing_params}"
        
        # URL 길이 체크
        if len(url) > 8192:  # 브라우저 URL 길이 제한
            return "⚠️ URL이 너무 깁니다. 일부 브라우저에서 문제가 될 수 있습니다."
        
        return "✅ URL 유효성 검증 통과"
        
    except Exception as e:
        return f"❌ URL 검증 실패: {e}"

def test_browser_open(url, actually_open=True):
    """브라우저 열기 테스트"""
    try:
        if actually_open:
            webbrowser.open(url)
            return "✅ 브라우저에서 PR 페이지가 열렸습니다!"
        else:
            # 실제로 열지 않고 가능 여부만 확인
            browser = webbrowser.get()
            return f"✅ 브라우저 사용 가능: {type(browser).__name__}"
            
    except Exception as e:
        return f"❌ 브라우저 열기 실패: {e}"

# 빠른 테스트 함수 (간단 버전)
def quick_test():
    """빠른 푸시 + URL 테스트"""
    
    print("⚡ 빠른 테스트 실행 중...")
    
    try:
        # 현재 정보 수집
        branch = get_current_branch()
        owner, repo = get_github_repo_info()
        
        if not branch or not owner or not repo:
            print("❌ Git 정보 수집 실패")
            return
        
        print(f"📂 브랜치: {branch}")
        print(f"🏠 저장소: {owner}/{repo}")
        
        # 푸시 실행
        print("🚀 푸시 중...")
        push_result = subprocess.run([
            "git", "push", "origin", branch
        ], capture_output=True, text=True)
        
        if push_result.returncode == 0:
            print("✅ 푸시 완료")
        else:
            print(f"⚠️ 푸시 결과: {push_result.stderr}")
        
        # URL 생성
        pr_url = create_github_pr_url(
            owner, repo, branch,
            "test: 빠른 테스트",
            "빠른 테스트용 PR입니다."
        )
        
        print(f"🔗 PR URL: {pr_url}")
        
        # 브라우저 열기
        webbrowser.open(pr_url)
        print("🌐 브라우저 열림!")
        
    except Exception as e:
        print(f"❌ 빠른 테스트 실패: {e}")

# 실행 선택
if __name__ == "__main__":
    print("어떤 테스트를 실행하시겠습니까?")
    print("1. 완전한 테스트 (complete_pr_test)")
    print("2. 빠른 테스트 (quick_test)")
    
    choice = input("선택 (1 또는 2): ").strip()
    
    if choice == "1":
        complete_pr_test()
    elif choice == "2":
        quick_test()
    else:
        print("기본값으로 완전한 테스트를 실행합니다.")
        complete_pr_test()