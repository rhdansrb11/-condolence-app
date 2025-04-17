import streamlit as st
import pandas as pd

# 엑셀 파일에서 데이터 불러오기 (조의금_자동화_자료.xlsx)
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("조의금_자동화_자료.xlsx", engine="openpyxl")
        df.columns = [col.strip() for col in df.columns]  # 혹시 모를 공백 제거

        # 컬럼 이름이 정확히 있는지 확인
        if '이름' not in df.columns or '금액' not in df.columns:
            st.error("엑셀 파일에 '이름' 또는 '금액' 열이 없습니다. 열 이름을 확인해주세요.")
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

st.title("조의금 명단 자동화")

# 사용자 이름 입력
query = st.text_input("이름을 입력하세요:")

if not df.empty:
    if query:
        # 입력한 내용으로 정확히 일치하는 이름만 필터링
        matches = df[df['표시이름'].str.fullmatch(query.strip(), na=False)]

        if len(matches) >= 1:
            with st.expander("🔍 검색 결과 보기", expanded=True):
                st.table(matches[['표시이름', '금액']].reset_index(drop=True))
        else:
            st.warning("일치하는 이름이 없습니다.")
