import streamlit as st
import streamlit.components.v1 as components
import time
import pomodoro_feature2
from datetime import date

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

button_clicked = st.button("Start")

t1 = focus_min * 60
t2 = break_min * 60

pomodoro_feature2.InitSessionState()
st.subheader(f"현재 {st.session_state.pomodoroIndex}포모도로 진행 중입니다.")

if button_clicked:
    container=st.empty()
    for t in range(t1, -1,-1):
        with container:
            components.html(draw_circle(t, t1), height=260, scrolling=False)
        time.sleep(1)
    st.toast("🔔 Focus complete! Time for a break.", icon="🍅")

    for t in range(t2, -1, -1):
        with container:
            components.html(draw_circle(t, t2), height=260, scrolling=False)
        time.sleep(1)
    st.toast("⏰ Break is over!", icon="⏰")
    st.session_state.pomodoroIndex += 1

pomodoro_feature2.ShowTodoSection(selectedDate)