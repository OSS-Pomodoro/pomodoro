import streamlit as st
import streamlit.components.v1 as components
import time
import pomodoro_feature2 
import pomodoro_feature1 as f1
from datetime import date, datetime
import base64

TIMER_CSS = """
<style>
.circle{
  width:240px;height:240px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;margin:auto;}
.circle span{font:700 2.2rem monospace;color:#fff}
</style>"""

def draw_circle(remaining, total):
    pct = remaining / total                 
    angle = pct * 360                       
    mm, ss = divmod(remaining, 60)
    timer = f"{mm:02d}:{ss:02d}"

    html = TIMER_CSS+f"""
    <div class="circle"
         style="background:
            conic-gradient(#e74c3c 0deg {angle}deg,
                           #eeeeee {angle}deg 360deg);">
      <span>{mm:02d}:{ss:02d}</span>
    </div>"""
    return html

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def image_to_base64(path):
    ext = path.split('.')[-1].lower()
    mime = {
        'jpg': 'jpeg',
        'jpeg': 'jpeg',
        'png': 'png',
        'gif': 'gif'
    }.get(ext, 'jpeg')
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return mime, encoded

local_css("style.css")

#---------------------------------#
st.write("""
# The Pomodoro App

Let's do some focus work in data science with this app.

Developed by: [Data Professor](http://youtube.com/dataprofessor)
Modified by: Donghyeon Ko
""")

# Timer 설정
st.sidebar.title("Settings")
focus_min = st.sidebar.number_input("Focus Time (minutes)", 1, 60, 25)
break_min = st.sidebar.number_input("Break Time (minutes)", 1, 30, 5)
selectedDate = st.sidebar.date_input("\U0001F4C5 Select Date", value=date.today())
selectedDateStr = selectedDate.strftime("%Y-%m-%d")

# 세션 상태 초기화 및 로딩
pomodoro_feature2.InitSessionState()
pomodoro_feature2.LoadTodoData()

if 'pomodoroCounts' not in st.session_state:
    st.session_state.pomodoroCounts = {}

if selectedDateStr not in st.session_state.pomodoroCounts:
    st.session_state.pomodoroCounts[selectedDateStr] = 0

st.session_state.pomodoroIndex = st.session_state.pomodoroCounts[selectedDateStr]

# 전체 종료 버튼
st.sidebar.markdown("---")
if st.sidebar.button("\U0001F6D1 전체 종료"):
    st.session_state.show_final_feedback = True
    st.session_state.timer_mode = None
    st.session_state.timer_start = None
    st.rerun()

button_clicked = st.button("Start")
st.subheader(f"현재 {st.session_state.pomodoroIndex}포모도로 진행 중입니다.")

# Focus 시작
if button_clicked:
    st.session_state.timer_mode = "focus"
    st.session_state.timer_duration = int(focus_min * 60)
    st.session_state.show_motivation = True
    t1 = st.session_state.timer_duration
    container = st.empty()

    for t in range(t1, -1, -1):
        with container:
            components.html(draw_circle(t, t1), height=260, scrolling=False)
        time.sleep(1)

    st.toast("\U0001F345 Focus complete! Time for a break.", icon="\U0001F345")

    # ✅ 포모도로 카운트 증가
    st.session_state.pomodoroCounts[selectedDateStr] += 1
    st.session_state.pomodoroIndex = st.session_state.pomodoroCounts[selectedDateStr]
    pomodoro_feature2.SaveTheState()

    st.session_state.timer_mode = "break"
    st.session_state.timer_duration = int(break_min * 60)
    st.session_state.timer_start = datetime.now()
    st.rerun()

# Break 타이머
elif st.session_state.timer_mode == "break" and st.session_state.timer_start:
    elapsed = (datetime.now() - st.session_state.timer_start).total_seconds()
    remaining = int(st.session_state.timer_duration - elapsed)

    if remaining <= 0:
        st.toast("⏰ Break is over!", icon="⏰")
        st.session_state.timer_mode = None
        st.session_state.timer_start = None
        pomodoro_feature2.SaveTheState()
        st.rerun()
    else:
        components.html(draw_circle(remaining, st.session_state.timer_duration), height=260)
        pomodoro_feature2.ShowTodoSection(selectedDate)
        time.sleep(1)
        st.rerun()

# 종료 후 
else:
    pomodoro_feature2.ShowTodoSection(selectedDate)

    st.markdown("### 💬 지금 당신에게 필요한 한 마디")
    st.info(f1.get_quote_by_level_today())

    if st.session_state.get("show_final_feedback", False):
        feedback_text = f1.get_feedback_after_pomodoro()

        if feedback_text == "🏆 오늘 완벽하게 해냈어요! 대단해요!":
            audio = "/mnt/data/Small Crowd Applause.mp3"
            mime, image = image_to_base64("great.jpg")
        elif feedback_text == "✅ 성실히 임하고 있어요. 이대로만 가도 좋아요!":
            audio = "/mnt/data/Small Crowd Applause.mp3"
            mime, image = image_to_base64("good.jpg")
        elif feedback_text == "✅ 방향은 잡았어요. 내일은 한 걸음만 더 내디뎌봐요!":
            audio = "/mnt/data/Strong Punch.mp3"
            mime, image = image_to_base64("momface.jpg")
        elif feedback_text == "언제까지 그렇게 살래?!!?!!":
            audio = "/mnt/data/Strong Punch.mp3"
            mime, image = image_to_base64("mom.gif")
        else:
            audio = ""
            mime = "jpeg"
            image = ""

        st.markdown(
            f"""
            <script>
                document.addEventListener('click', function() {{
                    window.location.search = '?reload=true';
                }});
            </script>
            <div style='position:fixed; top:0; left:0; width:100%; height:100%; background-color:#f0f8ff;
                 display:flex; flex-direction:column; align-items:center; justify-content:center; z-index:9999; cursor: pointer;'>
                <div style='font-size: 48px; font-weight: bold; text-align: center; margin-bottom: 20px;'>
                    ✅ 오늘의 피드백<br><br>{feedback_text}
                </div>
                <img src="data:image/{mime};base64,{image}" width="300">
            </div>
            """,
            unsafe_allow_html=True
        )

        if audio:
            st.audio(f"/mnt/data/{audio}", format="audio/mp3", start_time=0)

        if st.button("👉 계속하기", key="continue_button"):
            st.session_state.show_final_feedback = False
            st.rerun()

        st.stop()

# reload 파라미터 감지 → 원래 화면으로 복귀
if st.query_params.get("reload") == "true":
    st.session_state.show_final_feedback = False
    st.experimental_set_query_params()
    st.rerun()

if not st.session_state.get("show_final_feedback", False):
    st.markdown("### 📊 최근 통계 기반 격려")
    st.warning(f1.get_quote_by_recent_completion_rate())
