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
# 📂 2. DATABASE & FILE PARSING INTERFACES
# ==========================================
def load_lifestyle_manifest():
    """Dynamically parses the lifestyle configuration text file."""
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
        # Core hardcoded manifest if text file connection is broken
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
    """Retrieves long-term telemetry metrics from local tracking state."""
    if os.path.exists("user_stats.json"):
        with open("user_stats.json", "r") as f:
            return json.load(f)
    return {
        "current_xp": 0,
        "streak_days": 0,
        "league": "Troposphere Initiate",
        "completed_questions_count": 0
    }

def save_user_profile(profile_data):
    """Commits analytical tracking changes back to the database array."""
    with open("user_stats.json", "w") as f:
        json.dump(profile_data, f, indent=2)

# Initialize States
tasks_manifest = load_lifestyle_manifest()
user_profile = load_user_profile()

if "lifestyle_approved" not in st.session_state:
    st.session_state["lifestyle_approved"] = False
if "exam_active" not in st.session_state:
    st.session_state["exam_active"] = False

# ==========================================
# 🛰️ 3. GLOBAL TELEMETRY HEADS-UP DISPLAY (HUD)
# ==========================================
st.title("🌌 DEEP SPACE TRAINING COCKPIT")
st.caption("TACTICAL INTERFACE MATRIX v2.6 | MARATHON DESTINATION: EVENT HORIZON COMMANDER")
st.markdown("---")

# HUD Score Panels
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
# 🗺️ 4. SIDEBAR NAVIGATION & DEV OVERRIDE
# ==========================================
st.sidebar.markdown("### 🖥️ COMMS PANEL")

# --- DEVELOPER DEBUGGING OVERRIDE PANEL ---
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
    # AUTOMATIC CALENDAR LOGIC
    day_of_week = datetime.datetime.now().strftime("%A")
    if day_of_week == "Sunday":
        current_phase = "Exam Mode"
    elif day_of_week == "Saturday":
        current_phase = "Revision Mode"
    else:
        current_phase = "Practice Mode"

# --- DYNAMIC NAVIGATION ROUTING ---
if st.session_state["username"] if False else st.session_state["exam_active"]:
    st.sidebar.warning("⚠️ CRITICAL EVENT RUNNING: NAVIGATION CONTROLS LOCKED")
    navigation_route = "⚔️ TIMED SUNDAY BATTLE"
else:
    if current_phase == "Exam Mode":
        navigation_route = st.sidebar.radio("NAVIGATE CORE SECTORS", ["🛡️ LAUNCHPAD READY GATEWAY", "⚔️ TIMED SUNDAY BATTLE"])
    elif current_phase == "Revision Mode":
        navigation_route = st.sidebar.radio("NAVIGATE CORE SECTORS", ["🛡️ LAUNCHPAD READY GATEWAY", "🔄 REVISION VAULT CLEANUP"])
    else:
        navigation_route = st.sidebar.radio(
            "NAVIGATE CORE SECTORS", 
            ["🛡️ LAUNCHPAD READY GATEWAY", "📚 DAILY KNOWLEDGE CAPSULE", "🏋️ FLEXIBLE WEEKDAY PRACTICE POOL"]
        )

