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