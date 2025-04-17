def load_data():
    df = pd.read_excel("조의금_자동화_자료.xlsx")
    df.columns = [col.strip() for col in df.columns]  # 혹시 모를 공백 제거
    st.write("엑셀 열 목록:", df.columns.tolist())  # 확인용 출력

    # 열 이름 자동 매핑 처리
    if '이름' not in df.columns or '금액' not in df.columns:
        # 예: '이 름', '금 액' 같이 띄어쓰기 있을 경우
        df.columns = df.columns.str.replace(" ", "")
    
    df = df.rename(columns={"이름": "이름", "금액": "금액"})
    
    # 중복 처리
    df['표시이름'] = df.groupby('이름').cumcount().astype(str).replace('0', '')
    df['표시이름'] = df.apply(lambda row: row['이름'] if row['표시이름'] == '' else f"{row['이름']} ({int(row['표시이름'])+1})", axis=1)
    return df