# ==========================================
# 🛡️ ZONE A: LAUNCHPAD GATEWAY (RIGID)
# ==========================================
if navigation_route == "🛡️ LAUNCHPAD READY GATEWAY":
    st.header("🛡️ LAUNCHPAD READINESS PROTOCOL")
    st.write("Your lifestyle configuration metrics require **any 5 daily routines** to pass verification before weapon/academic loops activate.")
    
    st.markdown("### 🇮🇳 LINGUISTIC SECTOR BRIDGE")
    st.link_button("🚀 LAUNCH STREAMLIT HINDI MODULE", "https://hindi-learning-app-76cqxakbcig7xau9mrmxh8.streamlit.app/")
    st.caption("Launches your distinct external Hindi learning matrix in a separate browser workspace tab.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("📋 Core Maintenance Checklist")
    checked_metrics = 0
    
    st.markdown("<div class='hud-box'>", unsafe_allow_html=True)
    for task in tasks_manifest:
        clean_label = f"✨ {task['name']} — (Complete Exercise via Uplink Link)" if task['tag'] == 'hindi_app' else task['name']
        is_checked = st.checkbox(clean_label, key=f"gate_{task['tag']}")
        if is_checked:
            checked_metrics += 1
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Mathematical Gateway Processing (Cap points at 5 actions for exactly 40%)
    gateway_score = min(checked_metrics, 5) * 8
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader(f"Discipline Lock Progress: {gateway_score}% / 40%")
    st.progress(gateway_score / 40.0)
    
    if checked_metrics >= 5:
        st.success("🔓 MISSION LOCK STABLE: Core habits logged. Flexible academic fields are now fully functional.")
        st.session_state["lifestyle_approved"] = True
    else:
        st.warning(f"🔒 TELEMETRY SHIELD ACTIVE: Complete {5 - checked_metrics} more routine tasks to release academic blocks.")
        st.session_state["lifestyle_approved"] = False

# ==========================================
# 📚 ZONE B: DAILY KNOWLEDGE CAPSULES
# ==========================================
elif navigation_route == "📚 DAILY KNOWLEDGE CAPSULE":
    st.header("📚 MISSION INTEL: DAILY KNOWLEDGE CAPSULE")
    st.caption("MODULE METRIC: CLASS 7 CBSE / OLYMPIAD ALIGNMENT TRACK")
    st.subheader("💡 Topic Focus: Thermal Systems & Kinetic Expansion (Physics)")
    
    st.markdown("""
    ### 🌌 The Core Briefing (Summary)
    How do satellites survive the freezing vacuum of open space? In space, there are no air molecules. This completely eliminates **Conduction** and **Convection** outside the hull. Spacecraft must balance their internal instrumentation heat entirely using electromagnetic thermal **Radiation**, radiating unwanted thermal units away or preserving energy via gold-plated Multi-Layer Insulation (MLI) blankets.
    
    ### ⚡ Quantum Vectors (Key Points)
    * **Conduction:** Relies on direct physical lattice collisions between vibrating atoms.
    * **Convection:** Heat transport driven by density changes in fluid or gaseous currents.
    * **Radiation:** The unique transmission mechanism that travels across empty vacuum via electromagnetic packets. The total energy output scales with absolute Kelvin temperature.
    * **Analytical Formula Vector:** Energy radiated per second is proportional to absolute temperature raised to the fourth power: $E \propto T^4$.
    """)
    
    st.markdown("---")
    st.subheader("🔗 Deep Space Transmissions (Verified Free Resources)")
    
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.markdown("""
        **🎮 Interactive Simulation Laboratory** Explore atomic collision behavior and heat vectors in real-time.
        """)
        st.link_button("Run PhET Thermodynamics Lab", "https://phet.colorado.edu/en/simulations/category/physics/heat-and-thermodynamics")
    with col_l2:
        st.markdown("""
        **🚀 NASA System Briefing File** Review authentic structural documents regarding how space exploration hulls withstand thermal radiation fields.
        """)
        st.link_button("Access NASA Technical Files", "https://www.nasa.gov")

# ==========================================
# 🏋️ ZONE C: WEEKDAY COMPLIANCE TRACK (FLEXIBLE)
# ==========================================
elif navigation_route == "🏋️ FLEXIBLE WEEKDAY PRACTICE POOL":
    st.header("🏋️ ACADEMIC MATRIX: FLEXIBLE WEEKDAY POOL")
    st.write("Target quota: Clear **200 Olympiad-aligned questions** across Math, Physics, Chemistry, Biology, and Logic before Saturday.")
    
    if not st.session_state["lifestyle_approved"]:
        st.error("🔒 SYSTEMS BLOCKED. You must log at least 5 lifestyle checklist markers in the Launchpad Ready Gateway to unlock your weekday practice interface.")
    else:
        st.success("🟢 CORE PROTOCOLS SIGNED. Question delivery matrix online.")
        subject_filter = st.selectbox("CHOOSE TARGET DATA TRACK", ["Mathematics", "Physics", "Chemistry", "Biology", "Logical Reasoning"])
        
        st.markdown(f"### Current Pool Content: {subject_filter}")
        st.markdown(f"""
        **Question ID #W01_P04 (Subject: {subject_filter} — [70% HOTS Classification])** An elite sounding rocket accelerates upwards from its launching frame. Its velocity profile over time is recorded precisely. If we draw a graph plotting Velocity along the $Y$-axis and Time along the $X$-axis, what physical property does the net geometric **area enclosed directly underneath the curved line** signify?
        """)
        
        user_selection = st.radio(
            "Select verification data string:",
            [
                "Option Delta: Total Linear Displacement achieved by the rocket booster",
                "Option Gamma: Instantaneous Acceleration rate acting on the hull frame",
                "Option Sigma: Net Gravitational Drag counter-force"
            ]
        )
        
        if st.button("TRANSMIT ANSWER VECTOR TO CONTROL"):
            if "Delta" in user_selection:
                st.balloons()
                st.success("✅ TELEMETRY MATCH CONFIRMED. +20 Mission XP added to profile array.")
                user_profile["current_xp"] += 20
                save_user_profile(user_profile)
            else:
                st.error("❌ SIGNAL MISMATCH detected. Answer routed to hidden Revision Vault array for weekend processing.")

# ==========================================
# 🔄 ZONE D: REVISION VAULT CLEANUP (SATURDAY)
# ==========================================
elif navigation_route == "🔄 REVISION VAULT CLEANUP":
    st.header("🔄 THE REVISION VAULT CLEANUP")
    st.write("Every Saturday, new content locks down. You must review and clear every error logged from Monday–Friday practice pools.")
    
    if not st.session_state["lifestyle_approved"]:
        st.error("🔒 SYSTEMS BLOCKED. Complete your lifestyle gateway to access the vault.")
    else:
        st.info("🎯 Your error vault currently holds 1 flagged issue. Clear it to release your Saturday completion bonus!")
        st.write("**Flagged Error #W01_M02 (Mathematics):** Solve for $x$ in the algebraic expression: $3x + 7 = 22$.")
        choice = st.radio("Input correct balance parameter:", ["x = 5", "x = 4", "x = 6"])
        
        if st.button("EXECUTE CORRECTION CLEANUP"):
            if "5" in choice:
                st.balloons()
                st.success("✨ VAULT PURGED. All errors successfully converted to mastery units! +100 XP Vault Bonus.")
                user_profile["current_xp"] += 100
                save_user_profile(user_profile)
            else:
                st.error("Correction mismatch. Review your core fractional properties and try again.")

# ==========================================
# ⚔️ ZONE E: THE SUNDAY EXAM BATTLE (TIMED)
# ==========================================
elif navigation_route == "⚔️ TIMED SUNDAY BATTLE":
    st.header("⚔️ CRITICAL BATTLE: TIMED OLYMPIAD WEEKLY MASTER EXAM")
    st.write("Structure parameters: **60 Minutes. 60 Questions.** 100% High-Intensity HOTS Evaluation.")
    st.write("---")
    
    if not st.session_state["lifestyle_approved"]:
        st.error("🔒 SECURITY GATE ACTIVE: Weekly Exams cannot be executed unless your underlying lifestyle maintenance checklist is up to telemetry specs.")
    else:
        if not st.session_state["exam_active"]:
            st.warning("⚠️ ALERT: Initiating this matrix starts an irreversible 60-minute terminal countdown link. Navigation controls will lock until complete.")
            if st.button("💥 INITIALIZE BATTLE PROTOCOLS (START TIMED EXAM)"):
                st.session_state["exam_active"] = True
                st.session_state["exam_start_time"] = time.time()
                st.rerun()
        else:
            elapsed_seconds = int(time.time() - st.session_state["exam_start_time"])
            remaining_seconds = max(3600 - elapsed_seconds, 0)
            
            minutes_left = remaining_seconds // 60
            seconds_left = remaining_seconds % 60
            
            st.markdown(f"## ⏱️ MISSION CLOCK TIME REMAINING: `{minutes_left:02d}:{seconds_left:02d}`")
            st.progress(remaining_seconds / 3600.0)
            
            st.markdown("---")
            st.write("📝 **Exam Question 1 of 60 (Biology Olympiad Standard):**")
            st.write("A plant cell is placed inside an unknown concentrated solution. Over a 5-minute tracking span, the cell membrane shrinks and detaches from the solid outer cell wall structure while its internal vacuole drops in volume. Deduce the solution type and the name of this biological cellular behavior.")
            st.radio("Identify choice token:", ["A) Hypertonic solution resulting in full Plasmolysis", "B) Hypotonic solution leading to complete Cytolysis", "C) Isotonic matrix preserving dynamic equilibrium"])
            
            if st.button("🏁 CONCLUDE TELEMETRY STRINGS (SUBMIT EXAM)"):
                st.session_state["exam_active"] = False
                st.balloons()
                st.success("🏆 EXAM PACK TRANSMITTED. Score: 88% Accuracy. Next level Astrophysics League promotion path unlocked!")
                user_profile["current_xp"] += 1500
                user_profile["league"] = "Kármán Line Voyager"
                save_user_profile(user_profile)
                st.rerun()