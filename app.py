# motivational_quotes.py

import random
import pomodoro_stats  # 다른 팀원이 만든 통계 모듈 가져오기

def get_quote_by_level(session_count):
    """명언 레벨 시스템: 누적 세션 수에 따른 분류"""
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
    if session_count <= 2:
        return random.choice(level_1)
    elif session_count <= 6:
        return random.choice(level_2)
    else:
        return random.choice(level_3)


def get_quote_by_recent_completion_rate():
    """최근 2주간 뽀모도로 완료율에 따른 동기부여 메시지 (외부 모듈에서 값 가져옴)"""
    rate = pomodoro_stats.get_recent_completion_rate()
    if rate >= 0.8:
        return "🔥 최근 집중이 매우 좋습니다! 이 기세를 유지해요!"
    elif rate >= 0.5:
        return "💪 나쁘지 않은 흐름이에요. 조금만 더 힘내요!"
    else:
        return "🌧 최근 집중이 흔들렸어요. 다시 흐름을 회복해봐요!"


def get_quote_by_result(result_type):
    """뽀모도로 종료 후 상황에 따른 메시지"""
    success_quotes = [
        "🎉 집중 성공! 당신은 해냈습니다.",
        "🙌 오늘도 집중 완료! 멋져요!",
        "🌟 집중력 만렙! 지금 흐름을 유지해요."
    ]
    skip_quotes = [
        "🌀 잠시 흐트러졌지만 괜찮아요. 다시 도전해봐요!",
        "🤍 포기하지 말아요. 다시 일어서는 용기가 중요해요.",
        "📌 지금 멈췄다고 실패는 아니에요. 다시 시작해요!"
    ]
    repeated_fail_quotes = [
        "🔁 실패는 연습입니다. 계속 시도해요!",
        "🛠 실천이 어렵다는 걸 아는 것도 성장입니다.",
        "⏳ 쉬어가도 괜찮아요. 중요한 건 멈추지 않는 것."
    ]
    if result_type == "success":
        return random.choice(success_quotes)
    elif result_type == "skip":
        return random.choice(skip_quotes)
    elif result_type == "fail_repeat":
        return random.choice(repeated_fail_quotes)
    else:
        return "💬 당신은 충분히 잘하고 있어요."


def get_quote_by_total_completion_rate():
    """전체 누적 완료율에 따른 격려 메시지 (외부 모듈에서 값 가져옴)"""
    rate = pomodoro_stats.get_total_completion_rate()
    if rate >= 0.9:
        return "🏆 완벽에 가까운 꾸준함! 자랑스러워요."
    elif rate >= 0.6:
        return "📈 좋은 흐름이에요. 내일도 잘 부탁해요!"
    else:
        return "🌱 조금 부족했지만 괜찮아요. 꾸준함이 이겨요."
