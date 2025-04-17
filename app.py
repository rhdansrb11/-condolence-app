import streamlit as st
import pandas as pd

# 엑셀 파일에서 데이터 불러오기 (조의금_자동화_자료.xlsx)
@st.cache_data
def load_data():
    df = pd.read_excel("조의금_자동화_자료.xlsx")
    df.columns = [col.strip() for col in df.columns]  # 혹시 모를 공백 제거
    df = df.rename(columns={"이름": "이름", "금액": "금액"})
    # 이름 중복 처리
    df['표시이름'] = df.groupby('이름').cumcount().astype(str).replace('0', '')
    df['표시이름'] = df.apply(lambda row: row['이름'] if row['표시이름'] == '' else f"{row['이름']} ({int(row['표시이름'])+1})", axis=1)
    return df

# 데이터 불러오기
df = load_data()

st.title("조의금 명단 자동화")

# 사용자 이름 입력
query = st.text_input("이름을 입력하세요:")

# 자동완성 후보 필터링 (한 글자 이상부터 추천)
if len(query) >= 1:
    suggestions = df[df['표시이름'].str.contains(query)]
    if not suggestions.empty:
        selected_name = st.selectbox("추천된 이름에서 선택:", suggestions['표시이름'].tolist())
        if selected_name in df['표시이름'].values:
            selected_info = df[df['표시이름'] == selected_name].iloc[0]
            st.success(f"{selected_info['표시이름']} 님의 조의금은 {selected_info['금액']}만원입니다.")
        else:
            st.warning("선택한 이름이 명단에 없습니다.")
    else:
        st.warning("일치하는 이름이 없습니다.")

# 전체 명단 표시
with st.expander("전체 조의금 명단 보기"):
    st.dataframe(df[['표시이름', '금액']].rename(columns={'표시이름': '이름'}))