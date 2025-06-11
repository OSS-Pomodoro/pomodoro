import streamlit as st
import streamlit.components.v1 as components
import time
import json
import os
import pandas as pd
from datetime import date, datetime

# ── 세션 상태 초기화 ──
def InitSessionState():
    if "todoData" not in st.session_state:
        st.session_state.todoData = {}
    if "inputKeySuffix" not in st.session_state:
        st.session_state.inputKeySuffix = {}
    if "pomodoroIndex" not in st.session_state:
        st.session_state.pomodoroIndex = 0
    if "timer_start" not in st.session_state:
        st.session_state.timer_start = None
    if "timer_duration" not in st.session_state:
        st.session_state.timer_duration = 0
    if "timer_mode" not in st.session_state:
        st.session_state.timer_mode = None
    if "pomodoroCounts" not in st.session_state:
        st.session_state.pomodoroCounts = {}

# ── To-Do 리스트 섹션 ──
def ShowTodoSection(selectedDate):
    st.subheader(f"📋 To-Do List for {selectedDate.strftime('%Y-%m-%d')}")
    todoKey = selectedDate.strftime("%Y-%m-%d")
    todos = st.session_state.todoData.get(todoKey, [])
    checkedKey = f"{todoKey}_checked"
    if checkedKey not in st.session_state:
        st.session_state[checkedKey] = [False] * len(todos)

    checkedStates = []
    for i, task in enumerate(todos):
        checked = st.checkbox(task, value=st.session_state[checkedKey][i], key=f"{todoKey}_task_{i}")
        checkedStates.append(checked)
    st.session_state[checkedKey] = checkedStates

    if todoKey not in st.session_state.inputKeySuffix:
        st.session_state.inputKeySuffix[todoKey] = 0
    newTask = st.text_input("Add new task", key=f"{todoKey}_new_task_input_{st.session_state.inputKeySuffix[todoKey]}")
    if st.button("➕ Add Task", key=f"{todoKey}_add_btn"):
        if newTask.strip():
            todos.append(newTask.strip())
            st.session_state.todoData[todoKey] = todos
            st.session_state[checkedKey].append(False)
            st.session_state.inputKeySuffix[todoKey] += 1
            SaveTheState()

    if st.button("🗑️ Delete Checked Tasks", key=f"{todoKey}_delete_btn"):
        newTodos, newChecks = [], []
        for task, chk in zip(todos, checkedStates):
            if not chk:
                newTodos.append(task)
                newChecks.append(False)
        st.session_state.todoData[todoKey] = newTodos
        st.session_state[checkedKey] = newChecks
        SaveTheState()

# ── 상태 저장/로드 ──
def SaveTheState():
    FILENAME = "todoData.json"
    out = {}
    for d, todos in st.session_state.todoData.items():
        ckey = f"{d}_checked"
        out[d] = {
            "tasks": todos,
            "checked": st.session_state.get(ckey, [False] * len(todos)),
            "pomodoroCount": st.session_state.pomodoroCounts.get(d, 0)
        }
    with open(FILENAME, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

def LoadTodoData():
    FILENAME = "todoData.json"
    if os.path.exists(FILENAME):
        data = json.load(open(FILENAME, 'r', encoding='utf-8'))
        st.session_state.todoData = {}
        st.session_state.pomodoroCounts = {}
        for d, v in data.items():
            st.session_state.todoData[d] = v.get('tasks', [])
            st.session_state[f"{d}_checked"] = v.get('checked', [False] * len(st.session_state.todoData[d]))
            st.session_state.pomodoroCounts[d] = v.get('pomodoroCount', 0)
    else:
        st.session_state.todoData = {}
        st.session_state.pomodoroCounts = {}

# ── 통계 그래프 ──
def ShowPomodoroStats():
    st.subheader("📊 Pomodoro Statistics")
    data = st.session_state.get('pomodoroCounts', {})
    if not data:
        st.info("아직 완료된 포모도로가 없습니다.")
        return

    df = pd.DataFrame(list(data.items()), columns=['Date', 'Count'])
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date').sort_index()

    st.markdown("### 일별")
    st.bar_chart(df['Count'])
    st.markdown("### 주별")
    st.bar_chart(df.resample('W-MON')['Count'].sum())
    st.markdown("### 월별")
    st.bar_chart(df.resample('M')['Count'].sum())
    st.markdown("### 연도별")
    st.bar_chart(df.resample('Y')['Count'].sum())

# ── 원형 타이머 CSS & 함수 ──
TIMER_CSS = """
<style>
.circle{
  width:240px;height:240px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;margin:auto;}
.circle span{font:700 2.2rem monospace;color:#fff}
</style>"""

def draw_circle(rem, total):
    pct = rem / total
    angle = pct * 360
    mm, ss = divmod(rem, 60)
    return TIMER_CSS + f"""
    <div class="circle"
         style="background:
            conic-gradient(#e74c3c 0deg {angle}deg,
                           #eeeeee {angle}deg 360deg);">
      <span>{mm:02d}:{ss:02d}</span>
    </div>
    """

# ── 메인 실행 함수 ──
def main():
    InitSessionState()
    LoadTodoData()

    st.title("📑 The Pomodoro App")
    st.sidebar.title("Settings")
    focus_min = st.sidebar.number_input("Focus Time (minutes)", 1, 60, 25)
    break_min = st.sidebar.number_input("Break Time (minutes)", 1, 30, 5)
    sel = st.sidebar.date_input("Select Date", value=date.today())
    sel_str = sel.strftime('%Y-%m-%d')
    st.session_state.pomodoroIndex = st.session_state.pomodoroCounts.get(sel_str, 0)

    if st.button("Start"):
        st.session_state.timer_mode = 'focus'
        st.session_state.timer_duration = focus_min * 60
        t0 = st.session_state.timer_duration
        box = st.empty()
        for t in range(t0, -1, -1):
            box.markdown(draw_circle(t, t0), unsafe_allow_html=True)
            time.sleep(1)
        st.toast("🔔 Focus complete! Time for a break.", icon="🍅")
        st.session_state.timer_mode = 'break'
        st.session_state.timer_start = datetime.now()
        st.session_state.timer_duration = break_min * 60
        st.rerun()

    elif st.session_state.timer_mode == 'break' and st.session_state.timer_start:
        elapsed = (datetime.now() - st.session_state.timer_start).total_seconds()
        rem = int(st.session_state.timer_duration - elapsed)
        if rem <= 0:
            st.toast("⏰ Break is over!", icon="⏰")
            st.session_state.pomodoroIndex += 1
            st.session_state.pomodoroCounts[sel_str] = st.session_state.pomodoroIndex
            SaveTheState()
            st.session_state.timer_mode = None
            st.session_state.timer_start = None
            st.rerun()
        else:
            components.html(draw_circle(rem, st.session_state.timer_duration), height=260, scrolling=False)
            col1, col2 = st.columns(2)
            with col1:
                ShowTodoSection(sel)
            with col2:
                ShowPomodoroStats()
            time.sleep(1)
            st.rerun()
    else:
        col1, col2 = st.columns(2)
        with col1:
            ShowTodoSection(sel)
        with col2:
            ShowPomodoroStats()
