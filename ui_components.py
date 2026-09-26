# ui_components.py
import streamlit as st
import time

def draw_header():
    st.markdown(
        """
        <style>
            @import url('https://googleapis.com');
            html, body, [data-testid="stAppViewContainer"] {
                font-family: 'Lexend', sans-serif !important;
                background-color: #0E1117;
            }
            .quiz-header {
                background: linear-gradient(135deg, #FF3366, #6600CC);
                padding: 25px;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0px 8px 24px rgba(102, 0, 204, 0.5);
                margin-bottom: 25px;
            }
            .quiz-title {
                font-family: 'Fredoka One', cursive !important;
                color: #FFFFFF;
                margin: 0;
                font-size: 42px;
            }
            .quiz-subtitle {
                color: #00FFCC;
                margin: 8px 0 0 0;
                font-weight: 700;
                font-size: 14px;
                letter-spacing: 3px;
            }
            .avatar-card {
                display: inline-block;
                text-align: center;
                margin: 15px;
            }
            .avatar-circle {
                width: 75px;
                height: 75px;
                border-radius: 50%;
                background-color: #1F2937;
                border: 4px solid #00FFCC;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 36px;
                margin: 0 auto 8px auto;
            }
            .avatar-name {
                color: #FFFFFF;
                font-weight: 700;
                font-size: 14px;
            }
        </style>
        <div class='quiz-header'>
            <h1 class='quiz-title'>✏️ CODEQUEST.com</h1>
            <p class='quiz-subtitle'>⚡ MULTIPLAYER PROGRAMMING ARENA ⚡</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

def render_lobby_avatars(player_name, avatar_emoji):
    st.markdown(
        f"""
        <div class='avatar-card'>
            <div class='avatar-circle'>{avatar_emoji}</div>
            <div class='avatar-name'>{player_name}</div>
        </div>
        """, 
        unsafe_allow_html=True
    )

def display_level_badge(level, lang):
    color_map = {"Easy": "#2ECC71", "Medium": "#F1C40F", "Hard": "#E67E22", "Extreme": "#E74C3C"}
    hex_color = color_map.get(level, "#34495E")
    st.markdown(
        f"""
        <div style='background-color: {hex_color}; padding: 10px; border-radius: 12px; text-align: center; border: 2px solid #FFFFFF; margin-bottom: 20px;'>
            <h4 style='color: white; margin: 0; font-weight: 700; letter-spacing: 2px;'>🕹️ {lang.upper()} ARENA | LEVEL: {level.upper()}</h4>
        </div>
        """, 
        unsafe_allow_html=True
    )

def avatar_selector():
    avatars = {"🦊 CyberFox": "🦊", "🥷 CodeNinja": "🥷", "🐼 TechPanda": "🐼", "🦁 ByteLion": "🦁", "🤖 RoboCoder": "🤖"}
    selected = st.selectbox("🎯 Choose Your Game Avatar Icon:", list(avatars.keys()))
    return selected, avatars[selected]

def run_countdown_timer(time_limit=15):
    timer_place = st.empty()
    for seconds in range(time_limit, -1, -1):
        if st.session_state.get("eliminated", False):
            break
        if seconds > 5:
            timer_place.markdown(f"<h3 style='color: #2ECC71; text-align: center;'>⏳ TIME REMAINING: {seconds}s</h3>", unsafe_allow_html=True)
        else:
            timer_place.markdown(f"<h3 style='color: #E74C3C; text-align: center;'>🚨 HURRY UP: {seconds}s 🚨</h3>", unsafe_allow_html=True)
        time.sleep(1)
        st.session_state.last_timer_value = seconds