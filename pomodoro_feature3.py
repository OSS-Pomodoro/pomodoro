import streamlit as st
import pandas as pd
import altair as alt

def ShowPomodoroStats():
    st.subheader("📊 Pomodoro Statistics")
    data = st.session_state.get('pomodoroCounts', {})
    if not data:
        st.info("아직 완료된 포모도로가 없습니다.")
        return

    df = pd.DataFrame(list(data.items()), columns=['Date', 'Count'])
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date').sort_index()

    # 월 기준 주차 계산 함수
    def get_week_of_month(dt):
        first_day = dt.replace(day=1)
        dom = dt.day
        adjusted_dom = dom + first_day.weekday()
        return int((adjusted_dom - 1) / 7 + 1)
    
    def draw_bar_chart(dataframe, title, x_col, y_col='Count', horizontal=False, bar_size=10):
        chart = alt.Chart(dataframe).mark_bar(size=bar_size)
        if horizontal:
            chart = chart.encode(
                y=alt.Y(x_col, sort='-x', title=''),
                x=alt.X(f'{y_col}:Q', title='완료한 횟수')
            )
        else:
            chart = chart.encode(
                x=alt.X(x_col, sort=None, title='', axis=alt.Axis(labelAngle=0)),
                y=alt.Y(f'{y_col}:Q', title='완료한 횟수')
            )
        return chart.properties(title=title, width='container')


    # ── 일별
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 일별")
        st.altair_chart(draw_bar_chart(df.reset_index(), "", 'Date:T'), use_container_width=True)


    with col2:
        st.markdown("### 주별")
        weekly_df = df.resample('W-MON').sum().reset_index()

        def get_week_of_month(dt):
            first_day = dt.replace(day=1)
            dom = dt.day
            adjusted_dom = dom + first_day.weekday()
            return int((adjusted_dom - 1) / 7)

        weekly_df['WeekNo'] = weekly_df['Date'].apply(get_week_of_month)
        weekly_df['MonthName'] = weekly_df['Date'].dt.strftime('%b')
        weekly_df['Label'] = weekly_df['MonthName'] + '-' + weekly_df['WeekNo'].astype(str)

        st.altair_chart(
            draw_bar_chart(weekly_df, "", 'Label:N', horizontal=False),
            use_container_width=True
        )

    # ── 월별
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### 월별")
        monthly_df = df.resample('M').sum().reset_index()
        monthly_df['Label'] = monthly_df['Date'].dt.strftime('%m')
        st.altair_chart(draw_bar_chart(monthly_df, "", 'Label:N'), use_container_width=True)

    # ── 연도별
    with col4:
        st.markdown("### 연도별")
        yearly_df = df.resample('Y').sum().reset_index()
        yearly_df['Label'] = yearly_df['Date'].dt.strftime('%Y')
        st.altair_chart(draw_bar_chart(yearly_df, "", 'Label:N'), use_container_width=True)
