# ⚡ 빠른 시작 가이드

## 🎯 GitHub에서 바로 실행하기

### 방법 1: Codespaces 사용 (가장 쉬움!)

1. **저장소 페이지에서 "Code" 버튼 클릭**
   - https://github.com/neungju241601-afk/washing

2. **"Codespaces" 탭 선택**

3. **"Create codespace on main" 클릭**

4. **자동 설정 대기**
   - 패키지가 자동으로 설치됩니다
   - 데이터베이스가 자동으로 초기화됩니다

5. **터미널에서 실행**
   ```bash
   python app.py
   ```

6. **접속**
   - 포트 5000이 자동으로 포워딩됩니다
   - "Ports" 탭에서 공개 URL 확인
   - 또는 알림에서 "Open in Browser" 클릭

### 방법 2: 직접 링크 사용

**아래 링크를 클릭하면 바로 Codespace가 생성됩니다:**

👉 [GitHub Codespaces에서 바로 실행하기](https://codespaces.new/neungju241601-afk/washing)

---

## 💻 로컬에서 실행하기

### Windows

1. **저장소 클론**
   ```bash
   git clone https://github.com/neungju241601-afk/washing.git
   cd washing
   ```

2. **실행**
   ```bash
   start.bat
   ```
   또는
   ```bash
   pip install -r requirements.txt
   python app.py
   ```

### macOS/Linux

1. **저장소 클론**
   ```bash
   git clone https://github.com/neungju241601-afk/washing.git
   cd washing
   ```

2. **실행 권한 부여**
   ```bash
   chmod +x start.sh
   ```

3. **실행**
   ```bash
   ./start.sh
   ```
   또는
   ```bash
   pip install -r requirements.txt
   python app.py
   ```

---

## 🌐 공개 URL 만들기 (배포)

### Render 사용 (추천)

1. **Render 웹사이트 접속**
   - https://render.com

2. **"New +" → "Web Service" 클릭**

3. **GitHub 저장소 연결**
   - `neungju241601-afk/washing` 선택

4. **설정**
   - Name: `washing-machine`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

5. **배포 완료!**
   - 주소: `https://washing-machine.onrender.com`

---

## ❓ 문제 해결

### Codespaces가 느려요
- 첫 실행 시 약간의 시간이 걸릴 수 있습니다
- 잠시 기다려주세요

### 포트가 열리지 않아요
- Codespaces에서 포트 5000이 자동으로 포워딩됩니다
- "Ports" 탭에서 확인하세요

### 패키지 설치 오류
- 터미널에서 직접 실행:
  ```bash
  pip install -r requirements.txt
  ```

---

## 🎉 성공!

이제 어디서든 접속해서 사용할 수 있습니다!

