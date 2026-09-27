# app.py
import streamlit as st
import database as db
import logic
import ui_components
import os

# Har reload par database initialization check lagaya taaki cloud data drop na ho
db.init_db()
st.set_page_config(page_title="CodeQuest Multi-Arena", page_icon="💻", layout="centered")
ui_components.draw_header()

if "step" not in st.session_state: 
    st.session_state.step = "home"
if "score" not in st.session_state: 
    st.session_state.score = 0
if "current_q" not in st.session_state: 
    st.session_state.current_q = 0
if "mutated" not in st.session_state: 
    st.session_state.mutated = False
if "eliminated" not in st.session_state: 
    st.session_state.eliminated = False
if "reactions" not in st.session_state: 
    st.session_state.reactions = []

query_params = st.query_params
if "tab_cheat" in query_params and st.session_state.step == "quiz" and not st.session_state.eliminated:
    st.session_state.eliminated = True
    st.rerun()

if st.session_state.step == "quiz" and not st.session_state.eliminated:
    st.components.v1.html(
        """
        <script>
        document.addEventListener('visibilitychange', function() {
            if (document.hidden) {
                window.parent.postMessage({
                    type: 'streamlit:set_query_params',
                    queryParams: {tab_cheat: 'true'}
                }, '*');
                window.location.reload();
            }
        });
        </script>
        """,
        height=0,
    )

if st.session_state.step in ["home", "join_screen", "create_screen"] and not st.session_state.eliminated:
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("🕹️ ENTER MULTI-ARENA (PLAY)", use_container_width=True):
            st.session_state.step = "join_screen"
            st.rerun()
    with col_nav2:
        if st.button("🛠️ FORGE CUSTOM TRACK (HOST)", use_container_width=True):
            st.session_state.step = "create_screen"
            st.rerun()
st.divider()

