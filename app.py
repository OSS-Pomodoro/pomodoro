import streamlit as st
import streamlit.components.v1 as components
import time
import pomodoro_feature2
from datetime import date, datetime

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

local_css("style.css")

#---------------------------------#
st.write("""
# The Pomodoro App

Let's do some focus work in data science with this app.

Developed by: [Data Professor](http://youtube.com/dataprofessor)
Modified by: Donghyeon Ko


""")


# Timer
st.sidebar.title("Settings")
focus_min = st.sidebar.number_input("Focus Time (minutes)", 1, 60, 25)
break_min = st.sidebar.number_input("Break Time (minutes)", 1, 30, 5)
selectedDate = st.sidebar.date_input("📅 Select Date", value=date.today())

pomodoro_feature2.InitSessionState()
pomodoro_feature2.LoadTodoData()

selectedDateStr = selectedDate.strftime("%Y-%m-%d")

if 'pomodoroCounts' in st.session_state and selectedDateStr in st.session_state.pomodoroCounts:
    st.session_state.pomodoroIndex = st.session_state.pomodoroCounts[selectedDateStr]
else:
    st.session_state.pomodoroIndex = 0


button_clicked = st.button("Start")

st.subheader(f"현재 {st.session_state.pomodoroIndex}포모도로 진행 중입니다.")


if button_clicked:
    st.session_state.timer_mode = "focus"
    st.session_state.timer_duration = int(focus_min * 60)
    t1 = st.session_state.timer_duration
    container=st.empty()

    for t in range(t1, -1,-1):
        with container:
            components.html(draw_circle(t, t1), height=260, scrolling=False)
        time.sleep(1)

    st.toast("🔔 Focus complete! Time for a break.", icon="🍅")
    st.session_state.timer_mode = "break" # break time으로 전환
    st.session_state.timer_duration = int(break_min * 60)
    st.session_state.timer_start = datetime.now()
    st.rerun()  # break 모드로 즉시 진입

# break 타이머 로직
elif st.session_state.timer_mode == "break" and st.session_state.timer_start:
    elapsed = (datetime.now() - st.session_state.timer_start).total_seconds()
    remaining = int(st.session_state.timer_duration - elapsed)

    if remaining <= 0:
        st.toast("⏰ Break is over!", icon="⏰")
        st.session_state.pomodoroIndex += 1
        st.session_state.timer_mode = None
        st.session_state.timer_start = None
        st.session_state.pomodoroCounts[selectedDateStr] = st.session_state.pomodoroIndex
        pomodoro_feature2.SaveTheState()
        st.rerun()
    else:
        components.html(draw_circle(remaining, st.session_state.timer_duration), height=260)
        # break 중에는 다른 기능 사용 가능
        pomodoro_feature2.ShowTodoSection(selectedDate)
        # rerun을 통해 1초마다 갱신
        time.sleep(1)
        st.rerun()
else:
    pomodoro_feature2.ShowTodoSection(selectedDate)