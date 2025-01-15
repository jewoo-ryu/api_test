import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import os

def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def analyze_lg_twins(text, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    다음은 KBO 기록 데이터입니다:
    {text}
    
    이 데이터에서 LG 트윈스와 관련된 내용만 분석하여:
    1. 2023년 주요 성과와 한계점
    2. 2024년 시즌을 위한 개선점과 전략 제안
    3. 중점적으로 보강이 필요한 부분
    
    위 항목들에 대해 상세히 분석해주세요.
    """
    
    response = model.generate_content(prompt)
    return response.text

def main():
    st.title("LG 트윈스 2024 시즌 분석기")
    
    # API 키 입력
    api_key = st.text_input("Google API 키를 입력하세요", type="password")
    
    # PDF 파일 업로드
    uploaded_file = st.file_uploader("KBO 기록 PDF 파일을 업로드하세요", type="pdf")
    
    if uploaded_file and api_key:
        try:
            # PDF에서 텍스트 추출
            text = extract_text_from_pdf(uploaded_file)
            
            if st.button("분석 시작"):
                with st.spinner("분석 중입니다..."):
                    # 분석 실행
                    analysis = analyze_lg_twins(text, api_key)
                    st.success("분석이 완료되었습니다!")
                    st.markdown(analysis)
                    
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
    
    st.markdown("""
    ### 사용 방법
    1. Google API 키를 입력해주세요
    2. KBO 기록이 담긴 PDF 파일을 업로드해주세요
    3. '분석 시작' 버튼을 클릭하면 분석이 시작됩니다
    """)

if __name__ == "__main__":
    main()