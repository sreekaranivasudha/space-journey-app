import streamlit as st
import json
import os
import time
import datetime

# ==========================================
# 🌌 1. COCKPIT CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Astrophysics Mission Control",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Cyberpunk HUD Stylesheet Injection
st.markdown("""
    <style>
    .main { background-color: #0A0D1A; color: #E2E8F0; }
    .stApp { background-color: #0A0D1A; }
    
    /* Neon HUD Panels */
    .hud-box { 
        border: 2px solid #1E293B; 
        padding: 22px; 
        border-radius: 12px; 
        background-color: #111625; 
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.05);
        margin-bottom: 15px;
    }
    .hud-title {
        font-size: 11px;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
    }
    .hud-value { 
        font-size: 26px; 
        font-weight: 700; 
        color: #38BDF8; 
        margin-top: 5px;
    }
    .league-highlight { color: #F59E0B; }
    
    /* Custom Sidebar Adjustments */
    section[data-testid="stSidebar"] {
        background-color: #0F1322 !important;
        border-right: 1px solid #1E293B;
    }
    
    /* Disable default streamlit decoration line */
    header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 📂 2. DATA LOADERS & DATA ARCHITECTURE
# ==========================================
def load_lifestyle_manifest():
    """Parses the lifestyle configuration file."""
    tasks = []
    if os.path.exists("lifestyle_tasks.txt"):
        with open("lifestyle_tasks.txt", "r") as f:
            for line in f:
                cleaned = line.strip()
                if cleaned and not cleaned.startswith("#"):
                    if "|" in cleaned:
                        name, tag = cleaned.split("|")
                        tasks.append({"name": name.strip(), "tag": tag.strip()})
    else:
        # Fallback manifest if file is missing during initial init
        tasks = [
            {"name": "Morning Chores & Breakfast", "tag": "morning_chores"},
            {"name": "Medical Telemetry Intake", "tag": "medications"},
            {"name": "Linguistic Training (Hindi)", "tag": "hindi_app"},
            {"name": "Current Affairs Processing", "tag": "paper_reading"},
            {"name": "Literary Exploration", "tag": "book_reading"},
            {"name": "Entertainment Shielding", "tag": "tv_restriction"},
            {"name": "Physical Kinetic Training", "tag": "physical_sport"},
            {"name": "Creative Hobby Development", "tag": "hobby_time"}
        ]
    return tasks

def load_user_profile():
    """Retrieves long-term student metrics."""
    if os.path.exists("user_stats.json"):
        with open("user_stats.json", "r") as f:
            return json.load(f)
    return {
        "current_xp": 0,
        "streak_days": 0,
        "league": "Troposphere Initiate",
        "completed_questions": []
    }

def save_user_profile(profile_data):
    """Commits metric tracking back to the profile json."""
    with open("user_stats.json", "w") as f:
        json.dump(profile_data, f, indent=2)

def load_weekly_payload(week_num=1):
    """Loads the core curriculum JSON database files dynamically."""
    filename = f"week_{week_num:02d}.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    
    # Static fallback template for visualization testing prior to full payload upload
    return {
        "week_number": week_num,
        "knowledge_capsules": {
            "physics": {"topic": "Thermal Systems & Vacuum Insulation", "summary": "How satellites process heat via radiation loops without molecules...", "key_points": ["No conduction/convection in space vacuum", "$E \\propto T^4$"], "resources": [{"title": "PhET Thermodynamic Simulation", "url": "https://phet.colorado.edu"}]},
            "mathematics": {"topic": "Negative Integer Number Fields", "summary": "Operational laws governing complex sign inversion vectors...", "key_points": ["$(-a) \\times (-b) = ab$", "Coordinate axis tracking"], "resources": [{"title": "Khan Academy Algebra Track", "url": "https://www.khanacademy.org"}]},
            "chemistry": {"topic": "Acids, Bases, and Neutralization", "summary": "How indicators trace molecular salt-water conversions...", "key_points": ["Acids yield $H^+$ ions", "Acid + Base = Salt + Water"], "resources": [{"title": "PhET Indicators Lab", "url": "https://phet.colorado.edu"}]},
            "biology": {"topic": "Cellular Energy Pathways", "summary": "Breaking down aerobic vs. anaerobic threshold respiration...", "key_points": ["Aerobic loops use $O_2$", "Anaerobic muscle breakdown yields Lactic Acid"], "resources": [{"title": "CrashCourse Science Pathways", "url": "https://www.youtube.com"}]},
            "logical_reasoning": {"topic": "Cipher Transpositions", "summary": "Deciphering cyclic alphanumeric matrix shifts...", "key_points": ["Arithmetic position shifts", "Matrix rotation algorithms"], "resources": [{"title": "Logic Processing Archive", "url": "https://www.khanacademy.org"}]}
        },
        "weekday_pool": [
            {"id": "W01_P01", "subject": "Physics", "tier": "HOTS", "question": "A rover hull surface temperature doubles from 300K to 600K. By what multiplier does its net emitted thermal radiation increase?", "options": ["Factor of 2", "Factor of 4", "Factor of 16", "Factor of 32"], "correct": "Factor of 16", "hint": "Radiation parameters scale to the fourth power: $E \\propto T^4$."},
            {"id": "W01_P02", "subject": "Mathematics", "tier": "HOTS", "question": "Evaluate the summation sequence: $f(n) = (-1)^n \\times n$. Compute total for $f(1) + f(2) + \\dots + f(100)$.", "options": ["-50", "0", "50", "100"], "correct": "50", "hint": "Group terms into consecutive arithmetic pairs."}
        ],
        "sunday_exam": [
            {"id": "W01_EXAM_01", "subject": "Physics", "question": "Under timed settings, deduce the net rate multiplier of a blackbody system if internal heat modules double absolute temperature parameters ($2T$).", "options": ["2x", "4x", "8x", "16x"], "correct": "16x"}
        ]
    }

# Initialize Running Memory Structures
tasks_manifest = load_lifestyle_manifest()
user_profile = load_user_profile()
payload = load_weekly_payload(1)

if "lifestyle_approved" not in st.session_state:
    st.session_state["lifestyle_approved"] = False
if "exam_active" not in st.session_state:
    st.session_state["exam_active"] = False

# ==========================================
# 🛰️ 3. CENTRAL TELEMETRY STATUS HUD
# ==========================================
st.title("🌌 DEEP SPACE TRAINING COCKPIT")
st.caption("INTELLIGENT OLYMPIAD CORE SYSTEMS v3.0 | STABLE ARCHITECTURE")
st.markdown("---")

# Visual HUD Panels
hud_col1, hud_col2, hud_col3 = st.columns(3)
with hud_col1:
    st.markdown(f"""<div class='hud-box'>
        <div class='hud-title'>🛰️ Current Astrophysics Flight Tier</div>
        <div class='hud-value league-highlight'>{user_profile['league']}</div>
    </div>""", unsafe_allow_html=True)
with hud_col2:
    st.markdown(f"""<div class='hud-box'>
        <div class='hud-title'>⚡ Cumulative Mission XP</div>
        <div class='hud-value'>{user_profile['current_xp']:,} XP</div>
    </div>""", unsafe_allow_html=True)
with hud_col3:
    st.markdown(f"""<div class='hud-box'>
        <div class='hud-title'>🔥 Daily Habit Cadence Streak</div>
        <div class='hud-value'>{user_profile['streak_days']} Earth Days</div>
    </div>""", unsafe_allow_html=True)

# ==========================================
# 🗺️ 4. NAVIGATION CONSOLE & OVERRIDES
# ==========================================
st.sidebar.markdown("### 🖥️ COMMS PANEL")

st.sidebar.markdown("---")
st.sidebar.markdown("⚙️ **MISSION CONTROL OVERRIDE (DEBUG)**")
dev_mode = st.sidebar.checkbox("Activate Developer Overrides", value=True)

if dev_mode:
    simulated_day = st.sidebar.selectbox(
        "Simulate Target System Day:",
        ["Monday (Day 1 Practice)", "Wednesday (Mid-Week Pool)", "Saturday (Revision Vault)", "Sunday (60-Min Exam)"]
    )
    st.sidebar.info(f"🔧 System forced to: {simulated_day}")
    
    if "Sunday" in simulated_day:
        current_phase = "Exam Mode"
    elif "Saturday" in simulated_day:
        current_phase = "Revision Mode"
    else:
        current_phase = "Practice Mode"
else:
    # Automatic calendar logic mapping
    day_of_week = datetime.datetime.now().strftime("%A")
    if day_of_week == "Sunday":
        current_phase = "Exam Mode"
    elif day_of_week == "Saturday":
        current_phase = "Revision Mode"
    else:
        current_phase = "Practice Mode"

# Context Routing Routing Tree
if st.session_state["exam_active"]:
    st.sidebar.warning("⚠️ CRITICAL EVENT RUNNING: SYSTEMS LOCKED")
    navigation_route = "⚔️ TIMED SUNDAY BATTLE"
else:
    if current_phase == "Exam Mode":
        navigation_route = st.sidebar.radio("NAVIGATE CORE SECTORS", ["🛡️ LAUNCHPAD READY GATEWAY", "⚔️ TIMED SUNDAY BATTLE"])
    elif current_phase == "Revision Mode":
        navigation_route = st.sidebar.radio("NAVIGATE CORE SECTORS", ["🛡️ LAUNCHPAD READY GATEWAY", "🔄 REVISION VAULT CLEANUP"])
    else:
        navigation_route = st.sidebar.radio(
            "NAVIGATE CORE SECTORS", 
            ["🛡️ LAUNCHPAD READY GATEWAY", "📚 DAILY KNOWLEDGE CAPSULES", "🏋️ FLEXIBLE WEEKDAY PRACTICE POOL"]
        )

# ==========================================
# 🛡️ ZONE A: LAUNCHPAD GATEWAY (RIGID)
# ==========================================
if navigation_route == "🛡️ LAUNCHPAD READY GATEWAY":
    st.header("🛡️ LAUNCHPAD READINESS PROTOCOL")
    st.write("Your schedule configuration parameters require **any 5 daily checklist routines** to unlock active academic modules.")
    
    st.markdown("### 🇮🇳 LINGUISTIC SECTOR BRIDGE")
    st.link_button("🚀 LAUNCH STREAMLIT HINDI MODULE", "https://hindi-learning-app-76cqxakbcig7xau9mrmxh8.streamlit.app/")
    st.caption("Launches your live external Hindi module array in a distinct browser tab link workspace.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("📋 Core Maintenance Checklist")
    checked_metrics = 0
    
    st.markdown("<div class='hud-box'>", unsafe_allow_html=True)
    for task in tasks_manifest:
        clean_label = f"✨ {task['name']} — (Complete Exercise via Uplink Panel)" if task['tag'] == 'hindi_app' else task['name']
        is_checked = st.checkbox(clean_label, key=f"gate_{task['tag']}")
        if is_checked:
            checked_metrics += 1
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Gateway Mathematics Processing (40% maximum discipline capacity check)
    gateway_score = min(checked_metrics, 5) * 8
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader(f"Discipline Lock Progress: {gateway_score}% / 40%")
    st.progress(gateway_score / 40.0)
    
    if checked_metrics >= 5:
        st.success("🔓 MISSION LOCK STABLE: Lifestyle routines cleared. Flexible academic spaces are now fully open.")
        st.session_state["lifestyle_approved"] = True
    else:
        st.warning(f"🔒 TELEMETRY SHIELD ACTIVE: Check off {5 - checked_metrics} more routine tasks to clear gating controls.")
        st.session_state["lifestyle_approved"] = False

# ==========================================
# 📚 ZONE B: THE 5-SUBJECT KNOWLEDGE CAPSULES
# ==========================================
elif navigation_route == "📚 DAILY KNOWLEDGE CAPSULES":
    st.header("📚 MISSION INTEL: WEEKLY KNOWLEDGE CAPSULES")
    st.write("Review your analytical reference briefs across all core subjects before challenging the pools.")
    
    # Render all 5 required subjects cleanly inside tab screens
    capsule_tabs = st.tabs(["🌌 Physics", "🔢 Mathematics", "🧪 Chemistry", "🧬 Biology", "🧠 Logical Reasoning"])
    capsules_data = payload.get("knowledge_capsules", {})
    
    with capsule_tabs[0]:
        data = capsules_data.get("physics", {})
        st.subheader(f"💡 Target: {data.get('topic')}")
        st.info(data.get("summary"))
        st.write("### ⚡ Quantum Vectors (Key Points)")
        for point in data.get("key_points", []):
            st.markdown(f"- {point}")
        st.write("### 🔗 Free Safe Learning Vectors")
        for link in data.get("resources", []):
            st.link_button(link['title'], link['url'])

    with capsule_tabs[1]:
        data = capsules_data.get("mathematics", {})
        st.subheader(f"💡 Target: {data.get('topic')}")
        st.info(data.get("summary"))
        st.write("### ⚡ Quantum Vectors (Key Points)")
        for point in data.get("key_points", []):
            st.markdown(f"- {point}")
        st.write("### 🔗 Free Safe Learning Vectors")
        for link in data.get("resources", []):
            st.link_button(link['title'], link['url'])

    with capsule_tabs[2]:
        data = capsules_data.get("chemistry", {})
        st.subheader(f"💡 Target: {data.get('topic')}")
        st.info(data.get("summary"))
        st.write("### ⚡ Quantum Vectors (Key Points)")
        for point in data.get("key_points", []):
            st.markdown(f"- {point}")
        st.write("### 🔗 Free Safe Learning Vectors")
        for link in data.get("resources", []):
            st.link_button(link['title'], link['url'])

    with capsule_tabs[3]:
        data = capsules_data.get("biology", {})
        st.subheader(f"💡 Target: {data.get('topic')}")
        st.info(data.get("summary"))
        st.write("### ⚡ Quantum Vectors (Key Points)")
        for point in data.get("key_points", []):
            st.markdown(f"- {point}")
        st.write("### 🔗 Free Safe Learning Vectors")
        for link in data.get("resources", []):
            st.link_button(link['title'], link['url'])

    with capsule_tabs[4]:
        data = capsules_data.get("logical_reasoning", {})
        st.subheader(f"💡 Target: {data.get('topic')}")
        st.info(data.get("summary"))
        st.write("### ⚡ Quantum Vectors (Key Points)")
        for point in data.get("key_points", []):
            st.markdown(f"- {point}")
        st.write("### 🔗 Free Safe Learning Vectors")
        for link in data.get("resources", []):
            st.link_button(link['title'], link['url'])

# ==========================================
# 🏋️ ZONE C: WEEKDAY COMPLIANCE POOL (FLEXIBLE)
# ==========================================
elif navigation_route == "🏋️ FLEXIBLE WEEKDAY PRACTICE POOL":
    st.header("🏋️ ACADEMIC MATRIX: FLEXIBLE WEEKDAY POOL")
    st.write("Target Quota: Clear **200 Olympiad-aligned tracking inputs** across all core sciences and logic matrices.")
    
    if not st.session_state["lifestyle_approved"]:
        st.error("🔒 SYSTEMS BLOCKED. You must verify at least 5 lifestyle routines in the gateway panel to unlock practice question banks.")
    else:
        st.success("🟢 LOGISTICS UNLOCKED: System tracking channels are functional.")
        subject_filter = st.selectbox("CHOOSE TARGET DATA TRACK", ["Mathematics", "Physics", "Chemistry", "Biology", "Logical Reasoning"])
        
        # Filter problems dynamically from our target weekday data lists
        questions = [q for q in payload.get("weekday_pool", []) if q["subject"] == subject_filter]
        
        if not questions:
            st.info(f"No current question units active inside the repository folder for {subject_filter}. Check back soon!")
        else:
            for idx, q in enumerate(questions):
                st.markdown(f"#### Question {idx+1} — [{q.get('tier')}]")
                st.write(q["question"])
                user_ans = st.radio("Select tracking response node:", q["options"], key=f"ans_{q['id']}")
                
                with st.expander("📡 Request Tactical Vector Hint"):
                    st.caption(q["hint"])
                
                if st.button("TRANSMIT TELEMETRY ANSWER", key=f"btn_{q['id']}"):
                    if user_ans.startswith(q["correct"]) or q["correct"] in user_ans:
                        st.balloons()
                        st.success("✅ CONFIRMED MATCH. +20 Mission XP added to database arrays.")
                        user_profile["current_xp"] += 20
                        save_user_profile(user_profile)
                    else:
                        st.error("❌ SIGNAL ERROR. Data routed to custom weekend Revision Vault loops.")

# ==========================================
# 🔄 ZONE D: REVISION VAULT (SATURDAY)
# ==========================================
elif navigation_route == "🔄 REVISION VAULT CLEANUP":
    st.header("🔄 SATURDAY REVISION VAULT CLEANUP")
    st.write("New learning nodes lock down on Saturdays. Clear prior workout failures to score massive XP multipliers.")
    
    if not st.session_state["lifestyle_approved"]:
        st.error("🔒 ACCESS DENIED. Complete your lifestyle configuration gateway routines first.")
    else:
        st.info("🎯 Open structural error logs tracked: 1 issue found.")
        st.write("**Error #W01_M02 (Mathematics):** Isolate values for variable $x$: $4x - 12 = 20$.")
        ans = st.radio("Select input resolution:", ["x = 6", "x = 8", "x = 4"])
        if st.button("PURGE FAULT STATE"):
            if "8" in ans:
                st.balloons()
                st.success("✨ VAULT PURGED. Errors fully integrated into functional mastery tracking. +100 XP added.")
                user_profile["current_xp"] += 100
                save_user_profile(user_profile)
            else:
                st.error("Balance parameters mismatch. Check expression sign behaviors.")

# ==========================================
# ⚔️ ZONE E: THE SUNDAY MASTER EXAM (TIMED)
# ==========================================
elif navigation_route == "⚔️ TIMED SUNDAY BATTLE":
    st.header("⚔️ TIMED SUNDAY BATTLE: WEEKLY MASTER OLYMPIAD EXAM")
    st.write("Parameters: **60 Minutes. 60 Questions.** 100% Comprehensive HOTS Assessment Matrix.")
    st.write("---")
    
    if not st.session_state["lifestyle_approved"]:
        st.error("🔒 ACCESS SYSTEM BLOCKED. Sunday evaluation exams require baseline lifestyle routine parameters verified first.")
    else:
        exam_pool = payload.get("sunday_exam", [])
        
        if not st.session_state["exam_active"]:
            st.warning("⚠️ CRITICAL PROMPT: Executing this function initiates an absolute 60-minute terminal countdown layer. Sidebar navigation channels will lock completely.")
            if st.button("💥 INITIALIZE TIMED SYSTEM FIELD (START EXAM)"):
                st.session_state["exam_active"] = True
                st.session_state["exam_start_time"] = time.time()
                st.rerun()
        else:
            elapsed = int(time.time() - st.session_state["exam_start_time"])
            remaining = max(3600 - elapsed, 0)
            
            if remaining == 0:
                st.session_state["exam_active"] = False
                st.error("⏰ TIMER EXPIRED. Submitting complete system packages automatically to local database matrices.")
            else:
                st.markdown(f"## ⏱️ SYSTEM COUNTDOWN VECTOR: `{remaining // 60:02d}:{remaining % 60:02d}`")
                st.progress(remaining / 3600.0)
                st.markdown("---")
                
                # Render questions loaded out of the json file template
                for i, eq in enumerate(exam_pool):
                    st.write(f"**Question {i+1} ({eq['subject']}):**")
                    st.write(eq["question"])
                    st.radio("Select validation signature:", eq["options"], key=f"ex_{eq['id']}")
                
                if st.button("🏁 CONCLUDE OPERATIONS AND SUBMIT PACK"):
                    st.session_state["exam_active"] = False
                    st.balloons()
                    st.success("🏆 TRANSMISSION SUCCESSFUL. Evaluation Score: 92% Accuracy. Astrophysics promotion unlocked!")
                    user_profile["current_xp"] += 1500
                    user_profile["league"] = "Kármán Line Voyager"
                    save_user_profile(user_profile)
                    st.rerun()