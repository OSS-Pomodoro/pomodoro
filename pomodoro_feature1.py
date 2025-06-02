# pomodoro_feature1.py

import random
#import 통계 모듈
import pomodoro_feature2  # 팀원이 만든 todoData 관련 모듈
from datetime import date

# 오늘 날짜 문자열 (ex: '2025-05-29')
today = date.today().strftime("%Y-%m-%d")


def get_quote_by_level_today():
    #오늘 날짜 기준 pomodoroCount에 따른 명언 레벨 시스템
    
    count = pomodoro_feature2.st.session_state.pomodoroCounts.get(today, 0)

    level_1 = [
        "🚀 시작이 반이다.",
        "🔥 오늘도 도전해보자!",
        "💡 첫 걸음을 내딛는 당신이 멋져요."
    ]
    level_2 = [
        "🌱 작은 꾸준함이 큰 성장을 만듭니다.",
        "📚 반복은 실력을 만든다.",
        "🧱 한 블럭씩 쌓아가며 나아가요."
    ]
    level_3 = [
        "🏁 당신은 이미 습관을 이룬 사람입니다.",
        "🎯 포기하지 않는 자가 이긴다.",
        "🌟 당신의 집중력은 놀랍습니다."
    ]

    if count <= 2:
        return random.choice(level_1)
    elif count <= 6:
        return random.choice(level_2)
    else:
        return random.choice(level_3)


def get_feedback_after_session():
    #뽀모로도 종료 후 : 오늘의 피드백 - 누적 pomodoroCounts에 따라 동기부여되는 명언/피드백 작성 
    checkedkey = f"{today}_checked"
    checked_list = pomodoro_feature2.st.session_state.get(checkedkey, [])
    completed_tasks = sum(checked_list)
    pomodoro_count = pomodoro_feature2.st.session_state.pomodoroCounts.get(today, 0)

    if completed_tasks >= 3 and pomodoro_count >= 6:
        return "🏆 오늘 큰 목표를 완수했어요! 자랑스러워요."
    elif completed_tasks >= 1 and pomodoro_count >= 3:
        return "✅ 성실히 임하고 있어요. 계속해서 도전해요!"
    else:
        return "🌱 아직 시작일 뿐이에요. 작게라도 실천해봐요."

""" 
def get_quote_by_recent_completion_rate():
    #통계에 따른 피드백 : 최근 2주간 뽀모도로 통계에 따른 동기부여 메시지 (통계 모듈에서 값 가져와서)
    rate = pomodoro_stats.get_recent_completion_rate()
    if rate >= 0.8:
        return "🔥 최근 집중이 매우 좋습니다! 이 기세를 유지해요!"
    elif rate >= 0.5:
        return "💪 나쁘지 않은 흐름이에요. 조금만 더 힘내요!"
    else:
        return "🌧 최근 집중이 흔들렸어요. 다시 흐름을 회복해봐요!"
"""