import streamlit as st
import datetime
from agents.v1_rule_based import StudyAgentV1
from agents.v2_llm_only import StudyAgentV2
from agents.v3_llm_with_tool import StudyAgentV3
from agents.v4_memory import StudyAgentV4


st.set_page_config(page_title="Study Assistant Agent", page_icon="🧠", layout="wide")

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #1f4037, #99f2c8);
    color: white;
}
            
/* CHAT WRAPPER */
.chat-wrapper {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

/* COMMON MESSAGE STYLE */
.chat-bubble {
    padding: 12px 16px;
    border-radius: 18px;
    min-width:450px;
            max-width:800px;
    font-size: 30px;
    line-height: 1.4;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

/* USER MESSAGE (RIGHT SIDE) */
.user-container {
    display: flex;
    justify-content: flex-end;
}

.user-bubble {
    background: #DCF8C6;
    color: black;
    border-bottom-right-radius: 5px;
}

/* BOT MESSAGE (LEFT SIDE) */
.bot-container {
    display: flex;
    justify-content: flex-start;
}

.bot-bubble {
    background: #ffffff;
    color: black;
    border-bottom-left-radius: 5px;
}

/* TIMESTAMP */
.timestamp {
    font-size: 11px;
    opacity: 0.6;
    margin-top: 3px;
}

/* INPUT BOX STYLE */
[data-testid="stChatInput"] {
    position: fixed;
    bottom: 10px;
    width: 60%;
}

</style>
""", unsafe_allow_html=True)


st.title("🧠 Study Assistant AI Agents")
st.write("Choose an agent and start chatting 🚀")

st.sidebar.title("⚙️ Select Agent")

agent_option = st.sidebar.selectbox(
    "Choose Model",
    (
        "Rule-Based Agent",
        "LLM Only Agent",
        "LLM + Tools Agent",
        "Memory Agent"
    )
)

@st.cache_resource
def load_agent(option):
    if option == "Rule-Based Agent":
        return StudyAgentV1()
    elif option == "LLM Only Agent":
        return StudyAgentV2()
    elif option == "LLM + Tools Agent":
        return StudyAgentV3()
    elif option == "Memory Agent":
        return StudyAgentV4()
    

agent = load_agent(agent_option)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("<div class='chat-wrapper'>", unsafe_allow_html=True)

for role, message in st.session_state.chat_history:

    time = datetime.datetime.now().strftime("%H:%M")

    if role == "user":
        st.markdown(f"""
        <div class="user-container">
            <div>
                <div class="chat-bubble user-bubble">
                    👤 {message}
                    <div class="timestamp">{time}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div class="bot-container">
            <div>
                <div class="chat-bubble bot-bubble">
                    🤖 {message}
                    <div class="timestamp">{time}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    try:
        response = agent.run(user_input)
    except:
        response = "⚠️ Error running agent"

    st.session_state.chat_history.append(("bot", str(response)))

    st.rerun()
