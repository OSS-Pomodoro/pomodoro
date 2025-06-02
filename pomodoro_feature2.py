# 테스트용

import streamlit as st
from datetime import date
import json
import os

#세션 상태 초기화하는 함수
def InitSessionState():
    # 날짜별 Todo 저장용 세션 상태 초기화
    if "todoData" not in st.session_state:
        st.session_state.todoData = {}

    if "inputKeySuffix" not in st.session_state:
        '''
        날짜별 새로운 입력 위젯 키를 관리할 상태 초기화
        위젯에 목표를 적고 add하면 위젯 안에 작성한 단어는 초기화 됨 =>
        일일이 지우고 작성할 필요가 없게 하기 위함. 
        '''
        st.session_state.inputKeySuffix = {}
    
    # 포모도로 카운트 저장용 세션 상태 초기화화
    if "pomodoroIndex" not in st.session_state:
        st.session_state.pomodoroIndex = 0

    if "timer_start" not in st.session_state:
        st.session_state.timer_start = None

    if "timer_duration" not in st.session_state:
        st.session_state.timer_duration = 0

    if "timer_mode" not in st.session_state:
        st.session_state.timer_mode = None

    # 날짜별 포모도로 카운트들을 담는 딕셔너리
    if 'pomodoroCounts' not in st.session_state:
        st.session_state.pomodoroCounts = {}

            
def ShowTodoSection(selectedDate):
    st.subheader(f"📋 To-Do List for {selectedDate.strftime('%Y-%m-%d')}")

    todoKey = selectedDate.strftime("%Y-%m-%d")
    # 해당 날짜를 불러오면 todo list를 가져옴
    todos = st.session_state.todoData.get(todoKey, [])

    # 체크 상태 저장용 key
    checkedKey = f"{todoKey}_checked"

    if checkedKey not in st.session_state:
        st.session_state[checkedKey] = [False] * len(todos)

    # 체크박스 출력 및 상태 추적
    checkedStates = []
    for index, task in enumerate(todos):
        checked = st.checkbox(task, value=st.session_state[checkedKey][index], key=f"{todoKey}_task_{index}")
        checkedStates.append(checked)

    st.session_state[checkedKey] = checkedStates

    # 새로운 입력 키 suffix 없으면 초기화
    if todoKey not in st.session_state.inputKeySuffix:
        st.session_state.inputKeySuffix[todoKey] = 0

    # 새 할 일 입력 (키를 suffix와 함께 줘서 입력 초기화 효과 냄)
    newTaskKey = f"{todoKey}_new_task_input_{st.session_state.inputKeySuffix[todoKey]}"
    newTask = st.text_input("Add new task", key=newTaskKey)

    if st.button("➕ Add Task", key=f"{todoKey}_add_btn"):
        if newTask.strip():
            todos.append(newTask.strip())
            st.session_state.todoData[todoKey] = todos
            st.session_state[checkedKey].append(False)
            st.session_state.inputKeySuffix[todoKey] += 1 # 입력창 초기화
            SaveTheState()

    # 체크된 항목 삭제
    if st.button("🗑️ Delete Checked Tasks", key=f"{todoKey}_delete_btn"):
        newTodos = []
        newChecked = []
        for task, checked in zip(todos, checkedStates):
            if not checked:
                newTodos.append(task)
                newChecked.append(False)

        st.session_state.todoData[todoKey] = newTodos
        st.session_state[checkedKey] = newChecked
        SaveTheState()

# 지금까지 저장된 todolist는 json파일로 저장장
def SaveTheState():
    FILENAME = "todoData.json"
    dataToSave = {}
    for dateKey, todos in st.session_state.todoData.items():
        checkedKey = f"{dateKey}_checked"
        checkedState = st.session_state.get(checkedKey, [False] * len(todos))
        pomodoroCount = st.session_state.pomodoroCounts.get(dateKey, 0)
        dataToSave[dateKey] = {
            "tasks": todos,
            "checked": checkedState,
            "pomodoroCount": pomodoroCount
        }

    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(dataToSave, f, ensure_ascii=False, indent=2)

# json파일을 불러오는 함수수
def LoadTodoData():
    FILENAME = "todoData.json"
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            loadedData = json.load(f)
        
        if 'todoData' not in st.session_state.todoData:
            st.session_state.todoData = {}

        for dateKey, data in loadedData.items():
            # todolist를 json파일에서 불러옴
            st.session_state.todoData[dateKey] = data.get("tasks", [])
            checkedKey = f"{dateKey}_checked"
            
            # todolist에서 체크된 항목을 불러옴
            # 여기서 체크된 항목은 작업을 끝낸 항목
            st.session_state[checkedKey] = data.get("checked", [False]*len(st.session_state.todoData[dateKey]))

            # 선택된 캘린더에서 수행한 포모도로 카운트를 불러옴
            # pomodoroCounts => {'25-05-30' : 3, '25-05-31' :1} 이런식
            if "pomodoroCounts" not in st.session_state:
                st.session_state.pomodoroCounts = {}
            st.session_state.pomodoroCounts[dateKey] = data.get("pomodoroCount", 0)
    else:
        st.session_state.todoData = {}
        st.session_state.pomodoroCounts = {}