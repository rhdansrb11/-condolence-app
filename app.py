import streamlit as st
import pandas as pd

# 엑셀 파일에서 데이터 불러오기
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("조의금_자동화_자료.xlsx", engine="openpyxl")
        df.columns = [col.strip() for col in df.columns]

        if '이름' not in df.columns or '금액' not in df.columns:
            st.error("엑셀 파일에 '이름' 또는 '금액' 열이 없습니다.")
            return pd.DataFrame(columns=['이름', '금액', '표시이름'])

        # 이름 중복 처리
        df['표시이름'] = df.groupby('이름').cumcount().astype(str).replace('0', '')
        df['표시이름'] = df.apply(lambda row: row['이름'] if row['표시이름'] == '' else f"{row['이름']} ({int(row['표시이름'])+1})", axis=1)
        return df
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류 발생: {e}")
        return pd.DataFrame(columns=['이름', '금액', '표시이름'])

# 데이터 불러오기
df = load_data()

st.title("💐 조의금 명단 자동화")

query = st.text_input("이름을 입력하세요:")

if query and not df.empty:
    # 입력한 내용으로 '이름' 기준 필터링
    matches = df[df['이름'].str.contains(query, na=False)]

    if len(matches) == 1:
        row = matches.iloc[0]
        st.success(f"{row['표시이름']} 님의 조의금은 {row['금액']}만원입니다.")
    elif len(matches) > 1:
        selected = st.selectbox("여러 명이 검색되었습니다. 선택해주세요:", matches['표시이름'].tolist())
        row = matches[matches['표시이름'] == selected].iloc[0]
        st.success(f"{row['표시이름']} 님의 조의금은 {row['금액']}만원입니다.")
    else:
        st.warning("일치하는 이름이 없습니다.")

    # 추천 이름 보기
    with st.expander("🔍 추천 이름 보기"):
        st.write(matches[['표시이름']].drop_duplicates().reset_index(drop=True))

# 전체 명단
if not df.empty:
    with st.expander("📋 전체 조의금 명단 보기"):
        st.dataframe(df[['표시이름', '금액']].rename(columns={'표시이름': '이름'}))