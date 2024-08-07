import streamlit as st
import pandas as pd
from openai import OpenAI

# OpenAI API 키 설정
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# 2022 개정 교육과정 성취기준 데이터 (예시, 실제로는 더 많은 데이터가 필요합니다)
achievement_standards = {
    "중학교": {
        "1-2학년": [
            "[9국02-05] 글에 사용된 다양한 논증 방법을 파악하며 읽는다.",
            "[9국03-04] 주장하는 내용에 맞게 타당한 근거를 들어 글을 쓴다.",
            # 추가 성취기준...
        ],
        "3학년": [
            # 3학년 성취기준...
        ]
    },
    "고등학교": {
        "공통 과목": [
            # 공통 과목 성취기준...
        ],
        "선택 과목": [
            # 선택 과목 성취기준...
        ]
    }
}

# GRASPS 요소 선택 옵션
grasps_options = {
    "목표(G)": ["설명한다", "논증한다", "기술한다", "표현한다", "보여준다", "도출한다", "증명한다", "예측한다", "말한다"],
    "역할(R)": ["배우", "광고 기획자", "미술작가", "사장", "사업가", "후보자", "캐릭터", "만화가", "요리사", "대통령", "유튜버"],
    "대상(A)": ["학생", "학부모", "지역 주민", "정부 관계자", "기업가", "전문가", "일반 대중"],
    "상황(S)": ["학교 행사", "지역 문제", "사회 이슈", "환경 문제", "기술 혁신", "문화 교류"],
    "수행(P)": ["보고서 작성", "프레젠테이션", "토론", "포스터 제작", "동영상 제작", "캠페인 기획"],
    "기준(S)": ["창의성", "논리성", "실현 가능성", "협업 능력", "의사소통 능력", "문제 해결력"]
}

def get_gpt_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 GRASPS 모형을 활용한 프로젝트 수업 설계를 돕는 전문가입니다."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"

st.title("GRASPS 기반 국어 프로젝트 수업 설계 도우미")

# 학교급 선택
school_level = st.selectbox("학교급 선택", ["중학교", "고등학교"])

# 학년 또는 과목 선택
if school_level == "중학교":
    grade = st.selectbox("학년 선택", ["1-2학년", "3학년"])
else:
    grade = st.selectbox("과목 선택", ["공통 과목", "선택 과목"])

# 성취기준 선택
selected_standard = st.selectbox("성취기준 선택", achievement_standards[school_level][grade])

# GRASPS 요소 입력
st.subheader("GRASPS 요소 설정")
goal = st.selectbox("목표(G)", grasps_options["목표(G)"])
role = st.selectbox("역할(R)", grasps_options["역할(R)"])
audience = st.selectbox("대상(A)", grasps_options["대상(A)"])
situation = st.selectbox("상황(S)", grasps_options["상황(S)"])
performance = st.selectbox("수행(P)", grasps_options["수행(P)"])
standards = st.multiselect("기준(S)", grasps_options["기준(S)"])

if st.button("프로젝트 수업 설계 생성"):
    prompt = f"""
    다음 정보를 바탕으로 GRASPS 모형에 따른 국어 프로젝트 수업을 설계해주세요:
    
    학교급: {school_level}
    학년/과목: {grade}
    성취기준: {selected_standard}
    
    GRASPS 요소:
    - 목표(G): {goal}
    - 역할(R): {role}
    - 대상(A): {audience}
    - 상황(S): {situation}
    - 수행(P): {performance}
    - 기준(S): {', '.join(standards)}
    
    다음 형식으로 프로젝트 수업 계획을 작성해주세요:
    1. 프로젝트 제목
    2. 프로젝트 개요
    3. 학습 목표
    4. 주요 활동 단계
    5. 평가 방법
    6. 기대 효과
    """
    
    response = get_gpt_response(prompt)
    st.markdown("## 생성된 프로젝트 수업 계획")
    st.markdown(response)

st.markdown("---")
st.markdown("이 앱을 통해 GRASPS 모형을 활용한 프로젝트 수업을 쉽게 설계할 수 있습니다. 생성된 계획을 바탕으로 필요에 따라 수정 및 보완하여 사용하세요.")
