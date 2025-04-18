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
    # 전체 보기 기능
    if st.button("전체 보기"):
        df_sorted = df.copy()
        df_sorted = df_sorted.sort_values(by='이름').reset_index(drop=True)

        # 중복 이름 처리
        name_counts = df_sorted.groupby('이름').cumcount()
        df_sorted['이름_표시'] = df_sorted['이름']
        df_sorted.loc[name_counts > 0, '이름_표시'] += ' (' + (name_counts[name_counts > 0] + 1).astype(str) + ')'

        st.subheader("전체 명단")
        st.table(df_sorted[['이름_표시', '금액']].rename(columns={'이름_표시': '이름'}))

    # 이름 검색
    if query:
        recommendations = df[df['이름'].str.contains(query, case=False, na=False)]['이름'].unique()
        st.write("추천 이름:")
        for name in recommendations:
            st.write(f"- {name}")

        matches = df[df['이름'].str.strip().str.lower() == query.strip().lower()]

        if not matches.empty:
            counts = matches.groupby('이름').cumcount()
            matches['이름_표시'] = matches['이름']
            matches.loc[counts > 0, '이름_표시'] += ' (' + (counts[counts > 0] + 1).astype(str) + ')'

            st.subheader("검색 결과")
            st.table(matches[['이름_표시', '금액']].rename(columns={'이름_표시': '이름'}).reset_index(drop=True))
        else:
            st.warning("일치하는 이름이 없습니다.")
