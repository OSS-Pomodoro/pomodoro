# pomodoro_feature1.py

import random
import pomodoro_feature2  # todoData 모듈
from datetime import date, datetime, timedelta
import base64
import streamlit.components.v1 as components
# 오늘 날짜 문자열 (ex: '2025-05-29')
today = date.today().strftime("%Y-%m-%d")

def get_quote_by_level_today():
    #오늘 날짜 기준 pomodoroCount에 따른 명언 레벨 시스템
    
    count = pomodoro_feature2.st.session_state.pomodoroCounts.get(today, 0)

    level_1 = [ # 주제 : 시작, 명언
        "🚀 시작이 반이다. - 아리스토텔레스",
        "🔥 해보지 않고는 당신이 무엇을 해낼 수 있는지 알 수 없다. - 프랭클린 아담",
        "💡 시작하는 사람만이 성공할 수 있다. - 나폴레옹",
        "🚀 지금 할 수 있는 일부터 시작하라. - 괴테",
        "🔥 시작하기에 가장 완벽한 곳은 바로 지금 당신이 있는 그 곳이다. - Dieter F.Uchtdorf" 
    ]
    level_2 = [ # 주제 : 꾸준함, 끈기 
        "🧱 가장 잘 견디는 자가 가장 잘 해낼 수 있는 자이다. - 존 밀턴 -",
        "🌱 하나의 작은 꽃을 만드는데도 오랜 세월의 노력이 필요하다. - 윌리엄 블레이크",
        "📚 멈추지 않는 한 얼마나 천천히 가는 지는 중요하지 않다. - 공자",
        "🧱 시냇물과 바위의 대결에서 시냇물은 항상 이긴다. 힘이 아니라 끈기로. - 잭슨 브라운 주니어",
        "🌱 인내는 고통을 견디는 것이 아니라 목표를 견디는 것이다. - 나폴레옹 힐",
        "📚 지금 힘들다면 잘하고 있는 것이다. - 전옥표"
    ]
    level_3 = [ # 주제 : 승리, 성취
        "🌟 진정한 성취는 타인과의 비교가 아닌, 어제의 나와의 비교에서 탄생한다. - 로이 베넷",
        "🏁 어제보다 나은 내가 되면 충분하다.",
        "🎯 포기하지 않는 자가 이긴다.",
        "🌟 작은 변화가 큰 차이를 만든다. - 말콤 글래드웰",
        "🎯 자기만족은 기업경영 최대의 적이다. - 마이크 델",
        "🏁 성공은 끝이 아니며, 실패는 치명적이지 않다. 중요한 것은 계속 나아갈 용기다. - 윈스턴 처칠"

    ]

    if count <= 2:
        return random.choice(level_1)
    elif count <= 6:
        return random.choice(level_2)
    else:
        return random.choice(level_3)


def get_feedback_after_pomodoro():
    #뽀모로도 종료 후 : 오늘의 피드백 - 누적 pomodoroCounts에 따라 동기부여되는 명언/피드백 작성 
    checkedkey = f"{today}_checked"
    checked_list = pomodoro_feature2.st.session_state.get(checkedkey, [])
    completed_tasks = sum(checked_list)
    total_tasks = len(checked_list)
    pomodoro_count = pomodoro_feature2.st.session_state.pomodoroCounts.get(today, 0)

    if (total_tasks > 0 and completed_tasks == total_tasks) or pomodoro_count >= 6:
        return "🏆 오늘 완벽하게 해냈어요! 대단해요!"
    elif completed_tasks >= 1 or pomodoro_count >= 3:
        return "✅ 성실히 임하고 있어요. 이대로만 가도 좋아요!"
    elif completed_tasks >= 1:
        return "✅ 방향은 잡았어요. 내일은 한 걸음만 더 내디뎌봐요!"
    else:
        return "언제까지 그렇게 살래?!!?!!"


def get_quote_by_recent_completion_rate():
    #통계에 따른 피드백: 최근 2주간 포모도로 횟수 기반으로 동기부여 메시지 출력
    counts = pomodoro_feature2.st.session_state.get("pomodoroCounts", {})
    if not counts:
        return "📉 최근 완료된 포모도로가 없습니다. 지금부터 시작해볼까요?"

    two_weeks_ago = datetime.today() - timedelta(days=14)
    recent_total = 0

    for date_str, count in counts.items():
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            if dt >= two_weeks_ago:
                recent_total += count
        except:
            continue

    # 2주 기준 추천 횟수: 하루 2회 × 14일 = 28회
    completion_rate = recent_total / 28

    if completion_rate >= 0.8:
        return "🔥 최근 집중이 매우 좋습니다! 이 기세를 유지해요!"
    elif completion_rate >= 0.5:
        return "💪 나쁘지 않은 흐름이에요. 조금만 더 힘내요!"
    elif completion_rate >= 0.2:
        return "🌧 최근 집중이 흔들렸어요. 다시 흐름을 회복해봐요!"
    else:
        return "🪞 당신은 지금 멈춰 있어요. 다시 시작할 시간이에요."  


#########추가#########
# 음악 base64로 인코딩
def encode_music_file(file):
    if file is None:
        return None
    return base64.b64encode(file.read()).decode()

# 음악+타이머 재생
def play_music_with_timer(html_circle, music_base64, autoplay=True):
    audio_tag = f"""
    <audio {'autoplay' if autoplay else ''} loop id="bg-music">
        <source src="data:audio/mp3;base64,{music_base64}" type="audio/mpeg">
    </audio>
    """
    combined_html = f"{html_circle}{audio_tag}"
    components.html(combined_html, height=280)
