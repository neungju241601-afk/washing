# 📤 GitHub에 올리는 방법 (초등학생도 이해할 수 있는 설명)

## 🎯 이 가이드가 필요한 이유
이 프로젝트를 다른 사람들과 공유하거나, 나중에 다시 사용하려면 GitHub에 올려야 합니다.
GitHub는 코드를 저장하는 무료 저장소입니다. (네이버 클라우드나 구글 드라이브 같은 곳이라고 생각하면 됩니다!)

---

## 📝 준비물
1. **GitHub 계정** (없으면 만들어야 해요!)
   - https://github.com 에서 무료로 만들 수 있습니다
   
2. **Git 프로그램** (컴퓨터에 설치해야 해요!)
   - https://git-scm.com/downloads 에서 다운로드
   - Windows면 "Download for Windows" 클릭
   - 설치할 때는 "Next" 버튼만 계속 누르면 됩니다!

---

## 🚀 단계별 업로드 방법

### 1단계: GitHub에서 새 저장소 만들기

1. **GitHub 웹사이트 접속**
   - https://github.com 에 로그인

2. **새 저장소 만들기**
   - 오른쪽 위에 있는 **"+"** 버튼 클릭
   - **"New repository"** 클릭

3. **저장소 정보 입력**
   - **Repository name**: `washing-machine-reservation` (원하는 이름으로 변경 가능)
   - **Description**: "기숙사 세탁기 예약 시스템" (설명)
   - **Public** 선택 (무료로 공개)
   - **"Create repository"** 버튼 클릭

4. **중요!** 저장소 주소 복사하기
   - 다음 페이지에서 나오는 주소를 복사해두세요
   - 예: `https://github.com/사용자이름/washing-machine-reservation.git`

---

### 2단계: 컴퓨터에서 Git 초기화하기

**Windows PowerShell이나 명령 프롬프트를 열어주세요!**

1. **프로젝트 폴더로 이동**
   ```bash
   cd C:\Users\user\OneDrive\Documents\WashM
   ```

2. **Git 초기화** (처음 한 번만!)
   ```bash
   git init
   ```
   → "Initialized empty Git repository" 라는 메시지가 나오면 성공!

3. **모든 파일 추가하기**
   ```bash
   git add .
   ```
   → 모든 파일이 준비되었다는 뜻입니다!

4. **첫 번째 저장 (커밋)**
   ```bash
   git commit -m "첫 번째 버전: 세탁기 예약 시스템 완성"
   ```
   → "X files changed" 라는 메시지가 나오면 성공!

---

### 3단계: GitHub에 업로드하기

1. **GitHub 저장소 연결**
   ```bash
   git remote add origin https://github.com/사용자이름/washing-machine-reservation.git
   ```
   ⚠️ **주의**: `사용자이름` 부분을 본인의 GitHub 사용자 이름으로 바꿔주세요!

2. **업로드하기**
   ```bash
   git branch -M main
   git push -u origin main
   ```
   → GitHub 사용자 이름과 비밀번호를 물어볼 수 있습니다
   → 비밀번호 대신 **Personal Access Token**을 사용해야 할 수도 있어요!

---

## 🔑 Personal Access Token 만들기 (비밀번호 대신 사용)

GitHub에서 비밀번호 대신 토큰을 사용해야 합니다:

1. **GitHub 웹사이트 접속**
   - 오른쪽 위 프로필 사진 클릭
   - **Settings** 클릭

2. **토큰 만들기**
   - 왼쪽 메뉴에서 **Developer settings** 클릭
   - **Personal access tokens** → **Tokens (classic)** 클릭
   - **Generate new token** → **Generate new token (classic)** 클릭

3. **토큰 설정**
   - **Note**: "세탁기 프로젝트" (아무 이름이나)
   - **Expiration**: 90 days (원하는 기간)
   - **Select scopes**: `repo` 체크박스 선택
   - **Generate token** 클릭

4. **토큰 복사하기**
   - ⚠️ **중요**: 이 토큰은 한 번만 보여줍니다! 복사해서 안전한 곳에 저장하세요!

5. **업로드할 때 사용**
   - 비밀번호를 물어볼 때 이 토큰을 입력하세요!

---

## ✅ 업로드 확인하기

1. **GitHub 웹사이트에서 확인**
   - https://github.com/사용자이름/washing-machine-reservation 접속
   - 파일들이 보이면 성공! 🎉

2. **나중에 수정사항 업로드하기**
   ```bash
   git add .
   git commit -m "수정 내용 설명"
   git push
   ```

---

## 🆘 문제 해결

### "git이 인식되지 않습니다" 오류
→ Git이 설치되지 않았습니다. 1단계로 돌아가서 Git을 설치하세요!

### "remote origin already exists" 오류
→ 이미 연결되어 있습니다. 다음 명령어로 다시 연결:
```bash
git remote remove origin
git remote add origin https://github.com/사용자이름/washing-machine-reservation.git
```

### "Authentication failed" 오류
→ Personal Access Token을 사용해야 합니다. 위의 토큰 만들기 섹션을 참고하세요!

---

## 📚 더 배우고 싶다면

- **Git 기초**: https://git-scm.com/book/ko/v2
- **GitHub 가이드**: https://guides.github.com

---

## 💡 팁

- **README.md** 파일이 있으면 GitHub에서 자동으로 보여줍니다!
- **.gitignore** 파일로 불필요한 파일은 업로드하지 않습니다
- 프로젝트 설명을 잘 쓰면 다른 사람들이 이해하기 쉬워요!

---

**화이팅! GitHub에 성공적으로 업로드하세요! 🚀**

