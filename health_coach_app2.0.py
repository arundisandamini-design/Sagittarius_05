"""
╔══════════════════════════════════════════════════════════╗
║           VitaCoach — AI Health Coach App v4             ║
║  FIXED in v4:                                            ║
║   • Fixed getattr crash on session_state                 ║
║   • Fixed st.rerun() inside form causing errors          ║
║   • Fixed duplicate XP awards                            ║
║   • Fixed check_challenge attribute lookup               ║
║   • Fixed ask_coach history pollution                     ║
║   • Fixed medication time parsing crash                  ║
║   • Fixed BMI division-by-zero guard                     ║
║   • Fixed level index out-of-range                       ║
║   • Fixed pending_reward cleared too early               ║
║   • Fixed daily reset triggering on first load           ║
╚══════════════════════════════════════════════════════════╝

Install:
    pip install streamlit anthropic

Run:
    streamlit run health_coach_app.py
"""

import streamlit as st
import anthropic
import datetime
import math
import random

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VitaCoach – AI Health Coach",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'DM Serif Display', serif; }
.main { background-color: #f5f9f5; }
header { visibility: hidden; }

.vita-card {
    background: white; border-radius: 16px;
    padding: 1.4rem; box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 1rem;
}
.onboard-wrap {
    max-width: 640px; margin: 1.5rem auto;
    background: white; border-radius: 24px;
    padding: 2.5rem 2.8rem; box-shadow: 0 4px 32px rgba(0,0,0,0.08);
}
.xp-bar-wrap {
    background: rgba(255,255,255,0.18); border-radius: 999px;
    height: 10px; margin: 6px 0 2px; overflow: hidden;
}
.xp-bar-fill {
    height: 100%; border-radius: 999px;
    background: linear-gradient(90deg, #a5d6a7, #ffffff);
    transition: width 0.6s ease;
}
.level-label { font-size: 0.75rem; letter-spacing: 0.04em; opacity: 0.85; margin-bottom: 2px; }

.badge-grid { display: flex; flex-wrap: wrap; gap: 10px; margin: 0.6rem 0; }
.badge-pill {
    border-radius: 999px; padding: 5px 14px;
    font-size: 0.82rem; font-weight: 600;
    display: inline-flex; align-items: center; gap: 5px;
}
.badge-earned { background: #fff8e1; color: #e65100; border: 1.5px solid #ffcc80; }
.badge-locked { background: #f5f5f5; color: #bbb; border: 1.5px solid #e0e0e0; }

.reward-toast {
    background: linear-gradient(135deg, #e8f5e9, #f0fff4);
    border-left: 4px solid #4caf50; border-radius: 12px;
    padding: 1rem 1.3rem; margin: 0.6rem 0;
    box-shadow: 0 2px 12px rgba(76,175,80,0.15);
}
.challenge-card {
    background: linear-gradient(135deg, #1b5e20, #2e7d32);
    color: white; border-radius: 16px; padding: 1.2rem 1.5rem;
    margin-bottom: 1rem; box-shadow: 0 4px 18px rgba(46,125,50,0.25);
}
.challenge-card h4 { margin: 0 0 0.3rem; font-size: 1rem; }
.challenge-card p  { margin: 0; font-size: 0.88rem; opacity: 0.88; }

.streak-pill {
    display: inline-flex; align-items: center; gap: 5px;
    background: #fff3e0; color: #e65100;
    border-radius: 999px; padding: 4px 14px;
    font-weight: 600; font-size: 0.82rem;
    border: 1.5px solid #ffcc80;
}
.stat-row { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 1rem; }
.stat-box {
    flex: 1; min-width: 88px; background: #f1f8f1;
    border-radius: 12px; padding: 0.8rem 1rem; text-align: center;
}
.stat-box .val { font-size: 1.25rem; font-weight: 700; color: #2e7d32; }
.stat-box .lbl { font-size: 0.7rem; color: #777; margin-top: 2px; }

.bmi-badge { display: inline-block; border-radius: 999px; padding: 3px 14px; font-weight: 600; font-size: 0.82rem; }
.bmi-underweight { background:#dbeafe; color:#1e40af; }
.bmi-normal      { background:#d1fae5; color:#065f46; }
.bmi-overweight  { background:#fef3c7; color:#92400e; }
.bmi-obese       { background:#fee2e2; color:#991b1b; }

.user-bubble {
    background: #e8f5e9; border-radius: 16px 16px 4px 16px;
    padding: 0.8rem 1.1rem; margin: 0.4rem 0;
    max-width: 80%; margin-left: auto; font-size: 0.95rem;
}
.coach-bubble {
    background: white; border-left: 3px solid #4caf50;
    border-radius: 4px 16px 16px 16px; padding: 0.8rem 1.1rem;
    margin: 0.4rem 0; max-width: 88%; font-size: 0.95rem;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
}
.drop { font-size: 1.8rem; }
.empty { filter: grayscale(1) opacity(0.28); }

[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #1b5e20 0%, #2e7d32 60%, #388e3c 100%);
}
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebar"] label { color: #c8e6c9 !important; font-size: 0.83rem; }

.stButton > button {
    border-radius: 999px; background: #2e7d32; color: white;
    border: none; padding: 0.45rem 1.4rem; font-weight: 500;
}
.stButton > button:hover { background: #1b5e20; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ════════════════════════════════════════════════════════════════════════════
LEVELS = [
    (0,    "🌱 Seedling",     100),
    (100,  "🌿 Sprout",       250),
    (250,  "🌳 Grower",       500),
    (500,  "💪 Vitalist",     900),
    (900,  "⚡ Energiser",   1400),
    (1400, "🔥 Igniter",     2000),
    (2000, "🏅 Champion",    3000),
    (3000, "🌟 Elite",       5000),
    (5000, "🦁 Master",      8000),
    (8000, "👑 Grandmaster", 99999),
]

BADGES = [
    ("💧", "Hydration Hero",   "Drink your full water goal in a day",     "water_goal_hit"),
    ("🥗", "Meal Planner",     "Generate your first meal plan",            "meal_plan_done"),
    ("🧘", "Zen Seeker",       "Complete your first meditation session",    "meditation_done"),
    ("💪", "Workout Warrior",  "Generate your first workout plan",          "workout_done"),
    ("💊", "Med Master",       "Mark all medications taken in a day",       "all_meds_taken"),
    ("📊", "BMI Tracker",      "Log your BMI for the first time",           "bmi_logged"),
    ("💬", "Chatterbox",       "Send 10 messages to VitaCoach",             "chat_10"),
    ("🔥", "7-Day Streak",     "Use the app 7 days in a row",               "streak_7"),
    ("🌟", "Centurion",        "Earn 500 XP total",                         "xp_500"),
    ("🏆", "VitaCoach Legend", "Earn 2000 XP total",                        "xp_2000"),
    ("🌅", "Early Bird",       "Open the app before 8 AM",                  "early_bird"),
    ("🎯", "Goal Getter",      "Complete 5 daily challenges",               "challenges_5"),
]

DAILY_CHALLENGES = [
    ("💧", "Drink 3 glasses of water before noon.",           "water_count",       3),
    ("🧘", "Do a 5-minute meditation session.",               "meditation_done",   True),
    ("💬", "Ask VitaCoach for a healthy tip.",                "chat_count",        1),
    ("💊", "Mark all your medications as taken today.",       "all_meds_taken_today", True),
    ("📊", "Check your BMI and log it.",                      "bmi_logged_today",  True),
    ("🥗", "Generate a meal plan.",                          "meal_plan_done",    True),
    ("💪", "Generate a workout plan.",                       "workout_done",      True),
    ("💧", "Hit your full daily water goal.",                 "water_goal_hit_today", True),
]

XP_REWARDS = {
    "chat":         10,
    "water_glass":   5,
    "water_goal":   50,
    "meal_plan":    30,
    "meditation":   25,
    "workout":      30,
    "bmi_log":      20,
    "med_taken":    15,
    "all_meds":     40,
    "challenge":    60,
    "daily_login":  20,
    "streak_bonus": 10,
}

COMPLIMENTS = {
    "chat":       ["Great question! 🌟", "You're so curious — that's the key to growth! 💡",
                   "Love your dedication! 🧠", "You're doing amazing, keep asking! 🙌"],
    "water":      ["Hydration hero! 💧", "Your cells are dancing with joy! 🎉",
                   "One sip at a time! ✨", "Body goals: staying hydrated! 💦"],
    "water_goal": ["WATER GOAL SMASHED! 🏆", "You're a hydration champion! 💧🥇",
                   "Your future self is so proud of you! 🌟"],
    "meal_plan":  ["Nutrition genius alert! 🥗", "Treating your body like a temple! ✨",
                   "That meal plan will fuel your best days! 🔥"],
    "meditation": ["Inner peace unlocked! 🧘", "You gave your mind the gift of calm! 🌸",
                   "That mindfulness session was pure self-love! 💚"],
    "workout":    ["Beast mode: ON! 💪", "Your body will thank you! 🏋️",
                   "Strongest version of you — coming up! 🔥"],
    "bmi":        ["Data-driven health — smart move! 📊", "Tracking is the first step! 🎯",
                   "Knowledge is power and you've got plenty! 🌟"],
    "med":        ["Consistency is your superpower! 💊", "Your health routine is rock solid! 🏆",
                   "Taking care of yourself — true strength! 💪"],
    "streak":     ["STREAK ON FIRE! 🔥", "Consistency is your superpower! ⚡",
                   "Every day you show up is a win! 🏅"],
    "login":      ["Welcome back, champion! 🌿", "Another day to be amazing! ✨",
                   "So glad you're here — let's make today count! 🌟"],
    "level_up":   ["LEVEL UP!! You're unstoppable! 🚀🎉", "NEW LEVEL — you're incredible! 🏆✨",
                   "Look at you go — the glow-up is real! 🌟🔥"],
    "challenge":  ["DAILY CHALLENGE CRUSHED! 🎯🏆", "You showed up and delivered — legend! 💪🌟",
                   "Challenge complete — you're on a different level! 🔥"],
}

QUOTES = [
    '"The groundwork of all happiness is health." — Leigh Hunt',
    '"Take care of your body. It\'s the only place you have to live." — Jim Rohn',
    '"A healthy outside starts from the inside." — Robert Urich',
    '"Your body can stand almost anything. It\'s your mind you have to convince."',
    '"Health is not valued until sickness comes." — Thomas Fuller',
]

# ════════════════════════════════════════════════════════════════════════════
# SESSION STATE  — all keys initialised here so nothing ever KeyErrors
# ════════════════════════════════════════════════════════════════════════════
def _init_state():
    defaults = {
        "profile_complete":      False,
        "user_name":             "",
        "user_age":              25,
        "user_gender":           "Male",
        "user_height":           170.0,
        "user_weight":           70.0,
        "user_goal":             "General wellness",
        "user_activity":         "Moderately active",
        "api_key":               "",
        "messages":              [],
        "water_count":           0,
        "water_date":            "",          # blank so first-launch resets correctly
        "bmi_history":           [],
        "medications":           [],
        "xp":                    0,
        "badges_earned":         [],
        "streak":                0,
        "last_login_date":       "",
        "chat_count":            0,
        "challenges_done":       0,
        "daily_challenge_date":  "",
        "daily_challenge_done":  False,
        "daily_challenge_idx":   0,
        "pending_reward":        None,
        "bmi_logged_today":      False,
        "meal_plan_done":        False,
        "meditation_done":       False,
        "workout_done":          False,
        "all_meds_taken_today":  False,
        "water_goal_hit_today":  False,
        "early_bird_checked":    False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()

# ─── Helpers (defined BEFORE daily-reset block so they're available) ─────────
def _ss(key, default=0):
    """Safe session-state getter — avoids getattr pitfalls."""
    return st.session_state.get(key, default)

def bmi_value() -> float:
    h = st.session_state.user_height / 100
    if h <= 0:
        return 0.0
    return round(st.session_state.user_weight / (h ** 2), 1)

def bmi_category(bmi: float):
    if bmi <= 0:    return "Unknown", "bmi-normal"
    if bmi < 18.5:  return "Underweight", "bmi-underweight"
    elif bmi < 25:  return "Normal weight", "bmi-normal"
    elif bmi < 30:  return "Overweight", "bmi-overweight"
    else:           return "Obese", "bmi-obese"

def daily_water_goal() -> int:
    glasses = math.ceil((st.session_state.user_weight * 35) / 250)
    return max(6, min(glasses, 14))

def bmr_calc() -> float:
    w = st.session_state.user_weight
    h = st.session_state.user_height
    a = st.session_state.user_age
    if st.session_state.user_gender == "Male":
        return 10 * w + 6.25 * h - 5 * a + 5
    return 10 * w + 6.25 * h - 5 * a - 161

def get_level(xp: int):
    current = LEVELS[0]
    for lvl in LEVELS:
        if xp >= lvl[0]:
            current = lvl
        else:
            break
    return current

def xp_progress_pct(xp: int) -> float:
    lvl = get_level(xp)
    idx = LEVELS.index(lvl)
    if idx + 1 >= len(LEVELS):
        return 100.0
    nxt  = LEVELS[idx + 1]
    span = nxt[0] - lvl[0]
    if span <= 0:
        return 100.0
    return min(((xp - lvl[0]) / span) * 100, 100)

def award_xp(amount: int, compliment_key: str, badge_key: str = None):
    """Award XP, optionally unlock badge, queue reward toast."""
    old_level  = get_level(st.session_state.xp)
    st.session_state.xp += amount
    new_level  = get_level(st.session_state.xp)
    leveled_up = new_level[0] != old_level[0]

    new_badge = None
    # Explicit badge
    if badge_key and badge_key not in st.session_state.badges_earned:
        st.session_state.badges_earned.append(badge_key)
        new_badge = badge_key
    # XP milestone badges
    for threshold, key in [(500, "xp_500"), (2000, "xp_2000")]:
        if st.session_state.xp >= threshold and key not in st.session_state.badges_earned:
            st.session_state.badges_earned.append(key)
            new_badge = new_badge or key
    # Streak badge
    if st.session_state.streak >= 7 and "streak_7" not in st.session_state.badges_earned:
        st.session_state.badges_earned.append("streak_7")
        new_badge = new_badge or "streak_7"

    pool = COMPLIMENTS.get(compliment_key, ["Great job! 🌟"])
    msg  = random.choice(COMPLIMENTS["level_up"] if leveled_up else pool)
    if leveled_up:
        msg += f" **You reached {new_level[1]}!**"

    badge_info = ""
    if new_badge:
        b = next((x for x in BADGES if x[3] == new_badge), None)
        if b:
            badge_info = f" 🏅 New badge: **{b[0]} {b[1]}**!"

    st.session_state.pending_reward = {
        "xp":         amount,
        "msg":        f"{msg} **+{amount} XP**{badge_info}",
        "badge":      new_badge,
        "level_up":   leveled_up,
        "level_name": new_level[1] if leveled_up else None,
    }

def show_reward():
    """Render and then clear the pending reward toast."""
    r = st.session_state.get("pending_reward")
    if not r:
        return
    icon = "🎊" if r.get("level_up") else ("🏅" if r.get("badge") else "✨")
    st.markdown(
        f'<div class="reward-toast">'
        f'<span style="font-size:1.3rem">{icon}</span> {r["msg"]}'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.session_state.pending_reward = None

def check_challenge(trigger_key: str):
    """Complete today's challenge if its trigger key is now satisfied."""
    if st.session_state.daily_challenge_done:
        return
    ch = DAILY_CHALLENGES[st.session_state.daily_challenge_idx]
    if ch[2] != trigger_key:
        return
    # Read current value safely
    current = st.session_state.get(trigger_key, 0)
    threshold = ch[3]
    if isinstance(threshold, bool):
        met = bool(current) == threshold
    else:
        met = (current if isinstance(current, (int, float)) else 0) >= threshold
    if met:
        st.session_state.daily_challenge_done = True
        st.session_state.challenges_done += 1
        badge = "challenges_5" if st.session_state.challenges_done >= 5 else None
        award_xp(XP_REWARDS["challenge"], "challenge", badge)

def profile_context() -> str:
    bmi = bmi_value()
    cat, _ = bmi_category(bmi)
    return (
        f"Name: {st.session_state.user_name}, Age: {st.session_state.user_age}, "
        f"Gender: {st.session_state.user_gender}, Height: {st.session_state.user_height} cm, "
        f"Weight: {st.session_state.user_weight} kg, BMI: {bmi} ({cat}), "
        f"Activity: {st.session_state.get('user_activity', 'Moderately active')}, "
        f"Goal: {st.session_state.user_goal}. Personalise all advice to this profile."
    )

def build_system_prompt() -> str:
    return (
        "You are VitaCoach, a warm, motivating, empathetic AI health coach. "
        "Expertise: nutrition, meal plans, meditation, stress relief, workouts, "
        "hydration, sleep, BMI, and medication adherence.\n\n"
        "User profile — " + profile_context() + "\n\n"
        "Tone: uplifting, science-backed, concise, encouraging. "
        "Always end your response with one short motivating sentence personalised to the user. "
        "Never diagnose; recommend a doctor for medical issues."
    )

def ask_coach(user_msg: str, include_history: bool = False) -> str:
    """
    Call Claude as VitaCoach.
    include_history=True  → used only for the Chat page (multi-turn).
    include_history=False → one-shot calls from other pages.
    """
    client = anthropic.Anthropic(api_key=st.session_state.api_key)
    if include_history:
        history = [{"role": m["role"], "content": m["content"]}
                   for m in st.session_state.messages]
        history.append({"role": "user", "content": user_msg})
    else:
        history = [{"role": "user", "content": user_msg}]

    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=build_system_prompt(),
        messages=history,
    ) as stream:
        return stream.get_final_text()

# ─── Daily reset & login bonus ────────────────────────────────────────────────
today = str(datetime.date.today())

# Reset daily flags when date changes (also handles first launch when water_date=="")
if st.session_state.water_date != today:
    st.session_state.water_date            = today
    st.session_state.water_count           = 0
    st.session_state.bmi_logged_today      = False
    st.session_state.meal_plan_done        = False
    st.session_state.meditation_done       = False
    st.session_state.workout_done          = False
    st.session_state.all_meds_taken_today  = False
    st.session_state.water_goal_hit_today  = False
    for med in st.session_state.medications:
        med["taken"] = False

# Daily login XP & streak (only after profile is set up)
if st.session_state.profile_complete and st.session_state.last_login_date != today:
    yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
    if st.session_state.last_login_date == yesterday:
        st.session_state.streak += 1
    else:
        st.session_state.streak = 1
    st.session_state.last_login_date       = today
    st.session_state.daily_challenge_date  = today
    st.session_state.daily_challenge_done  = False
    st.session_state.daily_challenge_idx   = abs(hash(today)) % len(DAILY_CHALLENGES)

    bonus = XP_REWARDS["daily_login"]
    if st.session_state.streak > 1:
        bonus += XP_REWARDS["streak_bonus"] * min(st.session_state.streak, 7)
    pool = COMPLIMENTS["streak"] if st.session_state.streak >= 3 else COMPLIMENTS["login"]
    compliment = random.choice(pool)
    st.session_state.pending_reward = {
        "xp":       bonus,
        "msg":      f"{compliment} **+{bonus} XP** for showing up today! 🌿",
        "badge":    None,
        "level_up": False,
    }
    st.session_state.xp += bonus

# Early-bird badge
if (st.session_state.profile_complete
        and not st.session_state.early_bird_checked
        and datetime.datetime.now().hour < 8):
    st.session_state.early_bird_checked = True
    if "early_bird" not in st.session_state.badges_earned:
        st.session_state.badges_earned.append("early_bird")

# ════════════════════════════════════════════════════════════════════════════
# ONBOARDING
# ════════════════════════════════════════════════════════════════════════════
if not st.session_state.profile_complete:
    st.markdown("""
    <div style='text-align:center;padding:2rem 0 0.5rem'>
        <span style='font-size:3.5rem'>🌿</span>
        <h1 style='margin:0;color:#2e7d32'>VitaCoach</h1>
        <p style='color:#888;margin-top:0.2rem'>Your personalised AI health companion</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="onboard-wrap">', unsafe_allow_html=True)
    st.markdown("### 👋 Welcome! Let's set up your profile")
    st.markdown("We use your details to personalise every tip, plan, and recommendation.")
    st.divider()

    st.markdown("**🪪 About You**")
    col1, col2 = st.columns(2)
    with col1:
        name   = st.text_input("Full name *", placeholder="e.g. Alex Johnson")
    with col2:
        gender = st.selectbox("Gender *", ["Male", "Female", "Other / Prefer not to say"])

    st.markdown("**📏 Body Stats**")
    col1, col2, col3 = st.columns(3)
    with col1:
        age    = st.number_input("Age *", 10, 100, 25)
    with col2:
        height = st.number_input("Height (cm) *", 100.0, 250.0, 170.0, 0.5)
    with col3:
        weight = st.number_input("Weight (kg) *", 30.0, 300.0, 70.0, 0.5)

    if height > 0 and weight > 0:
        pb = round(weight / ((height / 100) ** 2), 1)
        pc, pcs = bmi_category(pb)
        st.markdown(
            f'<p style="color:#555;font-size:0.88rem">📊 BMI preview: '
            f'<strong>{pb}</strong> <span class="bmi-badge {pcs}">{pc}</span></p>',
            unsafe_allow_html=True,
        )

    st.markdown("**🎯 Your Goals**")
    col1, col2 = st.columns(2)
    with col1:
        goal = st.selectbox("Primary health goal *", [
            "General wellness", "Weight loss", "Muscle gain",
            "Improve fitness", "Stress management", "Better sleep",
            "Manage a health condition", "Increase energy levels",
        ])
    with col2:
        activity = st.select_slider("Activity level", [
            "Sedentary", "Lightly active", "Moderately active", "Very active", "Athlete",
        ], value="Moderately active")

    st.markdown("**🔑 API Access**")
    api_key = st.text_input(
        "Anthropic API Key *", type="password",
        placeholder="sk-ant-… (get yours at console.anthropic.com)",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Start my health journey 🚀", use_container_width=True):
        if not name.strip():
            st.error("Please enter your name.")
        elif not api_key.strip():
            st.error("Please enter your Anthropic API key.")
        else:
            bv = round(float(weight) / ((float(height) / 100) ** 2), 1)
            cv, _ = bmi_category(bv)
            st.session_state.update({
                "profile_complete": True,
                "user_name":        name.strip(),
                "user_age":         int(age),
                "user_gender":      gender,
                "user_height":      float(height),
                "user_weight":      float(weight),
                "user_goal":        goal,
                "user_activity":    activity,
                "api_key":          api_key.strip(),
            })
            st.session_state.bmi_history.append({"date": today, "bmi": bv, "category": cv})
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ════════════════════════════════════════════════════════════════════════════
WATER_GOAL    = daily_water_goal()
current_level = get_level(st.session_state.xp)
xp_pct        = xp_progress_pct(st.session_state.xp)

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 VitaCoach")
    g_icon = "👨" if st.session_state.user_gender == "Male" else \
             "👩" if st.session_state.user_gender == "Female" else "🧑"

    st.markdown(f"""
    <div style='background:rgba(255,255,255,0.12);border-radius:14px;
                padding:0.9rem 1rem;margin-bottom:0.5rem'>
        <div style='font-size:1.1rem;font-weight:600'>{g_icon} {st.session_state.user_name}</div>
        <div class='level-label'>{current_level[1]}</div>
        <div class='xp-bar-wrap'>
            <div class='xp-bar-fill' style='width:{xp_pct:.0f}%'></div>
        </div>
        <div style='font-size:0.72rem;opacity:0.75'>
            {st.session_state.xp} XP · {len(st.session_state.badges_earned)} badges
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.streak > 0:
        st.markdown(
            f'<div style="margin-bottom:0.6rem">'
            f'<span class="streak-pill">🔥 {st.session_state.streak}-day streak</span></div>',
            unsafe_allow_html=True,
        )

    bmi_s = bmi_value()
    bcat, _ = bmi_category(bmi_s)
    st.markdown(f"""
    <div style='font-size:0.82rem;line-height:2;opacity:0.9'>
        <b>Age:</b> {st.session_state.user_age} &nbsp;|&nbsp; {st.session_state.user_gender}<br>
        <b>Height:</b> {st.session_state.user_height} cm &nbsp;|&nbsp;
        <b>Weight:</b> {st.session_state.user_weight} kg<br>
        <b>BMI:</b> {bmi_s} · {bcat}<br>
        <b>Goal:</b> {st.session_state.user_goal}
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    page = st.radio("Navigate", [
        "🏠 Dashboard", "💬 Chat", "🥗 Meal Plan", "🧘 Meditation",
        "🏋️ Workout", "💧 Water Tracker",
        "📊 BMI Tracker", "💊 Medications", "👤 My Profile",
    ], label_visibility="collapsed")

    st.divider()
    if st.button("🔄 Edit Profile"):
        st.session_state.profile_complete = False
        st.rerun()
    st.caption("Not a substitute for medical advice.")

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("# 🌿 VitaCoach")
tod_h = datetime.datetime.now().hour
greeting = "Good morning" if tod_h < 12 else "Good afternoon" if tod_h < 17 else "Good evening"
st.markdown(f"**{greeting}, {st.session_state.user_name}! 👋** You're doing great — keep it up!")
show_reward()
st.divider()

# ════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
if page == "🏠 Dashboard":
    st.subheader("🏠 Your Dashboard")

    # Level card
    lvl_idx   = LEVELS.index(current_level)
    next_lvl  = LEVELS[min(lvl_idx + 1, len(LEVELS) - 1)]
    xp_needed = max(next_lvl[0] - st.session_state.xp, 0)
    st.markdown(f"""
    <div class='vita-card' style='border-left:4px solid #4caf50'>
        <div style='display:flex;justify-content:space-between;align-items:center'>
            <div>
                <div style='font-size:1.05rem;font-weight:700'>{current_level[1]}</div>
                <div style='font-size:0.82rem;color:#777'>
                    {st.session_state.xp} XP · {xp_needed} XP to next level
                </div>
            </div>
            <div style='font-size:2rem'>{current_level[1].split()[0]}</div>
        </div>
        <div style='background:#f0f0f0;border-radius:999px;height:10px;margin-top:0.8rem;overflow:hidden'>
            <div style='height:100%;width:{xp_pct:.0f}%;
                        background:linear-gradient(90deg,#81c784,#2e7d32);
                        border-radius:999px'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    taken_meds = sum(1 for m in st.session_state.medications if m.get("taken", False))
    total_meds = len(st.session_state.medications)
    meds_display = f"{taken_meds}/{total_meds}" if total_meds > 0 else "—"
    st.markdown(f"""
    <div class='stat-row'>
        <div class='stat-box'><div class='val'>{st.session_state.xp}</div><div class='lbl'>Total XP</div></div>
        <div class='stat-box'><div class='val'>{st.session_state.streak}🔥</div><div class='lbl'>Day Streak</div></div>
        <div class='stat-box'><div class='val'>{len(st.session_state.badges_earned)}</div><div class='lbl'>Badges</div></div>
        <div class='stat-box'><div class='val'>{st.session_state.water_count}/{WATER_GOAL}</div><div class='lbl'>Glasses today</div></div>
        <div class='stat-box'><div class='val'>{meds_display}</div><div class='lbl'>Meds taken</div></div>
        <div class='stat-box'><div class='val'>{st.session_state.challenges_done}</div><div class='lbl'>Challenges</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Daily challenge
    ch       = DAILY_CHALLENGES[st.session_state.daily_challenge_idx]
    ch_done  = st.session_state.daily_challenge_done
    ch_color = "#4caf50" if ch_done else "#ff9800"
    ch_status = "✅ Completed! +60 XP earned" if ch_done else "📌 Complete this to earn +60 XP"
    st.markdown(f"""
    <div class='challenge-card' style='border:2px solid {ch_color}'>
        <h4>{ch[0]} Today's Challenge</h4>
        <p style='font-size:1rem;font-weight:500;margin:0.3rem 0 0.2rem'>{ch[1]}</p>
        <p style='font-size:0.8rem;opacity:0.75'>{ch_status}</p>
    </div>
    """, unsafe_allow_html=True)

    # Badges
    st.markdown("#### 🏅 Your Badges")
    badge_html = ""
    for b in BADGES:
        earned    = b[3] in st.session_state.badges_earned
        cls       = "badge-earned" if earned else "badge-locked"
        badge_html += f'<span class="badge-pill {cls}" title="{b[2]}">{b[0]} {b[1]}</span>'
    st.markdown(f'<div class="badge-grid">{badge_html}</div>', unsafe_allow_html=True)
    if not st.session_state.badges_earned:
        st.caption("Complete actions across the app to earn your first badge!")

    # Quote
    st.markdown(f"""
    <div class='vita-card' style='text-align:center;padding:1.2rem'>
        <span style='font-size:1.5rem'>💭</span>
        <p style='color:#555;font-style:italic;margin:0.5rem 0 0'>{random.choice(QUOTES)}</p>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# CHAT
# ════════════════════════════════════════════════════════════════════════════
elif page == "💬 Chat":
    st.subheader("💬 Chat with VitaCoach")
    st.caption(
        f"{st.session_state.user_name} · {st.session_state.user_age}y · "
        f"{st.session_state.user_height}cm · {st.session_state.user_weight}kg · "
        f"{st.session_state.user_goal}"
    )

    quick = {
        "💪 Workout":   "Build me a personalised workout plan based on my profile.",
        "🥗 Meal plan": "Create a healthy 7-day meal plan suited to my profile and goal.",
        "🧘 Meditate":  "Teach me a quick stress-relief meditation I can do right now.",
        "💧 Water tip": "Give me a fun trick to drink more water daily.",
        "😴 Sleep":     "Give me personalised sleep improvement tips.",
    }
    cols = st.columns(len(quick))
    for col, (lbl, prompt) in zip(cols, quick.items()):
        if col.button(lbl):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

    # Render history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-bubble">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="coach-bubble">🌿 {msg["content"]}</div>', unsafe_allow_html=True)

    # Auto-reply if last message is user
    if (st.session_state.messages
            and st.session_state.messages[-1]["role"] == "user"):
        with st.spinner("VitaCoach is thinking…"):
            try:
                reply = ask_coach(
                    st.session_state.messages[-1]["content"],
                    include_history=True,
                )
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.session_state.chat_count += 1
                badge = "chat_10" if st.session_state.chat_count >= 10 else None
                award_xp(XP_REWARDS["chat"], "chat", badge)
                check_challenge("chat_count")
            except Exception as e:
                st.error(f"API error: {e}")
        st.rerun()

    # Input form
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Ask anything…", label_visibility="collapsed",
            placeholder="e.g. What should I eat after a workout?",
        )
        submitted = st.form_submit_button("Send 🌿")

    if submitted and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})
        st.rerun()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# MEAL PLAN
# ════════════════════════════════════════════════════════════════════════════
elif page == "🥗 Meal Plan":
    st.subheader("🥗 Personalised Meal Plan")

    est_kcal = int(bmr_calc() * 1.4)
    col1, col2, col3 = st.columns(3)
    with col1:
        diet     = st.selectbox("Diet type", ["Balanced", "Vegetarian", "Vegan",
                                               "Keto", "Mediterranean", "Low-carb", "High-protein"])
    with col2:
        duration = st.selectbox("Duration", ["1 day", "3 days", "7 days"])
    with col3:
        calories = st.number_input("Calories/day", 1200, 4000, est_kcal, 50,
                                   help="Pre-filled from your BMR estimate")

    extra = st.text_input("Allergies or restrictions",
                          placeholder="e.g. gluten-free, nut allergy")

    if st.button("Generate Meal Plan 🥦"):
        prompt = (
            f"Create a detailed {duration} {diet} meal plan (~{calories} kcal/day). "
            f"{'Restrictions: ' + extra + '. ' if extra else ''}"
            "Include breakfast, lunch, dinner, and snacks with ingredients and prep notes. "
            "Tailor to my age, gender, weight, and goal."
        )
        with st.spinner("Crafting your meal plan…"):
            try:
                reply = ask_coach(prompt)
                st.markdown(f'<div class="vita-card">{reply}</div>', unsafe_allow_html=True)
                if not st.session_state.meal_plan_done:
                    st.session_state.meal_plan_done = True
                    award_xp(XP_REWARDS["meal_plan"], "meal_plan", "meal_plan_done")
                    check_challenge("meal_plan_done")
                    show_reward()
            except Exception as e:
                st.error(f"API error: {e}")

# ════════════════════════════════════════════════════════════════════════════
# MEDITATION
# ════════════════════════════════════════════════════════════════════════════
elif page == "🧘 Meditation":
    st.subheader("🧘 Meditation & Stress Control")

    col1, col2 = st.columns(2)
    with col1:
        technique  = st.selectbox("Technique", [
            "Breathing (box breathing)", "Body scan", "Mindfulness",
            "Visualisation", "Progressive muscle relaxation", "Loving-kindness",
        ])
    with col2:
        duration_m = st.selectbox("Duration", ["3 min", "5 min", "10 min", "15 min", "20 min"])

    concern = st.text_input("What are you dealing with?",
                            placeholder="e.g. work anxiety, poor sleep")

    if st.button("Start Meditation 🕯️"):
        prompt = (
            f"Guide me through a {duration_m} {technique} meditation. "
            f"{'I am currently dealing with: ' + concern + '. ' if concern else ''}"
            "Give step-by-step real-time instructions. "
            "Briefly explain the science. Tailor to my profile."
        )
        with st.spinner("Preparing your session…"):
            try:
                reply = ask_coach(prompt)
                st.markdown(f'<div class="vita-card">{reply}</div>', unsafe_allow_html=True)
                if not st.session_state.meditation_done:
                    st.session_state.meditation_done = True
                    award_xp(XP_REWARDS["meditation"], "meditation", "meditation_done")
                    check_challenge("meditation_done")
                    show_reward()
            except Exception as e:
                st.error(f"API error: {e}")

# ════════════════════════════════════════════════════════════════════════════
# WORKOUT
# ════════════════════════════════════════════════════════════════════════════
elif page == "🏋️ Workout":
    st.subheader("🏋️ Personalised Workout Plan")
    st.caption("Age, weight, and gender already factored in.")

    col1, col2, col3 = st.columns(3)
    with col1:
        fitness_level = st.selectbox("Fitness level", ["Beginner", "Intermediate", "Advanced"])
    with col2:
        workout_type  = st.selectbox("Type", ["Strength", "Cardio", "HIIT",
                                               "Yoga/Flexibility", "Weight loss",
                                               "Muscle gain", "Full body"])
    with col3:
        days = st.selectbox("Days/week", [2, 3, 4, 5, 6])

    equipment = st.multiselect("Equipment", [
        "No equipment", "Dumbbells", "Barbell", "Resistance bands",
        "Pull-up bar", "Gym machines", "Kettlebell",
    ])
    wk_goal = st.text_input("Specific goal",
                            placeholder="e.g. lose 5 kg, run 5K, core strength")

    if st.button("Create Workout Plan 💪"):
        eq     = ", ".join(equipment) if equipment else "no equipment"
        prompt = (
            f"Create a {days}-day/week {workout_type} plan for a {fitness_level} using {eq}. "
            f"{'Goal: ' + wk_goal + '. ' if wk_goal else ''}"
            "Include sets, reps, rest, warm-up, and cool-down. "
            "Format as a weekly schedule. Tailor to my profile."
        )
        with st.spinner("Building your plan…"):
            try:
                reply = ask_coach(prompt)
                st.markdown(f'<div class="vita-card">{reply}</div>', unsafe_allow_html=True)
                if not st.session_state.workout_done:
                    st.session_state.workout_done = True
                    award_xp(XP_REWARDS["workout"], "workout", "workout_done")
                    check_challenge("workout_done")
                    show_reward()
            except Exception as e:
                st.error(f"API error: {e}")

# ════════════════════════════════════════════════════════════════════════════
# WATER TRACKER
# ════════════════════════════════════════════════════════════════════════════
elif page == "💧 Water Tracker":
    st.subheader("💧 Daily Water Tracker")
    st.markdown(
        f"Your personalised goal: **{WATER_GOAL} glasses/day** "
        f"({WATER_GOAL * 250} ml) — based on your weight of "
        f"**{st.session_state.user_weight} kg**"
    )

    count     = st.session_state.water_count
    remaining = max(0, WATER_GOAL - count)
    progress  = min(count / WATER_GOAL, 1.0)

    drops_html = "".join(
        f'<span class="drop {"" if i < count else "empty"}">💧</span>'
        for i in range(WATER_GOAL)
    )
    st.markdown(
        f'<div class="vita-card" style="text-align:center">'
        f'<h3>Today\'s intake</h3>{drops_html}'
        f'<p style="margin-top:0.8rem;font-size:1.1rem">'
        f'<strong>{count}</strong> / {WATER_GOAL} glasses</p>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.progress(progress)

    col1, col2, col3 = st.columns(3)

    if col1.button("➕ Add glass"):
        if st.session_state.water_count < WATER_GOAL:
            st.session_state.water_count += 1
            award_xp(XP_REWARDS["water_glass"], "water")
            check_challenge("water_count")
            if (st.session_state.water_count >= WATER_GOAL
                    and not st.session_state.water_goal_hit_today):
                st.session_state.water_goal_hit_today = True
                award_xp(XP_REWARDS["water_goal"], "water_goal", "water_goal_hit")
                check_challenge("water_goal_hit_today")
        st.rerun()

    if col2.button("➖ Remove glass"):
        if st.session_state.water_count > 0:
            st.session_state.water_count -= 1
        st.rerun()

    if col3.button("🔄 Reset"):
        st.session_state.water_count = 0
        st.rerun()

    if   count >= WATER_GOAL: st.success("🎉 Daily water goal smashed! You're a hydration hero!")
    elif remaining == 1:      st.info(f"🌊 Just {remaining} more glass — almost there!")
    else:                     st.info(f"💦 {remaining} more glasses to hit your goal. You've got this!")

    if st.button("💡 Hydration tip"):
        with st.spinner(""):
            try:
                tip = ask_coach(
                    "Give me one creative, fun hydration tip personalised to my weight. Keep it short."
                )
                st.markdown(f'<div class="vita-card">{tip}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"API error: {e}")

# ════════════════════════════════════════════════════════════════════════════
# BMI TRACKER
# ════════════════════════════════════════════════════════════════════════════
elif page == "📊 BMI Tracker":
    st.subheader("📊 BMI Tracker")
    st.caption("Pre-filled from your profile. Update whenever your measurements change.")

    col1, col2, col3 = st.columns(3)
    with col1:
        weight = st.number_input("Weight (kg)", 30.0, 300.0,
                                 float(st.session_state.user_weight), 0.5)
    with col2:
        height = st.number_input("Height (cm)", 100.0, 250.0,
                                 float(st.session_state.user_height), 0.5)
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        calc = st.button("Calculate & Save")

    if calc:
        if height <= 0:
            st.error("Height must be greater than 0.")
        else:
            bmi = round(weight / ((height / 100) ** 2), 1)
            cat, css = bmi_category(bmi)
            st.session_state.user_weight = weight
            st.session_state.user_height = height
            st.session_state.bmi_history.append(
                {"date": today, "bmi": bmi, "category": cat}
            )
            st.markdown(f"""
            <div class='vita-card' style='text-align:center'>
                <h2>Your BMI</h2>
                <div style='font-size:3rem;font-weight:700;color:#2e7d32'>{bmi}</div>
                <span class='bmi-badge {css}'>{cat}</span>
                <p style='margin-top:1rem;color:#555'>
                    Healthy range: <strong>18.5 – 24.9</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)

            with st.spinner("Getting personalised advice…"):
                try:
                    advice = ask_coach(
                        f"My BMI is {bmi} ({cat}), weight {weight} kg, height {height} cm. "
                        "Give me 3 specific, encouraging, actionable tips tailored to my profile."
                    )
                    st.markdown(f'<div class="vita-card">{advice}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"API error: {e}")

            if not st.session_state.bmi_logged_today:
                st.session_state.bmi_logged_today = True
                award_xp(XP_REWARDS["bmi_log"], "bmi", "bmi_logged")
                check_challenge("bmi_logged_today")
                show_reward()

    if st.session_state.bmi_history:
        st.markdown("#### History")
        for entry in reversed(st.session_state.bmi_history[-10:]):
            _, css = bmi_category(entry["bmi"])
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;'
                f'padding:0.5rem 0;border-bottom:1px solid #eee">'
                f'<span>{entry["date"]}</span>'
                f'<strong>{entry["bmi"]}</strong>'
                f'<span class="bmi-badge {css}">{entry["category"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

# ════════════════════════════════════════════════════════════════════════════
# MEDICATIONS
# ════════════════════════════════════════════════════════════════════════════
elif page == "💊 Medications":
    st.subheader("💊 Medication Reminders")

    # Add form — rerun happens OUTSIDE the form via a flag
    add_med_flag = False
    new_med_data = {}

    with st.expander("➕ Add medication",
                     expanded=len(st.session_state.medications) == 0):
        with st.form("med_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                med_name = st.text_input("Name", placeholder="e.g. Vitamin D")
            with col2:
                med_time = st.time_input("Time", datetime.time(8, 0))
            with col3:
                med_dose = st.text_input("Dose", placeholder="e.g. 1 tablet")
            submitted_med = st.form_submit_button("Add Medication")

        # Act AFTER the form closes (outside with-form block)
        if submitted_med and med_name.strip():
            st.session_state.medications.append({
                "name":  med_name.strip(),
                "time":  med_time.strftime("%H:%M:%S"),
                "dose":  med_dose.strip(),
                "taken": False,
            })
            st.rerun()

    now = datetime.datetime.now().time()

    if not st.session_state.medications:
        st.info("No medications added yet. Use the form above.")
    else:
        for i, med in enumerate(st.session_state.medications):
            # Safe time parsing
            try:
                mt = datetime.time.fromisoformat(med["time"])
            except Exception:
                mt = datetime.time(0, 0)

            overdue = not med.get("taken", False) and mt < now
            icon    = "✅" if med.get("taken") else ("⚠️" if overdue else "⏰")
            color   = "#4caf50" if med.get("taken") else ("#f44336" if overdue else "#ff9800")

            st.markdown(f"""
            <div class='vita-card' style='border-left:4px solid {color}'>
                <strong>{icon} {med['name']}</strong>
                {"<span style='color:#888;font-size:0.85rem'> · " + med['dose'] + "</span>"
                  if med.get('dose') else ""}
                <br><span style='color:#888;font-size:0.82rem'>⏱ {med['time']}</span>
                {"<span style='color:#f44336;font-size:0.82rem'> · Overdue!</span>"
                  if overdue else ""}
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3 = st.columns([2, 1, 1])
            with c2:
                lbl = "Mark taken ✅" if not med.get("taken") else "Undo ↩️"
                if st.button(lbl, key=f"tog_{i}"):
                    st.session_state.medications[i]["taken"] = not med.get("taken", False)
                    if st.session_state.medications[i]["taken"]:
                        award_xp(XP_REWARDS["med_taken"], "med")
                        all_taken = all(
                            m.get("taken", False)
                            for m in st.session_state.medications
                        )
                        if all_taken and not st.session_state.all_meds_taken_today:
                            st.session_state.all_meds_taken_today = True
                            award_xp(XP_REWARDS["all_meds"], "med", "all_meds_taken")
                            check_challenge("all_meds_taken_today")
                    st.rerun()
            with c3:
                if st.button("Remove 🗑️", key=f"del_{i}"):
                    st.session_state.medications.pop(i)
                    st.rerun()

    if st.session_state.medications:
        taken = sum(1 for m in st.session_state.medications if m.get("taken", False))
        total = len(st.session_state.medications)
        st.progress(taken / total)
        st.markdown(f"**{taken}/{total}** taken today.")
        if taken == total and total > 0:
            st.success("🎉 All medications taken — you're crushing it! 💊")

    if st.button("💡 Adherence tips"):
        with st.spinner(""):
            try:
                tip = ask_coach(
                    "Give me 3 fun, practical tips to remember taking medications on time."
                )
                st.markdown(f'<div class="vita-card">{tip}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"API error: {e}")

# ════════════════════════════════════════════════════════════════════════════
# MY PROFILE
# ════════════════════════════════════════════════════════════════════════════
elif page == "👤 My Profile":
    st.subheader("👤 My Health Profile")

    bv = bmi_value()
    cat, css = bmi_category(bv)
    st.markdown(f"""
    <div class='stat-row'>
        <div class='stat-box'><div class='val'>{st.session_state.user_age}</div><div class='lbl'>Age</div></div>
        <div class='stat-box'><div class='val'>{st.session_state.user_gender[0]}</div><div class='lbl'>Gender</div></div>
        <div class='stat-box'><div class='val'>{st.session_state.user_height} cm</div><div class='lbl'>Height</div></div>
        <div class='stat-box'><div class='val'>{st.session_state.user_weight} kg</div><div class='lbl'>Weight</div></div>
        <div class='stat-box'>
            <div class='val'>{bv}</div>
            <div class='lbl'>BMI · <span class='bmi-badge {css}'>{cat}</span></div>
        </div>
        <div class='stat-box'><div class='val'>{int(bmr_calc())} kcal</div><div class='lbl'>Est. BMR</div></div>
        <div class='stat-box'><div class='val'>{WATER_GOAL}💧</div><div class='lbl'>Water goal</div></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(
        f"**Goal:** {st.session_state.user_goal} &nbsp;|&nbsp; "
        f"**Activity:** {st.session_state.get('user_activity', '—')}"
    )

    st.divider()
    st.markdown("#### 🏆 Achievements")
    earned = [b for b in BADGES if b[3] in st.session_state.badges_earned]
    if earned:
        html = "".join(
            f'<span class="badge-pill badge-earned">{b[0]} {b[1]}</span>'
            for b in earned
        )
        st.markdown(f'<div class="badge-grid">{html}</div>', unsafe_allow_html=True)
    else:
        st.caption("No badges yet — start using the app to earn them!")

    st.markdown(f"""
    <div class='stat-row' style='margin-top:0.5rem'>
        <div class='stat-box'><div class='val'>{st.session_state.xp}</div><div class='lbl'>Total XP</div></div>
        <div class='stat-box'><div class='val'>{current_level[1]}</div><div class='lbl'>Level</div></div>
        <div class='stat-box'><div class='val'>{st.session_state.streak}🔥</div><div class='lbl'>Streak</div></div>
        <div class='stat-box'><div class='val'>{st.session_state.challenges_done}</div><div class='lbl'>Challenges</div></div>
        <div class='stat-box'><div class='val'>{st.session_state.chat_count}</div><div class='lbl'>Messages</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### ✏️ Edit Profile")

    GOAL_OPTIONS = [
        "General wellness", "Weight loss", "Muscle gain", "Improve fitness",
        "Stress management", "Better sleep", "Manage a health condition",
        "Increase energy levels",
    ]
    GENDER_OPTIONS = ["Male", "Female", "Other / Prefer not to say"]

    with st.form("profile_edit"):
        col1, col2 = st.columns(2)
        with col1:
            nn  = st.text_input("Name", st.session_state.user_name)
            na  = st.number_input("Age", 10, 100, st.session_state.user_age)
            nh  = st.number_input("Height (cm)", 100.0, 250.0,
                                   st.session_state.user_height, 0.5)
        with col2:
            ng  = st.selectbox(
                "Gender", GENDER_OPTIONS,
                index=GENDER_OPTIONS.index(st.session_state.user_gender)
                      if st.session_state.user_gender in GENDER_OPTIONS else 0,
            )
            nw  = st.number_input("Weight (kg)", 30.0, 300.0,
                                   st.session_state.user_weight, 0.5)
            ngl = st.selectbox(
                "Health goal", GOAL_OPTIONS,
                index=GOAL_OPTIONS.index(st.session_state.user_goal)
                      if st.session_state.user_goal in GOAL_OPTIONS else 0,
            )
        if st.form_submit_button("Save changes ✅"):
            st.session_state.update({
                "user_name":   nn,
                "user_age":    int(na),
                "user_gender": ng,
                "user_height": float(nh),
                "user_weight": float(nw),
                "user_goal":   ngl,
            })
            st.success("Profile updated! All advice is now personalised to your new stats. 🌿")
            st.rerun()

    st.divider()
    if st.button("💡 Get my personalised health summary"):
        with st.spinner(""):
            try:
                summary = ask_coach(
                    "Based on my profile, give me a concise personalised health summary: "
                    "current status, top 3 priorities, and one uplifting motivational message."
                )
                st.markdown(f'<div class="vita-card">{summary}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"API error: {e}")

# ─── Footer ──────────────────────────────────────────────────────────────────
st.divider()
st.caption("🌿 VitaCoach · Powered by Claude AI · Not a substitute for professional medical advice.")
