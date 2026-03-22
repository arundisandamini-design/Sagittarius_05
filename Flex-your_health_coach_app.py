"""
╔══════════════════════════════════════════════════════════╗
║           VitaCoach — AI Health Coach App v6             ║
║  100% FREE — No API Key needed at all!                   ║
║  Uses built-in smart health responses                    ║
║                                                          ║
║  Install:  pip install streamlit                         ║
║  Run:      streamlit run health_coach_app.py             ║
╚══════════════════════════════════════════════════════════╝
"""

import streamlit as st
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
    max-width: 640px; margin: 1.5rem auto; background: white;
    border-radius: 24px; padding: 2.5rem 2.8rem;
    box-shadow: 0 4px 32px rgba(0,0,0,0.08);
}
.xp-bar-wrap {
    background: rgba(255,255,255,0.18); border-radius: 999px;
    height: 10px; margin: 6px 0 2px; overflow: hidden;
}
.xp-bar-fill {
    height: 100%; border-radius: 999px;
    background: linear-gradient(90deg, #a5d6a7, #ffffff);
}
.level-label { font-size:0.75rem; letter-spacing:0.04em; opacity:0.85; margin-bottom:2px; }
.badge-grid  { display:flex; flex-wrap:wrap; gap:10px; margin:0.6rem 0; }
.badge-pill  {
    border-radius:999px; padding:5px 14px; font-size:0.82rem; font-weight:600;
    display:inline-flex; align-items:center; gap:5px;
}
.badge-earned { background:#fff8e1; color:#e65100; border:1.5px solid #ffcc80; }
.badge-locked { background:#f5f5f5; color:#bbb;    border:1.5px solid #e0e0e0; }
.reward-toast {
    background: linear-gradient(135deg,#e8f5e9,#f0fff4);
    border-left:4px solid #4caf50; border-radius:12px;
    padding:1rem 1.3rem; margin:0.6rem 0;
    box-shadow:0 2px 12px rgba(76,175,80,0.15);
}
.challenge-card {
    background: linear-gradient(135deg,#1b5e20,#2e7d32);
    color:white; border-radius:16px; padding:1.2rem 1.5rem;
    margin-bottom:1rem; box-shadow:0 4px 18px rgba(46,125,50,0.25);
}
.challenge-card h4 { margin:0 0 0.3rem; font-size:1rem; }
.challenge-card p  { margin:0; font-size:0.88rem; opacity:0.88; }
.streak-pill {
    display:inline-flex; align-items:center; gap:5px;
    background:#fff3e0; color:#e65100; border-radius:999px;
    padding:4px 14px; font-weight:600; font-size:0.82rem;
    border:1.5px solid #ffcc80;
}
.stat-row { display:flex; gap:10px; flex-wrap:wrap; margin-bottom:1rem; }
.stat-box  {
    flex:1; min-width:88px; background:#f1f8f1;
    border-radius:12px; padding:0.8rem 1rem; text-align:center;
}
.stat-box .val { font-size:1.25rem; font-weight:700; color:#2e7d32; }
.stat-box .lbl { font-size:0.7rem; color:#777; margin-top:2px; }
.bmi-badge      { display:inline-block; border-radius:999px; padding:3px 14px; font-weight:600; font-size:0.82rem; }
.bmi-underweight{ background:#dbeafe; color:#1e40af; }
.bmi-normal     { background:#d1fae5; color:#065f46; }
.bmi-overweight { background:#fef3c7; color:#92400e; }
.bmi-obese      { background:#fee2e2; color:#991b1b; }
.user-bubble {
    background:#e8f5e9; border-radius:16px 16px 4px 16px;
    padding:0.8rem 1.1rem; margin:0.4rem 0;
    max-width:80%; margin-left:auto; font-size:0.95rem;
}
.coach-bubble {
    background:white; border-left:3px solid #4caf50;
    border-radius:4px 16px 16px 16px; padding:0.8rem 1.1rem;
    margin:0.4rem 0; max-width:88%; font-size:0.95rem;
    box-shadow:0 1px 6px rgba(0,0,0,0.06);
}
.drop  { font-size:1.8rem; }
.empty { filter:grayscale(1) opacity(0.28); }
[data-testid="stSidebar"] {
    background: linear-gradient(160deg,#1b5e20 0%,#2e7d32 60%,#388e3c 100%);
}
[data-testid="stSidebar"] * { color:white !important; }
[data-testid="stSidebar"] label { color:#c8e6c9 !important; font-size:0.83rem; }
.stButton > button {
    border-radius:999px; background:#2e7d32; color:white;
    border:none; padding:0.45rem 1.4rem; font-weight:500;
}
.stButton > button:hover { background:#1b5e20; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# BUILT-IN SMART RESPONSES  (no API needed)
# ════════════════════════════════════════════════════════════════════════════

def get_response(category: str, profile: dict) -> str:
    """Return a personalised health response based on category and user profile."""
    name   = profile["name"]
    age    = profile["age"]
    gender = profile["gender"]
    weight = profile["weight"]
    height = profile["height"]
    goal   = profile["goal"]
    bmi    = round(weight / ((height / 100) ** 2), 1)

    responses = {

    "meal_plan": f"""
### 🥗 Your Personalised 7-Day Meal Plan, {name}!

Based on your profile ({age}y, {weight}kg, goal: *{goal}*), here's your plan:

**📅 Day 1**
- 🌅 Breakfast: Oatmeal with banana, honey & chia seeds
- 🌞 Lunch: Grilled chicken salad with olive oil dressing
- 🌙 Dinner: Baked salmon with steamed broccoli & brown rice
- 🍎 Snack: Apple with almond butter

**📅 Day 2**
- 🌅 Breakfast: Greek yoghurt with mixed berries & granola
- 🌞 Lunch: Lentil soup with whole grain bread
- 🌙 Dinner: Stir-fried tofu with vegetables & quinoa
- 🍌 Snack: Banana & a handful of walnuts

**📅 Day 3**
- 🌅 Breakfast: Scrambled eggs (2) with spinach & whole grain toast
- 🌞 Lunch: Tuna wrap with lettuce, tomato & avocado
- 🌙 Dinner: Chicken stir-fry with bell peppers & brown rice
- 🥕 Snack: Carrot sticks with hummus

**📅 Day 4**
- 🌅 Breakfast: Smoothie — banana, spinach, almond milk, protein powder
- 🌞 Lunch: Quinoa bowl with chickpeas, cucumber & feta
- 🌙 Dinner: Grilled fish tacos with cabbage slaw & salsa
- 🍊 Snack: Orange & a handful of almonds

**📅 Day 5**
- 🌅 Breakfast: Whole grain pancakes with fresh fruit
- 🌞 Lunch: Turkey & avocado sandwich on whole grain bread
- 🌙 Dinner: Beef & vegetable stew with whole grain roll
- 🫐 Snack: Blueberries & cottage cheese

**📅 Day 6**
- 🌅 Breakfast: Avocado toast with poached egg & cherry tomatoes
- 🌞 Lunch: Black bean soup with whole grain crackers
- 🌙 Dinner: Baked chicken breast with sweet potato & green beans
- 🥜 Snack: Mixed nuts & dried fruit

**📅 Day 7**
- 🌅 Breakfast: Veggie omelette with mushrooms, peppers & onions
- 🌞 Lunch: Greek salad with grilled shrimp & pita bread
- 🌙 Dinner: Homemade vegetable curry with basmati rice
- 🍓 Snack: Strawberries & dark chocolate (2 squares)

> 💡 **Tip for you, {name}:** Aim to eat every 3–4 hours to keep your energy steady. You're doing amazing — keep fuelling that body! 💪
    """,

    "workout": f"""
### 💪 Your Personalised Workout Plan, {name}!

Designed for: {age}y, {gender}, {weight}kg, Goal: *{goal}*

**📋 Weekly Schedule (4 days/week)**

**🏋️ Day 1 — Upper Body Strength**
- Warm-up: 5 min light cardio + arm circles
- Push-ups: 3 × 12 reps
- Dumbbell shoulder press: 3 × 10 reps
- Bent-over rows: 3 × 12 reps
- Bicep curls: 3 × 12 reps
- Tricep dips: 3 × 10 reps
- Cool-down: 5 min stretching

**🦵 Day 2 — Lower Body Strength**
- Warm-up: 5 min brisk walk + leg swings
- Squats: 3 × 15 reps
- Lunges: 3 × 12 reps each leg
- Glute bridges: 3 × 15 reps
- Calf raises: 3 × 20 reps
- Wall sit: 3 × 30 seconds
- Cool-down: 5 min stretching

**🏃 Day 3 — Cardio & Core**
- 20 min brisk walk or jog
- Plank: 3 × 30 seconds
- Crunches: 3 × 15 reps
- Bicycle crunches: 3 × 12 reps each side
- Mountain climbers: 3 × 20 reps
- Cool-down: 5 min walking

**🤸 Day 4 — Full Body & Flexibility**
- 10 min yoga or stretching
- Burpees: 3 × 8 reps
- Jump squats: 3 × 10 reps
- Superman holds: 3 × 10 reps
- Child's pose, downward dog, hip flexor stretch
- Cool-down: 10 min full body stretch

> 💡 **Rest on Days 5–7** — recovery is just as important as training!
> 🌟 You've got this, {name}! Every rep brings you closer to your goal!
    """,

    "meditation": f"""
### 🧘 5-Minute Stress Relief Meditation for You, {name}

Find a quiet spot, sit comfortably, and follow these steps:

**Step 1 — Settle In (30 seconds)**
Sit upright, close your eyes gently. Place both hands on your knees, palms facing up. Let your shoulders drop away from your ears.

**Step 2 — Box Breathing (2 minutes)**
This technique calms your nervous system in minutes:
- 🫁 **Inhale** slowly through your nose for **4 counts**
- ⏸️ **Hold** your breath for **4 counts**
- 💨 **Exhale** slowly through your mouth for **4 counts**
- ⏸️ **Hold** empty for **4 counts**
- Repeat this cycle **6 times**

**Step 3 — Body Scan (1 minute)**
Starting from the top of your head, slowly move your attention down your body. Notice any tension in your jaw, shoulders, chest, stomach, legs. Don't judge — just notice and breathe into each area.

**Step 4 — Gratitude Moment (1 minute)**
Think of 3 things you are grateful for today. They can be tiny — a warm drink, a kind word, your heartbeat. Let yourself feel the warmth of each one.

**Step 5 — Return (30 seconds)**
Take one deep breath in, hold for 3 seconds, then slowly exhale. Gently wiggle your fingers and toes, open your eyes slowly.

> 🌸 **The science:** Box breathing activates your parasympathetic nervous system, reducing cortisol (stress hormone) within minutes.
> 💚 Well done, {name} — you just gave your mind the greatest gift: peace. Do this daily for best results!
    """,

    "bmi_advice": f"""
### 📊 Your BMI Analysis, {name}

**Your BMI: {bmi}**

{"✅ **Great news!** Your BMI is in the healthy range (18.5–24.9). Here's how to maintain it:" if 18.5 <= bmi <= 24.9 else ""}
{"⚠️ Your BMI suggests you are **underweight**. Here's how to reach a healthy weight:" if bmi < 18.5 else ""}
{"📌 Your BMI suggests you are **overweight**. Here are gentle, sustainable steps:" if 25 <= bmi <= 29.9 else ""}
{"💙 Your BMI is in the obese range. Small, consistent changes make a big difference:" if bmi >= 30 else ""}

**🎯 3 Personalised Tips for You:**

**1. Nutrition**
{"Eat plenty of protein (chicken, fish, eggs, legumes) and complex carbs. Avoid skipping meals." if bmi < 18.5 else "Focus on whole foods — vegetables, lean proteins, whole grains. Reduce processed foods and sugary drinks."}

**2. Movement**
{"Start with 20–30 min of walking 4 times a week. Add strength training 2–3 times a week to build muscle." if bmi >= 25 else "Maintain 150 minutes of moderate exercise per week. Mix cardio and strength training."}

**3. Lifestyle**
Sleep 7–9 hours per night. Drink {round(weight * 35 / 1000, 1)} litres of water daily. Manage stress with meditation or deep breathing.

> 💪 Remember, {name} — your BMI is just one number. You are more than a measurement. Every healthy choice you make is a victory! 🌟
    """,

    "hydration": f"""
### 💧 Hydration Tips Personalised for You, {name}

**Your daily water goal: {round(weight * 35 / 1000, 1)} litres ({round(weight * 35 / 250)} glasses)**

**🌟 Top 5 Fun Hydration Tricks:**

**1. The Morning Kick-Start**
Keep a glass of water on your bedside table. Drink it before your feet touch the floor every morning. This jumpstarts your metabolism and rehydrates your body after 8 hours of sleep.

**2. The Habit Stack**
Link water to things you already do: drink a glass before every meal, after every bathroom visit, and every time you check your phone. Before you know it — you're hitting your goal without thinking!

**3. Make It Exciting**
Add slices of lemon, cucumber, mint or berries to your water bottle. Herbal teas count too! When water tastes great, you'll naturally drink more.

**4. The 2-Hour Alarm**
Set a gentle reminder on your phone every 2 hours that says "💧 Time to hydrate, {name}!" Small, consistent sips beat chugging large amounts.

**5. Track Your Drops**
Use the Water Tracker in this app — every glass earns you XP points and gets you closer to the 💧 Hydration Hero badge!

> 🏆 At {weight}kg, your body needs about {round(weight * 35 / 1000, 1)} litres daily. You're already here tracking — that means you care about your health. That's everything! 💙
    """,

    "sleep": f"""
### 😴 Personalised Sleep Guide for {name}

At {age} years old, you need **7–9 hours** of quality sleep per night.

**🌙 Your Evening Routine (Start 1 hour before bed):**

**9:00 PM — Wind Down**
Dim the lights in your home. Bright light signals your brain it's daytime. Switch to warm, dim lighting in the evening.

**9:15 PM — Screen Limit**
Put your phone face down or use night mode. Blue light from screens blocks melatonin (your sleep hormone) for up to 3 hours.

**9:30 PM — Relax Your Body**
Try 5 minutes of gentle stretching or the 4-7-8 breathing technique: inhale 4 seconds, hold 7 seconds, exhale 8 seconds. Repeat 4 times.

**9:45 PM — Prep Your Space**
Keep your bedroom cool (18–20°C is ideal), dark, and quiet. A consistent sleep environment trains your brain to sleep automatically.

**10:00 PM — Sleep Time**
Try to sleep and wake at the same time every day — even weekends. This locks in your body clock.

**☀️ Morning Tip:**
Get 10 minutes of natural sunlight within 1 hour of waking. This resets your circadian rhythm and improves your sleep the *next* night.

> 🌟 Sleep is your superpower, {name}! Quality sleep improves mood, energy, metabolism, and even weight management. You deserve great rest every single night! 💚
    """,

    "stress": f"""
### 🧠 Stress Management Guide for {name}

Stress affects your health, weight, sleep, and energy. Here are science-backed techniques:

**⚡ Instant Relief (Under 2 Minutes)**
- **4-7-8 Breathing:** Inhale 4s → Hold 7s → Exhale 8s. Repeat 3 times.
- **Cold water:** Splash cold water on your face — activates the dive reflex, slowing heart rate immediately.
- **5-4-3-2-1 Grounding:** Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste.

**🌿 Daily Habits (15 Minutes/Day)**
- Morning: 5 min of box breathing before checking your phone
- Afternoon: A 10-min walk outside (nature reduces cortisol by 20%)
- Evening: Write 3 things you're grateful for in a journal

**💪 Weekly Habits**
- Exercise 3–4 times/week (even a 20-min walk counts!)
- Connect with someone you care about — social connection is the #1 stress buffer
- Limit caffeine after 2 PM — it raises cortisol for up to 6 hours

**🚨 Signs You Need Extra Support**
If stress feels overwhelming for more than 2 weeks, please speak to a doctor or mental health professional. There is no shame in asking for help — it's the bravest thing you can do.

> 💚 {name}, you are stronger than your stress. One breath at a time, one day at a time. You've got this! 🌿
    """,

    "general": f"""
### 🌿 Health Tips Personalised for {name}

Welcome! Here are your top health priorities based on your profile:

**🎯 Your Goal: {goal}**

**1. 🥗 Nutrition**
Eat 3 balanced meals and 2 healthy snacks daily. Fill half your plate with vegetables, a quarter with lean protein, and a quarter with whole grains. Avoid skipping meals — it leads to overeating later.

**2. 💧 Hydration**
Your daily target: **{round(weight * 35 / 1000, 1)} litres** ({round(weight * 35 / 250)} glasses). Start every morning with a glass of water before anything else.

**3. 🏃 Movement**
Aim for 30 minutes of moderate activity most days. This doesn't have to be the gym — dancing, walking, cycling, or swimming all count!

**4. 😴 Sleep**
7–9 hours per night is your target. Poor sleep increases hunger hormones by 30% and reduces willpower significantly.

**5. 🧘 Stress**
Practice 5 minutes of deep breathing or meditation daily. Chronic stress raises cortisol, which can lead to weight gain, poor immunity, and fatigue.

**6. 💊 Consistency**
The secret to great health isn't perfection — it's consistency. Small healthy choices, made daily, create extraordinary results over time.

> 🌟 {name}, the fact that you're here and taking steps for your health already puts you ahead of most. Be proud of every small win. You are doing brilliantly! 💚
    """,
    }

    return responses.get(category, responses["general"])


def get_chat_response(user_msg: str, profile: dict) -> str:
    """Return a smart response based on keywords in the user's message."""
    msg = user_msg.lower()
    name = profile["name"]

    if any(w in msg for w in ["meal", "food", "eat", "diet", "nutrition", "recipe", "breakfast", "lunch", "dinner"]):
        return get_response("meal_plan", profile)
    elif any(w in msg for w in ["workout", "exercise", "gym", "training", "fitness", "strength", "cardio"]):
        return get_response("workout", profile)
    elif any(w in msg for w in ["meditat", "calm", "relax", "mindful", "breathe", "breathing", "peace"]):
        return get_response("meditation", profile)
    elif any(w in msg for w in ["stress", "anxiety", "worry", "overwhelm", "pressure", "mental"]):
        return get_response("stress", profile)
    elif any(w in msg for w in ["water", "hydrat", "drink", "thirst"]):
        return get_response("hydration", profile)
    elif any(w in msg for w in ["sleep", "insomnia", "tired", "rest", "fatigue", "energy"]):
        return get_response("sleep", profile)
    elif any(w in msg for w in ["bmi", "weight", "height", "overweight", "underweight"]):
        return get_response("bmi_advice", profile)
    else:
        tips = [
            f"Great question, {name}! 🌟 Here's my advice: focus on the basics first — drink {round(profile['weight'] * 35 / 1000, 1)}L of water daily, sleep 7–9 hours, move your body for 30 minutes, and eat mostly whole foods. These four habits alone will transform your health over time. You're asking the right questions — that's the first step to change! 💚",
            f"Love that you're taking charge of your health, {name}! 💪 Remember: health is built in small, daily decisions — not big dramatic changes. The water you drank today, the walk you took, the meal you cooked — all of it counts. Keep going! 🌿",
            f"That's a thoughtful question, {name}! 🧠 My top tip: don't try to change everything at once. Pick ONE healthy habit this week and do it every single day. Consistency beats perfection every time. What habit will you start today? 🌟",
            f"You're on the right track, {name}! 🎯 Here's a power tip: pair new healthy habits with things you already do. Drink water when you brush your teeth. Stretch while watching TV. Take the stairs instead of the lift. Small changes, massive results over time! 🔥",
        ]
        return random.choice(tips)


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
    ("💧", "Hydration Hero",   "Drink your full water goal in a day",   "water_goal_hit"),
    ("🥗", "Meal Planner",     "Generate your first meal plan",          "meal_plan_done"),
    ("🧘", "Zen Seeker",       "Complete a meditation session",          "meditation_done"),
    ("💪", "Workout Warrior",  "Generate your first workout plan",       "workout_done"),
    ("💊", "Med Master",       "Mark all medications taken in a day",    "all_meds_taken"),
    ("📊", "BMI Tracker",      "Log your BMI",                           "bmi_logged"),
    ("💬", "Chatterbox",       "Send 10 messages to VitaCoach",          "chat_10"),
    ("🔥", "7-Day Streak",     "Use the app 7 days in a row",            "streak_7"),
    ("🌟", "Centurion",        "Earn 500 XP total",                      "xp_500"),
    ("🏆", "VitaCoach Legend", "Earn 2000 XP total",                     "xp_2000"),
    ("🌅", "Early Bird",       "Open the app before 8 AM",               "early_bird"),
    ("🎯", "Goal Getter",      "Complete 5 daily challenges",            "challenges_5"),
]
DAILY_CHALLENGES = [
    ("💧", "Drink 3 glasses of water before noon.",     "water_count",          3),
    ("🧘", "Do a meditation session today.",             "meditation_done",       True),
    ("💬", "Ask VitaCoach for a health tip.",            "chat_count",            1),
    ("💊", "Mark all medications as taken.",             "all_meds_taken_today",  True),
    ("📊", "Log your BMI today.",                        "bmi_logged_today",      True),
    ("🥗", "Generate a meal plan.",                      "meal_plan_done",        True),
    ("💪", "Generate a workout plan.",                   "workout_done",          True),
    ("💧", "Hit your full daily water goal.",            "water_goal_hit_today",  True),
]
XP_REWARDS = {
    "chat": 10, "water_glass": 5, "water_goal": 50,
    "meal_plan": 30, "meditation": 25, "workout": 30,
    "bmi_log": 20, "med_taken": 15, "all_meds": 40,
    "challenge": 60, "daily_login": 20, "streak_bonus": 10,
}
COMPLIMENTS = {
    "chat":       ["Great question! 🌟","You're so curious — that's the key to growth! 💡","You're doing amazing! 🙌"],
    "water":      ["Hydration hero! 💧","Your cells are dancing with joy! 🎉","One sip at a time! ✨"],
    "water_goal": ["WATER GOAL SMASHED! 🏆","You're a hydration champion! 💧🥇","Future you is so proud! 🌟"],
    "meal_plan":  ["Nutrition genius alert! 🥗","Treating your body like a temple! ✨","Fuel your best days! 🔥"],
    "meditation": ["Inner peace unlocked! 🧘","You gave your mind calm! 🌸","Pure self-love! 💚"],
    "workout":    ["Beast mode: ON! 💪","Your body will thank you! 🏋️","Strongest version incoming! 🔥"],
    "bmi":        ["Data-driven health! 📊","Tracking is the first step! 🎯","Knowledge is power! 🌟"],
    "med":        ["Consistency is your superpower! 💊","Rock solid routine! 🏆","True strength! 💪"],
    "streak":     ["STREAK ON FIRE! 🔥","Consistency is your superpower! ⚡","Every day is a win! 🏅"],
    "login":      ["Welcome back, champion! 🌿","Another day to be amazing! ✨","Let's make today count! 🌟"],
    "level_up":   ["LEVEL UP!! Unstoppable! 🚀🎉","NEW LEVEL — incredible! 🏆✨","The glow-up is real! 🌟🔥"],
    "challenge":  ["CHALLENGE CRUSHED! 🎯🏆","You delivered — legend! 💪🌟","Different level! 🔥"],
}
QUOTES = [
    '"The groundwork of all happiness is health." — Leigh Hunt',
    '"Take care of your body. It\'s the only place you have to live." — Jim Rohn',
    '"A healthy outside starts from the inside." — Robert Urich',
    '"Your body can stand almost anything. It\'s your mind you have to convince."',
    '"Health is not valued until sickness comes." — Thomas Fuller',
]
GOAL_OPTIONS   = ["General wellness","Weight loss","Muscle gain","Improve fitness",
                  "Stress management","Better sleep","Manage a health condition","Increase energy levels"]
GENDER_OPTIONS = ["Male","Female","Other / Prefer not to say"]

# ════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ════════════════════════════════════════════════════════════════════════════
def _init_state():
    defaults = {
        "profile_complete":     False,
        "user_name":            "",
        "user_age":             25,
        "user_gender":          "Male",
        "user_height":          170.0,
        "user_weight":          70.0,
        "user_goal":            "General wellness",
        "user_activity":        "Moderately active",
        "messages":             [],
        "water_count":          0,
        "water_date":           "",
        "bmi_history":          [],
        "medications":          [],
        "xp":                   0,
        "badges_earned":        [],
        "streak":               0,
        "last_login_date":      "",
        "chat_count":           0,
        "challenges_done":      0,
        "daily_challenge_date": "",
        "daily_challenge_done": False,
        "daily_challenge_idx":  0,
        "pending_reward":       None,
        "bmi_logged_today":     False,
        "meal_plan_done":       False,
        "meditation_done":      False,
        "workout_done":         False,
        "all_meds_taken_today": False,
        "water_goal_hit_today": False,
        "early_bird_checked":   False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()

# ════════════════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════════════════
def get_profile():
    return {
        "name":   st.session_state.user_name,
        "age":    st.session_state.user_age,
        "gender": st.session_state.user_gender,
        "height": st.session_state.user_height,
        "weight": st.session_state.user_weight,
        "goal":   st.session_state.user_goal,
    }

def bmi_value():
    h = st.session_state.user_height / 100
    return round(st.session_state.user_weight / (h ** 2), 1) if h > 0 else 0.0

def bmi_category(bmi):
    if bmi <= 0:    return "Unknown",       "bmi-normal"
    if bmi < 18.5:  return "Underweight",   "bmi-underweight"
    elif bmi < 25:  return "Normal weight", "bmi-normal"
    elif bmi < 30:  return "Overweight",    "bmi-overweight"
    else:           return "Obese",         "bmi-obese"

def daily_water_goal():
    return max(6, min(math.ceil((st.session_state.user_weight * 35) / 250), 14))

def bmr_calc():
    w, h, a = st.session_state.user_weight, st.session_state.user_height, st.session_state.user_age
    return (10*w+6.25*h-5*a+5) if st.session_state.user_gender=="Male" else (10*w+6.25*h-5*a-161)

def get_level(xp):
    cur = LEVELS[0]
    for lvl in LEVELS:
        if xp >= lvl[0]: cur = lvl
        else: break
    return cur

def xp_progress_pct(xp):
    lvl = get_level(xp); idx = LEVELS.index(lvl)
    if idx+1 >= len(LEVELS): return 100.0
    nxt = LEVELS[idx+1]; span = nxt[0]-lvl[0]
    return min(((xp-lvl[0])/span)*100, 100) if span > 0 else 100.0

def award_xp(amount, compliment_key, badge_key=None):
    old_lvl = get_level(st.session_state.xp)
    st.session_state.xp += amount
    new_lvl = get_level(st.session_state.xp)
    leveled_up = new_lvl[0] != old_lvl[0]
    new_badge = None
    if badge_key and badge_key not in st.session_state.badges_earned:
        st.session_state.badges_earned.append(badge_key); new_badge = badge_key
    for thr, key in [(500,"xp_500"),(2000,"xp_2000")]:
        if st.session_state.xp >= thr and key not in st.session_state.badges_earned:
            st.session_state.badges_earned.append(key); new_badge = new_badge or key
    if st.session_state.streak >= 7 and "streak_7" not in st.session_state.badges_earned:
        st.session_state.badges_earned.append("streak_7"); new_badge = new_badge or "streak_7"
    pool = COMPLIMENTS.get(compliment_key, ["Great job! 🌟"])
    msg  = random.choice(COMPLIMENTS["level_up"] if leveled_up else pool)
    if leveled_up: msg += f" **You reached {new_lvl[1]}!**"
    badge_info = ""
    if new_badge:
        b = next((x for x in BADGES if x[3]==new_badge), None)
        if b: badge_info = f" 🏅 New badge: **{b[0]} {b[1]}**!"
    st.session_state.pending_reward = {
        "xp": amount, "msg": f"{msg} **+{amount} XP**{badge_info}",
        "badge": new_badge, "level_up": leveled_up,
    }

def show_reward():
    r = st.session_state.get("pending_reward")
    if not r: return
    icon = "🎊" if r.get("level_up") else ("🏅" if r.get("badge") else "✨")
    st.markdown(
        f'<div class="reward-toast"><span style="font-size:1.3rem">{icon}</span> {r["msg"]}</div>',
        unsafe_allow_html=True)
    st.session_state.pending_reward = None

def check_challenge(trigger_key):
    if st.session_state.daily_challenge_done: return
    ch = DAILY_CHALLENGES[st.session_state.daily_challenge_idx]
    if ch[2] != trigger_key: return
    current = st.session_state.get(trigger_key, 0)
    threshold = ch[3]
    met = bool(current) if isinstance(threshold, bool) \
          else (current if isinstance(current,(int,float)) else 0) >= threshold
    if met:
        st.session_state.daily_challenge_done = True
        st.session_state.challenges_done += 1
        award_xp(XP_REWARDS["challenge"], "challenge",
                 "challenges_5" if st.session_state.challenges_done >= 5 else None)

# ─── Daily reset & login ─────────────────────────────────────────────────────
today = str(datetime.date.today())

if st.session_state.water_date != today:
    st.session_state.water_date = today
    st.session_state.water_count = 0
    for k in ["bmi_logged_today","meal_plan_done","meditation_done","workout_done",
              "all_meds_taken_today","water_goal_hit_today"]:
        st.session_state[k] = False
    for med in st.session_state.medications:
        med["taken"] = False

if st.session_state.profile_complete and st.session_state.last_login_date != today:
    yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
    st.session_state.streak = (st.session_state.streak+1
                                if st.session_state.last_login_date==yesterday else 1)
    st.session_state.last_login_date = today
    st.session_state.daily_challenge_date = today
    st.session_state.daily_challenge_done = False
    st.session_state.daily_challenge_idx  = abs(hash(today)) % len(DAILY_CHALLENGES)
    bonus = XP_REWARDS["daily_login"]
    if st.session_state.streak > 1:
        bonus += XP_REWARDS["streak_bonus"] * min(st.session_state.streak, 7)
    pool = COMPLIMENTS["streak"] if st.session_state.streak >= 3 else COMPLIMENTS["login"]
    st.session_state.xp += bonus
    st.session_state.pending_reward = {
        "xp": bonus, "msg": f"{random.choice(pool)} **+{bonus} XP** for showing up today! 🌿",
        "badge": None, "level_up": False,
    }

if (st.session_state.profile_complete and not st.session_state.early_bird_checked
        and datetime.datetime.now().hour < 8):
    st.session_state.early_bird_checked = True
    if "early_bird" not in st.session_state.badges_earned:
        st.session_state.badges_earned.append("early_bird")

# ════════════════════════════════════════════════════════════════════════════
# ONBOARDING — only asks Name, Age, Gender, Height, Weight, Goal
# ════════════════════════════════════════════════════════════════════════════
if not st.session_state.profile_complete:
    st.markdown("""
    <div style='text-align:center;padding:2rem 0 0.5rem'>
        <span style='font-size:3.5rem'>🌿</span>
        <h1 style='margin:0;color:#2e7d32'>VitaCoach</h1>
        <p style='color:#888;margin-top:0.2rem'>Your personalised AI health companion — 100% Free!</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="onboard-wrap">', unsafe_allow_html=True)
    st.markdown("### 👋 Welcome! Let's set up your profile")
    st.markdown("Just fill in your details — no account, no payment, no API key needed! 🎉")
    st.divider()

    st.markdown("**🪪 About You**")
    col1, col2 = st.columns(2)
    with col1: name   = st.text_input("Full name *", placeholder="e.g. Alex Johnson")
    with col2: gender = st.selectbox("Gender *", GENDER_OPTIONS)

    st.markdown("**📏 Body Stats**")
    col1, col2, col3 = st.columns(3)
    with col1: age    = st.number_input("Age *", 10, 100, 25)
    with col2: height = st.number_input("Height (cm) *", 100.0, 250.0, 170.0, 0.5)
    with col3: weight = st.number_input("Weight (kg) *", 30.0, 300.0, 70.0, 0.5)

    if height > 0 and weight > 0:
        pb = round(weight / ((height/100)**2), 1)
        pc, pcs = bmi_category(pb)
        st.markdown(
            f'<p style="color:#555;font-size:0.88rem">📊 BMI preview: '
            f'<strong>{pb}</strong> <span class="bmi-badge {pcs}">{pc}</span></p>',
            unsafe_allow_html=True)

    st.markdown("**🎯 Your Goals**")
    col1, col2 = st.columns(2)
    with col1: goal = st.selectbox("Primary health goal *", GOAL_OPTIONS)
    with col2: activity = st.select_slider("Activity level",
        ["Sedentary","Lightly active","Moderately active","Very active","Athlete"],
        value="Moderately active")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Start my health journey 🚀", use_container_width=True):
        if not name.strip():
            st.error("Please enter your name.")
        else:
            bv = round(float(weight)/((float(height)/100)**2), 1)
            cv, _ = bmi_category(bv)
            st.session_state.update({
                "profile_complete": True,
                "user_name": name.strip(), "user_age": int(age),
                "user_gender": gender, "user_height": float(height),
                "user_weight": float(weight), "user_goal": goal,
                "user_activity": activity,
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
profile       = get_profile()

with st.sidebar:
    st.markdown("## 🌿 VitaCoach")
    g_icon = "👨" if st.session_state.user_gender=="Male" else \
             "👩" if st.session_state.user_gender=="Female" else "🧑"
    st.markdown(f"""
    <div style='background:rgba(255,255,255,0.12);border-radius:14px;
                padding:0.9rem 1rem;margin-bottom:0.5rem'>
        <div style='font-size:1.1rem;font-weight:600'>{g_icon} {st.session_state.user_name}</div>
        <div class='level-label'>{current_level[1]}</div>
        <div class='xp-bar-wrap'><div class='xp-bar-fill' style='width:{xp_pct:.0f}%'></div></div>
        <div style='font-size:0.72rem;opacity:0.75'>
            {st.session_state.xp} XP · {len(st.session_state.badges_earned)} badges
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.session_state.streak > 0:
        st.markdown(
            f'<div style="margin-bottom:0.6rem">'
            f'<span class="streak-pill">🔥 {st.session_state.streak}-day streak</span></div>',
            unsafe_allow_html=True)
    bmi_s = bmi_value(); bcat, _ = bmi_category(bmi_s)
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
        "🏠 Dashboard","💬 Chat","🥗 Meal Plan","🧘 Meditation",
        "🏋️ Workout","💧 Water Tracker","📊 BMI Tracker","💊 Medications","👤 My Profile",
    ], label_visibility="collapsed")
    st.divider()
    if st.button("🔄 Edit Profile"):
        st.session_state.profile_complete = False; st.rerun()
    st.caption("Not a substitute for medical advice.")

st.markdown("# 🌿 VitaCoach")
tod_h = datetime.datetime.now().hour
greeting = "Good morning" if tod_h < 12 else "Good afternoon" if tod_h < 17 else "Good evening"
st.markdown(f"**{greeting}, {st.session_state.user_name}! 👋** You're doing great — keep it up!")
show_reward()
st.divider()

# ─── DASHBOARD ───────────────────────────────────────────────────────────────
if page == "🏠 Dashboard":
    st.subheader("🏠 Your Dashboard")
    lvl_idx = LEVELS.index(current_level)
    next_lvl = LEVELS[min(lvl_idx+1, len(LEVELS)-1)]
    xp_needed = max(next_lvl[0] - st.session_state.xp, 0)
    st.markdown(f"""
    <div class='vita-card' style='border-left:4px solid #4caf50'>
        <div style='display:flex;justify-content:space-between;align-items:center'>
            <div>
                <div style='font-size:1.05rem;font-weight:700'>{current_level[1]}</div>
                <div style='font-size:0.82rem;color:#777'>{st.session_state.xp} XP · {xp_needed} XP to next level</div>
            </div>
            <div style='font-size:2rem'>{current_level[1].split()[0]}</div>
        </div>
        <div style='background:#f0f0f0;border-radius:999px;height:10px;margin-top:0.8rem;overflow:hidden'>
            <div style='height:100%;width:{xp_pct:.0f}%;background:linear-gradient(90deg,#81c784,#2e7d32);border-radius:999px'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    taken_meds = sum(1 for m in st.session_state.medications if m.get("taken",False))
    total_meds = len(st.session_state.medications)
    st.markdown(f"""
    <div class='stat-row'>
        <div class='stat-box'><div class='val'>{st.session_state.xp}</div><div class='lbl'>Total XP</div></div>
        <div class='stat-box'><div class='val'>{st.session_state.streak}🔥</div><div class='lbl'>Streak</div></div>
        <div class='stat-box'><div class='val'>{len(st.session_state.badges_earned)}</div><div class='lbl'>Badges</div></div>
        <div class='stat-box'><div class='val'>{st.session_state.water_count}/{WATER_GOAL}</div><div class='lbl'>Water today</div></div>
        <div class='stat-box'><div class='val'>{f"{taken_meds}/{total_meds}" if total_meds else "—"}</div><div class='lbl'>Meds taken</div></div>
        <div class='stat-box'><div class='val'>{st.session_state.challenges_done}</div><div class='lbl'>Challenges</div></div>
    </div>
    """, unsafe_allow_html=True)

    ch = DAILY_CHALLENGES[st.session_state.daily_challenge_idx]
    ch_done = st.session_state.daily_challenge_done
    st.markdown(f"""
    <div class='challenge-card' style='border:2px solid {"#4caf50" if ch_done else "#ff9800"}'>
        <h4>{ch[0]} Today's Challenge</h4>
        <p style='font-size:1rem;font-weight:500;margin:0.3rem 0 0.2rem'>{ch[1]}</p>
        <p style='font-size:0.8rem;opacity:0.75'>{"✅ Completed! +60 XP" if ch_done else "📌 Complete to earn +60 XP"}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 🏅 Your Badges")
    badge_html = "".join(
        f'<span class="badge-pill {"badge-earned" if b[3] in st.session_state.badges_earned else "badge-locked"}" title="{b[2]}">{b[0]} {b[1]}</span>'
        for b in BADGES)
    st.markdown(f'<div class="badge-grid">{badge_html}</div>', unsafe_allow_html=True)
    if not st.session_state.badges_earned:
        st.caption("Complete actions to earn your first badge!")

    st.markdown(f"""
    <div class='vita-card' style='text-align:center;padding:1.2rem'>
        <span style='font-size:1.5rem'>💭</span>
        <p style='color:#555;font-style:italic;margin:0.5rem 0 0'>{random.choice(QUOTES)}</p>
    </div>
    """, unsafe_allow_html=True)

# ─── CHAT ────────────────────────────────────────────────────────────────────
elif page == "💬 Chat":
    st.subheader("💬 Chat with VitaCoach")
    st.caption(f"{st.session_state.user_name} · {st.session_state.user_age}y · {st.session_state.user_height}cm · {st.session_state.user_weight}kg")

    quick = {
        "💪 Workout":   "Create a workout plan for me",
        "🥗 Meal plan": "Give me a 7-day meal plan",
        "🧘 Meditate":  "Teach me a stress relief meditation",
        "💧 Water tip": "Give me hydration tips",
        "😴 Sleep":     "How can I sleep better",
    }
    cols = st.columns(len(quick))
    for col, (lbl, prompt) in zip(cols, quick.items()):
        if col.button(lbl):
            st.session_state.messages.append({"role":"user","content":prompt})
            st.rerun()

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-bubble">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="coach-bubble">🌿 {msg["content"]}</div>', unsafe_allow_html=True)

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.spinner("VitaCoach is thinking…"):
            reply = get_chat_response(st.session_state.messages[-1]["content"], profile)
            st.session_state.messages.append({"role":"assistant","content":reply})
            st.session_state.chat_count += 1
            award_xp(XP_REWARDS["chat"], "chat", "chat_10" if st.session_state.chat_count >= 10 else None)
            check_challenge("chat_count")
        st.rerun()

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Ask anything…", label_visibility="collapsed",
                                   placeholder="e.g. What should I eat after a workout?")
        submitted = st.form_submit_button("Send 🌿")
    if submitted and user_input.strip():
        st.session_state.messages.append({"role":"user","content":user_input.strip()})
        st.rerun()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []; st.rerun()

# ─── MEAL PLAN ────────────────────────────────────────────────────────────────
elif page == "🥗 Meal Plan":
    st.subheader("🥗 Personalised Meal Plan")
    est_kcal = int(bmr_calc() * 1.4)
    col1, col2, col3 = st.columns(3)
    with col1: diet     = st.selectbox("Diet", ["Balanced","Vegetarian","Vegan","Keto","Mediterranean","Low-carb","High-protein"])
    with col2: duration = st.selectbox("Duration", ["1 day","3 days","7 days"])
    with col3: calories = st.number_input("Calories/day", 1200, 4000, est_kcal, 50)
    extra = st.text_input("Allergies or restrictions", placeholder="e.g. gluten-free, nut allergy")

    if st.button("Generate Meal Plan 🥦"):
        with st.spinner("Crafting your meal plan…"):
            reply = get_response("meal_plan", profile)
        st.markdown(f'<div class="vita-card">{reply}</div>', unsafe_allow_html=True)
        if not st.session_state.meal_plan_done:
            st.session_state.meal_plan_done = True
            award_xp(XP_REWARDS["meal_plan"], "meal_plan", "meal_plan_done")
            check_challenge("meal_plan_done")
            show_reward()

# ─── MEDITATION ───────────────────────────────────────────────────────────────
elif page == "🧘 Meditation":
    st.subheader("🧘 Meditation & Stress Control")
    col1, col2 = st.columns(2)
    with col1: technique  = st.selectbox("Technique", ["Breathing (box breathing)","Body scan","Mindfulness","Visualisation","Progressive muscle relaxation","Loving-kindness"])
    with col2: duration_m = st.selectbox("Duration", ["3 min","5 min","10 min","15 min","20 min"])
    concern = st.text_input("What are you dealing with?", placeholder="e.g. work anxiety, poor sleep")

    if st.button("Start Meditation 🕯️"):
        with st.spinner("Preparing your session…"):
            reply = get_response("meditation", profile)
        st.markdown(f'<div class="vita-card">{reply}</div>', unsafe_allow_html=True)
        if not st.session_state.meditation_done:
            st.session_state.meditation_done = True
            award_xp(XP_REWARDS["meditation"], "meditation", "meditation_done")
            check_challenge("meditation_done")
            show_reward()

# ─── WORKOUT ──────────────────────────────────────────────────────────────────
elif page == "🏋️ Workout":
    st.subheader("🏋️ Personalised Workout Plan")
    col1, col2, col3 = st.columns(3)
    with col1: fitness_level = st.selectbox("Level", ["Beginner","Intermediate","Advanced"])
    with col2: workout_type  = st.selectbox("Type",  ["Strength","Cardio","HIIT","Yoga/Flexibility","Weight loss","Muscle gain","Full body"])
    with col3: days          = st.selectbox("Days/week", [2,3,4,5,6])
    equipment = st.multiselect("Equipment", ["No equipment","Dumbbells","Barbell","Resistance bands","Pull-up bar","Gym machines","Kettlebell"])
    wk_goal   = st.text_input("Specific goal", placeholder="e.g. lose 5 kg, run 5K")

    if st.button("Create Workout Plan 💪"):
        with st.spinner("Building your plan…"):
            reply = get_response("workout", profile)
        st.markdown(f'<div class="vita-card">{reply}</div>', unsafe_allow_html=True)
        if not st.session_state.workout_done:
            st.session_state.workout_done = True
            award_xp(XP_REWARDS["workout"], "workout", "workout_done")
            check_challenge("workout_done")
            show_reward()

# ─── WATER TRACKER ────────────────────────────────────────────────────────────
elif page == "💧 Water Tracker":
    st.subheader("💧 Daily Water Tracker")
    st.markdown(f"Goal: **{WATER_GOAL} glasses/day** ({WATER_GOAL*250} ml) — based on your weight of **{st.session_state.user_weight} kg**")
    count    = st.session_state.water_count
    progress = min(count / WATER_GOAL, 1.0)
    drops_html = "".join(f'<span class="drop {"" if i<count else "empty"}">💧</span>' for i in range(WATER_GOAL))
    st.markdown(
        f'<div class="vita-card" style="text-align:center"><h3>Today\'s intake</h3>{drops_html}'
        f'<p style="margin-top:0.8rem;font-size:1.1rem"><strong>{count}</strong> / {WATER_GOAL} glasses</p></div>',
        unsafe_allow_html=True)
    st.progress(progress)

    col1, col2, col3 = st.columns(3)
    if col1.button("➕ Add glass"):
        if st.session_state.water_count < WATER_GOAL:
            st.session_state.water_count += 1
            award_xp(XP_REWARDS["water_glass"], "water")
            check_challenge("water_count")
            if st.session_state.water_count >= WATER_GOAL and not st.session_state.water_goal_hit_today:
                st.session_state.water_goal_hit_today = True
                award_xp(XP_REWARDS["water_goal"], "water_goal", "water_goal_hit")
                check_challenge("water_goal_hit_today")
        st.rerun()
    if col2.button("➖ Remove glass"):
        if st.session_state.water_count > 0: st.session_state.water_count -= 1
        st.rerun()
    if col3.button("🔄 Reset"):
        st.session_state.water_count = 0; st.rerun()

    remaining = max(0, WATER_GOAL - count)
    if   count >= WATER_GOAL: st.success("🎉 Daily water goal smashed! You're a hydration hero!")
    elif remaining == 1:      st.info("🌊 Just 1 more glass — almost there!")
    else:                     st.info(f"💦 {remaining} more glasses to go. You've got this!")

    if st.button("💡 Hydration tip"):
        st.markdown(f'<div class="vita-card">{get_response("hydration", profile)}</div>', unsafe_allow_html=True)

# ─── BMI TRACKER ──────────────────────────────────────────────────────────────
elif page == "📊 BMI Tracker":
    st.subheader("📊 BMI Tracker")
    col1, col2, col3 = st.columns(3)
    with col1: weight = st.number_input("Weight (kg)", 30.0, 300.0, float(st.session_state.user_weight), 0.5)
    with col2: height = st.number_input("Height (cm)", 100.0, 250.0, float(st.session_state.user_height), 0.5)
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        calc = st.button("Calculate & Save")

    if calc and height > 0:
        bmi = round(weight / ((height/100)**2), 1)
        cat, css = bmi_category(bmi)
        st.session_state.user_weight = weight
        st.session_state.user_height = height
        st.session_state.bmi_history.append({"date": today, "bmi": bmi, "category": cat})
        st.markdown(f"""
        <div class='vita-card' style='text-align:center'>
            <h2>Your BMI</h2>
            <div style='font-size:3rem;font-weight:700;color:#2e7d32'>{bmi}</div>
            <span class='bmi-badge {css}'>{cat}</span>
            <p style='margin-top:1rem;color:#555'>Healthy range: <strong>18.5 – 24.9</strong></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="vita-card">{get_response("bmi_advice", profile)}</div>', unsafe_allow_html=True)
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
                f'<div style="display:flex;justify-content:space-between;padding:0.5rem 0;border-bottom:1px solid #eee">'
                f'<span>{entry["date"]}</span><strong>{entry["bmi"]}</strong>'
                f'<span class="bmi-badge {css}">{entry["category"]}</span></div>',
                unsafe_allow_html=True)

# ─── MEDICATIONS ──────────────────────────────────────────────────────────────
elif page == "💊 Medications":
    st.subheader("💊 Medication Reminders")
    with st.expander("➕ Add medication", expanded=len(st.session_state.medications)==0):
        with st.form("med_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1: med_name = st.text_input("Name", placeholder="e.g. Vitamin D")
            with col2: med_time = st.time_input("Time", datetime.time(8,0))
            with col3: med_dose = st.text_input("Dose", placeholder="e.g. 1 tablet")
            submitted_med = st.form_submit_button("Add Medication")
        if submitted_med and med_name.strip():
            st.session_state.medications.append({
                "name": med_name.strip(), "time": med_time.strftime("%H:%M:%S"),
                "dose": med_dose.strip(), "taken": False,
            })
            st.rerun()

    now = datetime.datetime.now().time()
    if not st.session_state.medications:
        st.info("No medications added yet. Use the form above.")
    else:
        for i, med in enumerate(st.session_state.medications):
            try:    mt = datetime.time.fromisoformat(med["time"])
            except: mt = datetime.time(0,0)
            overdue = not med.get("taken",False) and mt < now
            icon  = "✅" if med.get("taken") else ("⚠️" if overdue else "⏰")
            color = "#4caf50" if med.get("taken") else ("#f44336" if overdue else "#ff9800")
            st.markdown(f"""
            <div class='vita-card' style='border-left:4px solid {color}'>
                <strong>{icon} {med['name']}</strong>
                {"<span style='color:#888;font-size:0.85rem'> · "+med['dose']+"</span>" if med.get('dose') else ""}
                <br><span style='color:#888;font-size:0.82rem'>⏱ {med['time']}</span>
                {"<span style='color:#f44336;font-size:0.82rem'> · Overdue!</span>" if overdue else ""}
            </div>
            """, unsafe_allow_html=True)
            c1, c2, c3 = st.columns([2,1,1])
            with c2:
                if st.button("Mark taken ✅" if not med.get("taken") else "Undo ↩️", key=f"tog_{i}"):
                    st.session_state.medications[i]["taken"] = not med.get("taken",False)
                    if st.session_state.medications[i]["taken"]:
                        award_xp(XP_REWARDS["med_taken"], "med")
                        if all(m.get("taken") for m in st.session_state.medications) and not st.session_state.all_meds_taken_today:
                            st.session_state.all_meds_taken_today = True
                            award_xp(XP_REWARDS["all_meds"], "med", "all_meds_taken")
                            check_challenge("all_meds_taken_today")
                    st.rerun()
            with c3:
                if st.button("Remove 🗑️", key=f"del_{i}"):
                    st.session_state.medications.pop(i); st.rerun()

    if st.session_state.medications:
        taken = sum(1 for m in st.session_state.medications if m.get("taken",False))
        total = len(st.session_state.medications)
        st.progress(taken/total)
        st.markdown(f"**{taken}/{total}** taken today.")
        if taken == total > 0: st.success("🎉 All medications taken — you're crushing it! 💊")

    if st.button("💡 Adherence tips"):
        tips = f"""
**3 Tips to Never Miss Your Medications, {st.session_state.user_name}:**

**1. 📱 Phone Alarm Method**
Set a specific alarm for each medication with a label like "💊 Vitamin D — take now!". 
A distinct ringtone just for medications makes it impossible to ignore.

**2. 🔗 Habit Stacking**
Pair medications with an existing habit — take your morning pill right after brushing your teeth, 
and your evening pill right after dinner. Your existing habits become automatic reminders!

**3. 📦 Visual Cue**
Keep your medication bottle next to your toothbrush, coffee maker, or phone charger — 
somewhere you look every day without fail. Out of sight = out of mind!

> 💊 Consistency is your superpower, {st.session_state.user_name}! Every dose taken is a vote for your future health! 🌟
        """
        st.markdown(f'<div class="vita-card">{tips}</div>', unsafe_allow_html=True)

# ─── MY PROFILE ───────────────────────────────────────────────────────────────
elif page == "👤 My Profile":
    st.subheader("👤 My Health Profile")
    bv = bmi_value(); cat, css = bmi_category(bv)
    st.markdown(f"""
    <div class='stat-row'>
        <div class='stat-box'><div class='val'>{st.session_state.user_age}</div><div class='lbl'>Age</div></div>
        <div class='stat-box'><div class='val'>{st.session_state.user_gender[0]}</div><div class='lbl'>Gender</div></div>
        <div class='stat-box'><div class='val'>{st.session_state.user_height} cm</div><div class='lbl'>Height</div></div>
        <div class='stat-box'><div class='val'>{st.session_state.user_weight} kg</div><div class='lbl'>Weight</div></div>
        <div class='stat-box'><div class='val'>{bv}</div><div class='lbl'>BMI · <span class='bmi-badge {css}'>{cat}</span></div></div>
        <div class='stat-box'><div class='val'>{int(bmr_calc())} kcal</div><div class='lbl'>Est. BMR</div></div>
        <div class='stat-box'><div class='val'>{WATER_GOAL}💧</div><div class='lbl'>Water goal</div></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"**Goal:** {st.session_state.user_goal} &nbsp;|&nbsp; **Activity:** {st.session_state.get('user_activity','—')}")

    st.divider()
    st.markdown("#### 🏆 Achievements")
    earned = [b for b in BADGES if b[3] in st.session_state.badges_earned]
    if earned:
        st.markdown('<div class="badge-grid">'+"".join(f'<span class="badge-pill badge-earned">{b[0]} {b[1]}</span>' for b in earned)+'</div>', unsafe_allow_html=True)
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
    with st.form("profile_edit"):
        col1, col2 = st.columns(2)
        with col1:
            nn = st.text_input("Name", st.session_state.user_name)
            na = st.number_input("Age", 10, 100, st.session_state.user_age)
            nh = st.number_input("Height (cm)", 100.0, 250.0, st.session_state.user_height, 0.5)
        with col2:
            ng  = st.selectbox("Gender", GENDER_OPTIONS, index=GENDER_OPTIONS.index(st.session_state.user_gender) if st.session_state.user_gender in GENDER_OPTIONS else 0)
            nw  = st.number_input("Weight (kg)", 30.0, 300.0, st.session_state.user_weight, 0.5)
            ngl = st.selectbox("Health goal", GOAL_OPTIONS, index=GOAL_OPTIONS.index(st.session_state.user_goal) if st.session_state.user_goal in GOAL_OPTIONS else 0)
        if st.form_submit_button("Save changes ✅"):
            st.session_state.update({
                "user_name":nn,"user_age":int(na),"user_gender":ng,
                "user_height":float(nh),"user_weight":float(nw),"user_goal":ngl,
            })
            st.success("Profile updated! 🌿"); st.rerun()

    st.divider()
    if st.button("💡 Get my health summary"):
        st.markdown(f'<div class="vita-card">{get_response("general", profile)}</div>', unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.divider()
st.caption("🌿 VitaCoach · 100% Free · No API Key needed · Not a substitute for medical advice.")