if st.session_state.eliminated:
    st.markdown(
        """
        <div style='background-color: #E74C3C; padding: 30px; border-radius: 15px; text-align: center; border: 5px solid #FFFFFF;'>
            <h1 style='color: white; font-size: 50px; margin: 0;'>❌ ELIMINATED ❌</h1>
            <h3 style='color: white; margin: 10px 0;'>Tab Switching Detected! Cheating is Prohibited.</h3>
            <p style='color: #FFFF00; font-weight: bold; margin: 0;'>You have been disconnected from the Matrix.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("🔄 Respawn / Main Menu Pe Wapas Jayein", use_container_width=True):
        st.session_state.step = "home"
        st.session_state.score = 0
        st.session_state.current_q = 0
        st.session_state.eliminated = False
        st.session_state.mutated = False
        st.query_params.clear()
        st.rerun()

elif st.session_state.step == "home":
    st.markdown("<h3 style='text-align: center; color: #00FFCC;'>⚠️ ANTI-CHEAT MATRIX IS ACTIVE ⚠️</h3>", unsafe_allow_html=True)
    st.info("💡 Tab Switch = Instant Elimination! Select an option above to boot gameplay parameters.")

elif st.session_state.step == "join_screen":
    st.markdown("<h3 style='text-align: center; color: #FFFFFF;'>🎮 Join Game Room</h3>", unsafe_allow_html=True)
    room_input = st.text_input("Enter 5-Digit Room Code (PIN):", placeholder="e.g. 598835").upper()
    lang_choice = st.selectbox("⚡ Choose Programming Language Target:", ["Python", "JavaScript", "C++", "Java"])
    player_name = st.text_input("Gamer Tag / Nickname:")
    selected_avatar_name, avatar_emoji = ui_components.avatar_selector()
    
    st.write("")
    ui_components.render_lobby_avatars(player_name if player_name else "You", avatar_emoji)
    st.write("")
    
    if st.button("🚀 Break Into Arena", use_container_width=True):
        if room_input and player_name:
            # Force auto-trigger init logic again on live connection matrix to guarantee records loading
            db.init_db()
            st.session_state.player_identity = player_name
            st.session_state.display_name = f"{avatar_emoji} {player_name}"
            st.session_state.room_code = room_input
            st.session_state.selected_lang = lang_choice
            st.session_state.questions = db.get_room_questions(room_input, lang_choice)
            st.session_state.step = "quiz"
            st.rerun()
        else:
            st.error("Invalid configurations! Fill all parameters.")

elif st.session_state.step == "create_screen":
    st.subheader("🛠️ Custom Language Track Studio")
    if "creator_room_code" not in st.session_state:
        st.session_state.creator_room_code = logic.generate_room_code()
    st.success(f"Constructed Room Encryption PIN Code: {st.session_state.creator_room_code}")
    
    with st.form("add_question_form", clear_on_submit=True):
        custom_lang = st.selectbox("Target Programming Tool Language:", ["Python", "JavaScript", "C++", "Java"])
        q_level = st.selectbox("Assign Difficulty Tier:", ["Easy", "Medium", "Hard", "Extreme"])
        q_code = st.text_area("Write Code Snippet Matrix:")
        c1, c2 = st.columns(2)
        with c1:
            o1 = st.text_input("Option 1:")
            o2 = st.text_input("Option 2:")
        with c2:
            o3 = st.text_input("Option 3:")
            o4 = st.text_input("Option 4:")
        correct_ans = st.text_input("Target Correct Output String:")
        
        if st.form_submit_button("➕ Append to Language Matrix"):
            if q_code and o1 and o2 and o3 and o4 and correct_ans:
                db.save_custom_question(st.session_state.creator_room_code, custom_lang, q_level, q_code, o1, o2, o3, o4, correct_ans)
                st.toast("Linked successfully!")
            else:
                st.error("Matrix incomplete!")
                
    if st.button("✅ Launch Room To Public Web", use_container_width=True):
        st.session_state.step = "home"
        del st.session_state.creator_room_code
        st.rerun()

elif st.session_state.step == "quiz":
    st.sidebar.markdown(f"### ⚡ Hacker: {st.session_state.display_name}")
    st.sidebar.markdown(f"### ⚙️ Language: `{st.session_state.selected_lang}`")
    st.sidebar.markdown(f"### 🔑 PIN Room: `{st.session_state.room_code}`")
    st.sidebar.markdown(f"### 🏆 Score: `{st.session_state.score}`")
    
    st.sidebar.write("---")
    st.sidebar.markdown("##### 🎭 Send Live Reaction Emojis:")
    r_col1, r_col2, r_col3, r_col4 = st.sidebar.columns(4)
    with r_col1:
        if st.button("🔥"): 
            st.session_state.reactions.append("🔥")
    with r_col2:
        if st.button("😂"): 
            st.session_state.reactions.append("😂")
    with r_col3:
        if st.button("😮"): 
            st.session_state.reactions.append("😮")
    with r_col4:
        if st.button("👑"): 
            st.session_state.reactions.append("👑")
        
    if st.session_state.reactions:
        st.markdown(f"<div style='background-color: #1F2937; padding: 8px; border-radius: 8px; text-align: center; border: 1px solid #00FFCC;'>💥 Live Floating Reaction Sent: <span style='font-size: 24px;'>{st.session_state.reactions[-1]}</span></div>", unsafe_allow_html=True)
    
    active_questions = st.session_state.questions
    
    if len(active_questions) == 0:
        st.error(f"Is Room code mein {st.session_state.selected_lang} ka koi question load nahi hai!")
        if st.button("🏡 Return Home"):
            st.session_state.step = "home"
            st.rerun()
    else:
        progress_val = st.session_state.current_q / len(active_questions)
        st.progress(progress_val)
        
        if st.session_state.current_q < len(active_questions):
            q = active_questions[st.session_state.current_q]
            ui_components.display_level_badge(q["level"], st.session_state.selected_lang)
            
            display_code = q["code"]
            timer_place = st.empty()
            code_place = st.empty()
            
            user_choice = st.radio("Predict Terminal Compilation Output / Select Correct Code:", q["options"], index=None, key=f"langq_{st.session_state.current_q}")
            locked = st.button("🎯 Lock Selection & Synchronize", use_container_width=True)
            
            if not locked:
                for seconds in range(15, -1, -1):
                    if st.session_state.eliminated:
                        break
                    if seconds <= 5 and not st.session_state.mutated and st.session_state.selected_lang == "Python" and "Target Terminal Output" in display_code:
                        st.session_state.mutated = True
                        display_code = display_code + "\n\n⚠️ SYSTEM ERROR: MUTATION ACTIVE! ⚠️"
                    
                    if st.session_state.mutated:
                        timer_place.markdown(f"<h3 style='color: #E74C3C; text-align: center;'>⚠️ REVERSE MUTATION DETECTED! ⚠️<br>🚨 TIME CRITICAL: {seconds}s</h3>", unsafe_allow_html=True)
                    else:
                        timer_place.markdown(f"<h3 style='color: #2ECC71; text-align: center;'>⏳ Arena Stable. Remaining: {seconds}s</h3>", unsafe_allow_html=True)
                    
                    lang_key = "python" if st.session_state.selected_lang == "Python" else "javascript" if st.session_state.selected_lang == "JavaScript" else "cpp" if st.session_state.selected_lang == "C++" else "java"
                    code_place.code(display_code, language=lang_key)
                    
                    import time
                    time.sleep(1)
                    st.session_state.last_timer_value = seconds
            else:
                lang_key = "python" if st.session_state.selected_lang == "Python" else "javascript" if st.session_state.selected_lang == "JavaScript" else "cpp" if st.session_state.selected_lang == "C++" else "java"
                code_place.code(display_code, language=lang_key)
                time_saved = getattr(st.session_state, 'last_timer_value', 1)
                if user_choice == q["correct"]:
                    pts = logic.calculate_points(time_saved, difficulty=q["level"])
                    if st.session_state.mutated:
                        pts += 300
                    st.session_state.score += pts
                    st.success(f"🥳 Decrypted Successfully! +{pts} Pts")
                else:
                    st.error(f"😢 Compiler Failed. Intended state value: {q['correct']}")
                st.session_state.mutated = False
                st.session_state.current_q += 1
                import time
                time.sleep(1.5)
                st.rerun()
        else:
            db.save_score(st.session_state.room_code, st.session_state.player_identity, st.session_state.score)
            st.session_state.step = "leaderboard"
            st.rerun()
elif st.session_state.step == "leaderboard":
     st.markdown("🏆 THE OVERLORD LEADERBOARD 🏆", unsafe_allow_html=True)
     scores_data = db.get_leaderboard(st.session_state.room_code)
     player_rank = None
     for idx, (p_name, score) in enumerate(scores_data, start=1):
         if p_name == st.session_state.player_identity:
             player_rank = idx
             break
     for rank, (name, score) in enumerate(scores_data, start=1):
         if rank == 1:
            st.markdown(f"🥇 RANK {rank}: {name} — {score} Pts [ARENA OVERLORD]", unsafe_allow_html=True)
         else:
            medal = "🥈" if rank == 2 else "🥉" if rank == 3 else "👾"
     st.markdown(f"### {medal} Rank {rank}: {name} — {score} Pts")
     st.divider()
     st.subheader("📜 Cryptographic Verification Terminal")
     if player_rank and player_rank <= 3:
        st.success(f"👑 Divine Matrix Clear! Rank {player_rank} Secured!")
        cert_file = logic.create_certificate(st.session_state.player_identity, rank=player_rank)
     else:
        st.info("👍 Stage clear. Fetching certificate...")
        cert_file = logic.create_certificate(st.session_state.player_identity, rank=None)
     with open(cert_file, "rb") as file:
        st.download_button(
            label="📥 Export Digital Signature Certificate (PNG)",
            data=file,
            file_name=os.path.basename(cert_file),
            mime="image/png",
            use_container_width=True
        )
     if st.button("🔄 Recycle Core Hub System", use_container_width=True):
         st.session_state.step = "home"
         st.session_state.score = 0
         st.session_state.current_q = 0
         st.session_state.reactions = []
         st.query_params.clear()
         st.rerun()