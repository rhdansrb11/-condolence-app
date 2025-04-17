import streamlit as st
import pandas as pd

# 엑셀 파일에서 데이터 불러오기
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("조의금_자동화_자료.xlsx", engine="openpyxl")
        df.columns = [col.strip() for col in df.columns]

        if '이름' not in df.columns or '금액' not in df.columns:
            st.error("엑셀 파일에 '이름' 또는 '금액' 열이 없습니다. 열 이름을 확인해주세요.")
            return pd.DataFrame(columns=['이름', '금액'])

        return df
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류 발생: {e}")
        return pd.DataFrame(columns=['이름', '금액'])

# 데이터 불러오기
df = load_data()

st.title("조의금 명단 자동화")

# 사용자 이름 입력
query = st.text_input("이름을 입력하세요:")

if not df.empty:
    if query:
        # 추천 이름 목록 필터링
        recommendations = df[df['이름'].str.contains(query, case=False, na=False)]['이름'].unique()
        st.write("추천 이름:")
        for name in recommendations:
            st.write(f"- {name}")

        # 정확히 일치하는 이름 검색
        matches = df[df['이름'].str.strip().str.lower() == query.strip().lower()]

        if len(matches) >= 1:
            matches = matches.copy()
            matches['이름_표시'] = matches['이름']
            duplicated = matches.duplicated(subset=['이름'], keep=False)
            if duplicated.any():
                matches.loc[duplicated, '이름_표시'] = matches.loc[duplicated, '이름'] + ' (' + (matches.groupby('이름').cumcount() + 1).astype(str) + ')'
            st.table(matches[['이름_표시', '금액']].rename(columns={'이름_표시': '이름'}).reset_index(drop=True))
        else:
            st.warning("일치하는 이름이 없습니다.")