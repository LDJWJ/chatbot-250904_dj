import openai
import streamlit as st
from openai import OpenAI
import os

# 페이지 설정
st.set_page_config(
    page_title="여행 AI 챗봇",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS 스타일
st.markdown("""
<style>
    /* 메인 타이틀 스타일 */
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        padding: 1rem 0;
    }
    
    /* 사이드바 스타일 */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* 채팅 메시지 컨테이너 */
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        border-radius: 10px;
        background-color: #f8f9fa;
        margin: 1rem 0;
    }
    
    /* 사용자 메시지 스타일 */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        margin-left: 20%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* AI 메시지 스타일 */
    .ai-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        margin-right: 20%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* 입력 필드 스타일 */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e9ecef;
        padding: 12px 20px;
        font-size: 16px;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* 경고 메시지 스타일 */
    .stAlert {
        border-radius: 10px;
    }
    
    /* 아이콘 스타일 */
    .message-icon {
        font-size: 1.2rem;
        margin-right: 8px;
    }
</style>
""", unsafe_allow_html=True)

# 메인 타이틀
st.markdown('<h1 class="main-title">✈️ 여행 AI 챗봇</h1>', unsafe_allow_html=True)

# 컬럼 레이아웃 생성
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### 🌟 당신의 여행 파트너가 되어드립니다!")
    st.markdown("---")

# 사이드바 설정
with st.sidebar:
    st.markdown("### ⚙️ 설정")
    st.markdown("---")
    
    # API 키 입력
    openai_api_key = st.text_input(
        "🔑 OpenAI API 키", 
        type="password",
        help="OpenAI API 키를 입력해주세요. 키는 안전하게 보호됩니다."
    )
    
    if not openai_api_key:
        st.warning("⚠️ OpenAI API 키를 입력해주세요.")
        st.info("💡 API 키는 OpenAI 웹사이트에서 발급받을 수 있습니다.")
        st.stop()
    else:
        st.success("✅ API 키가 설정되었습니다!")
    
    st.markdown("---")
    
    # 사용법 안내
    st.markdown("### 📖 사용법")
    st.markdown("""
    1. 여행 관련 질문을 입력하세요
    2. 전송 버튼을 클릭하거나 Enter를 누르세요
    3. AI가 친절하게 답변해드립니다!
    
    **예시 질문:**
    - 일본 여행 추천 코스는?
    - 유럽 배낭여행 준비물은?
    - 태국 음식 추천해줘
    """)
    
    st.markdown("---")
    
    # 대화 초기화 버튼
    if st.button("🗑️ 대화 초기화", type="secondary"):
        st.session_state.messages = [
            {"role": "system", 
             "content": "기본적으로 한국어와 영어로 제공해 주세요. "
                       "당신은 여행에 관한 질문에 답하는 친절한 AI 챗봇입니다. "
                       "만약에 여행 외의 질문에 대해서는 정중히 거절하고 여행 관련 질문을 요청해주세요. "
                       "정확하지 않은 정보는 제공하지 말고, 모르는 내용은 솔직히 모른다고 답변해주세요. "
                       "여행지 추천, 준비물, 문화, 음식 등 다양한 여행 관련 주제에 대해 친절하고 상세하게 안내해주세요."
            }
        ]
        st.rerun()

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=openai_api_key)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", 
         "content": "기본적으로 한국어와 영어로 제공해 주세요. "
                   "당신은 여행에 관한 질문에 답하는 친절한 AI 챗봇입니다. "
                   "만약에 여행 외의 질문에 대해서는 정중히 거절하고 여행 관련 질문을 요청해주세요. "
                   "정확하지 않은 정보는 제공하지 말고, 모르는 내용은 솔직히 모른다고 답변해주세요. "
                   "여행지 추천, 준비물, 문화, 음식 등 다양한 여행 관련 주제에 대해 친절하고 상세하게 안내해주세요."
        }
    ]

# 메인 채팅 영역
st.markdown("### 💬 채팅")

# 사용자 입력 영역
with st.container():
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "메시지를 입력하세요...", 
            key="user_input",
            placeholder="여행 관련 질문을 자유롭게 물어보세요! 예: 제주도 여행 코스 추천해줘",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("📤 전송", type="primary", use_container_width=True)

# 메시지 전송 처리
if send_button and user_input.strip():
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    
    # 로딩 스피너 표시
    with st.spinner("🤖 AI가 답변을 생성하고 있습니다..."):
        try:
            # OpenAI API 호출
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            # AI 응답 추가
            response_message = response.choices[0].message.content
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response_message
            })
            
        except Exception as e:
            st.error(f"❌ 오류가 발생했습니다: {str(e)}")
            st.info("💡 API 키를 확인하거나 잠시 후 다시 시도해주세요.")
    
    # 입력 필드 초기화를 위한 rerun
    st.rerun()

# 채팅 메시지 표시
st.markdown("---")

if len(st.session_state.messages) > 1:  # 시스템 메시지 제외
    st.markdown("### 📝 대화 내역")
    
    # 채팅 컨테이너
    chat_container = st.container()
    
    with chat_container:
        # 시스템 메시지를 제외한 대화 내역만 표시
        for message in st.session_state.messages[1:]:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <span class="message-icon">👤</span>
                    <strong>사용자:</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
                
            elif message["role"] == "assistant":
                st.markdown(f"""
                <div class="ai-message">
                    <span class="message-icon">🤖</span>
                    <strong>여행 AI:</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
        
        # 자동 스크롤을 위한 빈 요소
        st.markdown('<div id="bottom"></div>', unsafe_allow_html=True)

else:
    # 환영 메시지
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                border-radius: 15px; color: white; margin: 1rem 0;">
        <h3>🎉 환영합니다!</h3>
        <p>여행에 관한 모든 것을 물어보세요. 저는 당신의 여행을 더욱 특별하게 만들어드릴 AI 어시스턴트입니다!</p>
        <p><strong>💡 팁:</strong> 구체적인 질문일수록 더 정확한 답변을 드릴 수 있어요.</p>
    </div>
    """, unsafe_allow_html=True)

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 1rem;">
    <p>✈️ <strong>여행 AI 챗봇</strong> | 당신의 꿈꾸는 여행을 현실로 만들어드립니다 🌍</p>
    <p><small>⚠️ AI가 생성한 정보는 참고용이며, 실제 여행 계획 시 최신 정보를 확인해주세요.</small></p>
</div>
""", unsafe_allow_html=True)
