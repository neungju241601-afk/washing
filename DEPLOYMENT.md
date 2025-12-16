# 🚀 무료 호스팅 배포 가이드

이 프로젝트를 무료로 인터넷에 올려서 누구나 사용할 수 있게 만드는 방법입니다!

## 🎯 왜 호스팅이 필요한가요?

- 지금은 `localhost:5000`으로만 접속 가능 (본인 컴퓨터에서만)
- 호스팅하면 **어디서든 인터넷으로 접속 가능**해요!
- 친구들, 선생님, 다른 사람들도 사용할 수 있어요!

---

## 🌟 추천 무료 호스팅 서비스

### 1. Render (가장 추천! ⭐) - 5분 안에 배포!

**현재 저장소**: https://github.com/neungju241601-afk/washing

**자세한 배포 가이드**: [`배포_자동화_가이드.md`](배포_자동화_가이드.md) 파일을 참고하세요!

**왜 좋은가요?**
- 완전 무료!
- 사용하기 쉬워요
- GitHub와 자동 연결

**배포 방법:**

1. **GitHub에 프로젝트 업로드**
   - `GITHUB_업로드_가이드.md` 참고

2. **Render 웹사이트 접속**
   - https://render.com 접속
   - "Get Started for Free" 클릭
   - GitHub 계정으로 로그인

3. **새 웹 서비스 만들기**
   - "New +" 버튼 클릭
   - "Web Service" 선택

4. **GitHub 저장소 연결**
   - "Connect account" 클릭
   - GitHub 저장소 선택
   - "Connect" 클릭

5. **설정 입력**
   - **Name**: `washing-machine` (원하는 이름)
   - **Region**: `Singapore` (한국과 가까운 곳)
   - **Branch**: `main`
   - **Root Directory**: (비워두기)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

6. **환경 변수 설정** (선택사항)
   - "Advanced" 클릭
   - "Add Environment Variable" 클릭
   - Key: `FLASK_DEBUG`, Value: `False`
   - Key: `PORT`, Value: (비워두기 - 자동 설정됨)

7. **배포 시작!**
   - "Create Web Service" 클릭
   - 2-3분 기다리기
   - "Your service is live!" 메시지가 나오면 성공! 🎉

8. **접속하기**
   - 주소가 나와요: `https://washing-machine.onrender.com`
   - 이 주소를 누구에게나 공유할 수 있어요!

---

### 2. Railway

**배포 방법:**

1. **Railway 웹사이트 접속**
   - https://railway.app 접속
   - GitHub로 로그인

2. **새 프로젝트 만들기**
   - "New Project" 클릭
   - "Deploy from GitHub repo" 선택
   - 저장소 선택

3. **자동 배포!**
   - Railway가 자동으로 감지해서 배포해요
   - 주소가 생성되면 끝!

---

### 3. Fly.io

**배포 방법:**

1. **Fly.io 설치**
   ```bash
   # Windows (PowerShell)
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **로그인**
   ```bash
   fly auth login
   ```

3. **배포**
   ```bash
   fly launch
   ```
   - 질문에 답하면 자동으로 배포돼요!

---

## ⚙️ 배포 전 확인사항

### 1. Procfile 확인
`Procfile` 파일이 있어야 해요:
```
web: python app.py
```

### 2. requirements.txt 확인
필요한 패키지가 모두 있어야 해요:
```
Flask==3.0.0
Werkzeug==3.0.1
```

### 3. 포트 설정 확인
`app.py`에서 포트를 환경 변수로 받도록 되어 있어요:
```python
port = int(os.environ.get('PORT', 5000))
```

---

## 🔧 배포 후 설정

### 데이터베이스
- SQLite 파일은 호스팅 서버에 저장돼요
- 서버가 재시작되면 일부 플랫폼에서는 데이터가 사라질 수 있어요
- 영구 저장이 필요하면 외부 스토리지 사용 고려

### 도메인 이름 (선택사항)
- Render: `프로젝트이름.onrender.com` (무료)
- Railway: `프로젝트이름.up.railway.app` (무료)
- 커스텀 도메인도 연결 가능 (유료)

---

## 📊 무료 플랜 비교

| 서비스 | 무료 제공 | 제한사항 |
|--------|----------|---------|
| **Render** | 무제한 | 15분 비활성 시 슬리프 모드 |
| **Railway** | $5 크레딧/월 | 크레딧 소진 시 중지 |
| **Fly.io** | 3개 앱 | 제한적 리소스 |

**추천**: Render (가장 쉬움!)

---

## 🆘 문제 해결

### "Build failed" 오류
- `requirements.txt` 확인
- Python 버전 확인 (`runtime.txt`)

### "Application error" 오류
- 로그 확인 (호스팅 서비스의 "Logs" 탭)
- `app.py`의 포트 설정 확인

### 데이터가 사라져요
- 일부 플랫폼은 파일 시스템이 임시적이에요
- 외부 데이터베이스 사용 고려 (SQLite 대신)

---

## 🎉 성공!

배포가 완료되면:
1. 주소를 친구들에게 공유하세요!
2. 어디서든 접속해서 사용할 수 있어요!
3. 프로젝트를 자랑하세요! 🚀

---

**화이팅! 성공적인 배포를 기원합니다!** ✨

