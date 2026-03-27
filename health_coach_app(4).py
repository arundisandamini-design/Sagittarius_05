"""
╔══════════════════════════════════════════════════════════╗
║           FlexCoach — AI Health Coach App v6             ║
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
import streamlit.components.v1 as components

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FlexCoach – Your Health Coach",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS — DARK MODE ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0d0d0d !important;
    color: #e0e0e0 !important;
}
h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #00e676 !important; }
h4, h5, h6 { color: #b0b0b0 !important; }
p, span, div { color: #e0e0e0; }
header { visibility: hidden; }

.main, .block-container { background-color: #0d0d0d !important; }

.flex-card {
    background: #161625;
    border: 1px solid #252545;
    border-radius: 16px; padding: 1.4rem;
    box-shadow: 0 4px 24px rgba(0,230,118,0.07);
    margin-bottom: 1rem;
}
.onboard-wrap {
    max-width: 640px; margin: 1.5rem auto;
    background: #161625; border: 1px solid #252545;
    border-radius: 24px; padding: 2.5rem 2.8rem;
    box-shadow: 0 4px 40px rgba(0,230,118,0.12);
}
.xp-bar-wrap {
    background: rgba(255,255,255,0.07); border-radius: 999px;
    height: 10px; margin: 6px 0 2px; overflow: hidden;
}
.xp-bar-fill {
    height: 100%; border-radius: 999px;
    background: linear-gradient(90deg, #00c853, #00e676);
    box-shadow: 0 0 8px rgba(0,230,118,0.5);
}
.level-label { font-size:0.75rem; letter-spacing:0.06em; opacity:0.7; margin-bottom:2px; color:#00e676 !important; }

.badge-grid { display:flex; flex-wrap:wrap; gap:10px; margin:0.6rem 0; }
.badge-pill {
    border-radius:999px; padding:5px 14px; font-size:0.82rem; font-weight:600;
    display:inline-flex; align-items:center; gap:5px;
}
.badge-earned { background:#0d2818; color:#00e676; border:1.5px solid #00e676; }
.badge-locked { background:#161625; color:#444;    border:1.5px solid #252545; }

.reward-toast {
    background: linear-gradient(135deg,#0a1f10,#0d2615);
    border-left: 4px solid #00e676; border-radius:12px;
    padding:1rem 1.3rem; margin:0.6rem 0;
    box-shadow: 0 2px 20px rgba(0,230,118,0.18);
}
.challenge-card {
    background: linear-gradient(135deg,#0a1a10,#0d2015);
    border: 1.5px solid #00e676;
    border-radius:16px; padding:1.2rem 1.5rem;
    margin-bottom:1rem; box-shadow:0 4px 20px rgba(0,230,118,0.15);
}
.challenge-card h4 { margin:0 0 0.3rem; font-size:1rem; color:#00e676 !important; }
.challenge-card p  { margin:0; font-size:0.88rem; opacity:0.85; color:#e0e0e0 !important; }

.streak-pill {
    display:inline-flex; align-items:center; gap:5px;
    background:#1f1200; color:#ffab40; border-radius:999px;
    padding:4px 14px; font-weight:600; font-size:0.82rem;
    border:1.5px solid #ffab40;
}
.stat-row { display:flex; gap:10px; flex-wrap:wrap; margin-bottom:1rem; }
.stat-box {
    flex:1; min-width:88px; background:#161625;
    border:1px solid #252545;
    border-radius:12px; padding:0.8rem 1rem; text-align:center;
}
.stat-box .val { font-size:1.25rem; font-weight:700; color:#00e676 !important; }
.stat-box .lbl { font-size:0.7rem; color:#666 !important; margin-top:2px; }

.bmi-badge      { display:inline-block; border-radius:999px; padding:3px 14px; font-weight:600; font-size:0.82rem; }
.bmi-underweight{ background:#0a1530; color:#82b1ff; }
.bmi-normal     { background:#0a2015; color:#00e676; }
.bmi-overweight { background:#1f1500; color:#ffab40; }
.bmi-obese      { background:#200a0a; color:#ff5252; }

.user-bubble {
    background:#0d2015; border-radius:16px 16px 4px 16px;
    padding:0.8rem 1.1rem; margin:0.4rem 0;
    max-width:80%; margin-left:auto; font-size:0.95rem;
    color:#e0e0e0 !important; border:1px solid #00e676;
}
.coach-bubble {
    background:#161625; border-left:3px solid #00e676;
    border-radius:4px 16px 16px 16px; padding:0.8rem 1.1rem;
    margin:0.4rem 0; max-width:88%; font-size:0.95rem;
    color:#e0e0e0 !important;
    box-shadow:0 2px 12px rgba(0,230,118,0.08);
}
.drop  { font-size:1.8rem; }
.empty { filter:grayscale(1) opacity(0.18); }

[data-testid="stSidebar"] {
    background: #090912 !important;
    border-right: 1px solid #1a1a30;
}
[data-testid="stSidebar"] * { color: #e0e0e0 !important; }
[data-testid="stSidebar"] h2 { color:#00e676 !important; font-size:1.1rem !important; letter-spacing:0.05em; }

.stButton > button {
    border-radius:999px;
    background: linear-gradient(90deg, #00c853, #00e676) !important;
    color:#0a0a0a !important; font-weight:700;
    border:none; padding:0.5rem 1.6rem;
    box-shadow: 0 0 14px rgba(0,230,118,0.3);
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background: linear-gradient(90deg,#00e676,#69f0ae) !important;
    box-shadow: 0 0 22px rgba(0,230,118,0.55);
    transform: translateY(-1px);
}
.stTextInput input, .stNumberInput input {
    background:#161625 !important; color:#e0e0e0 !important;
    border:1px solid #252545 !important; border-radius:8px !important;
}
.stTextInput input:focus {
    border-color:#00e676 !important;
    box-shadow:0 0 8px rgba(0,230,118,0.25) !important;
}
div[data-baseweb="select"] > div {
    background:#161625 !important; border-color:#252545 !important;
    color:#e0e0e0 !important;
}
.stProgress > div > div > div {
    background: linear-gradient(90deg,#00c853,#00e676) !important;
    box-shadow:0 0 8px rgba(0,230,118,0.4);
}
[data-testid="stExpander"] {
    background:#161625 !important; border:1px solid #252545 !important;
    border-radius:12px !important;
}
[data-testid="stForm"] {
    background:#161625 !important; border:1px solid #252545 !important;
    border-radius:12px; padding:1rem;
}
hr { border-color:#252545 !important; }
.stSuccess { background:#0a2015 !important; border-color:#00e676 !important; }
.stInfo    { background:#0a1525 !important; border-color:#448aff !important; }
.stError   { background:#200a0a !important; border-color:#ff5252 !important; }
.stWarning { background:#1f1500 !important; border-color:#ffab40 !important; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# BUILT-IN SMART RESPONSES  (no API needed)
# ════════════════════════════════════════════════════════════════════════════


def build_meal_plan(profile: dict) -> str:
    """Generate a fully personalised 7-day meal plan based on user profile."""
    name   = profile["name"]
    age    = profile["age"]
    gender = profile["gender"]
    weight = profile["weight"]
    height = profile["height"]
    goal   = profile["goal"]
    bmi    = round(weight / ((height / 100) ** 2), 1)
    kcal   = int((10*weight + 6.25*height - 5*age + (5 if gender=="Male" else -161)) * 1.4)

    # ── Per-goal calorie adjustment ──────────────────────────────────────────
    if goal in ["Weight loss"]:
        kcal = max(1200, kcal - 400)
        goal_note = f"calorie deficit of ~{kcal} kcal/day to support weight loss"
        protein_tip = "Prioritise lean protein (chicken, fish, tofu) at every meal to preserve muscle while losing fat."
    elif goal in ["Muscle gain", "Improve fitness"]:
        kcal = kcal + 300
        goal_note = f"calorie surplus of ~{kcal} kcal/day to support muscle growth"
        protein_tip = "Aim for 1.6–2.0 g of protein per kg of body weight daily. Eat within 30 min after training."
    elif goal in ["Better sleep"]:
        goal_note = f"~{kcal} kcal/day with sleep-supporting nutrients (magnesium, tryptophan)"
        protein_tip = "Eat a light snack with tryptophan before bed (banana, warm milk, turkey) to support melatonin."
    elif goal in ["Stress management"]:
        goal_note = f"~{kcal} kcal/day with anti-stress nutrients (omega-3, magnesium, B vitamins)"
        protein_tip = "Include fatty fish, dark leafy greens and nuts — these are proven stress-reducing foods."
    elif goal in ["Increase energy levels"]:
        goal_note = f"~{kcal} kcal/day with sustained-energy foods"
        protein_tip = "Eat complex carbs (oats, quinoa, sweet potato) for steady energy — avoid sugar spikes."
    else:
        goal_note = f"balanced ~{kcal} kcal/day for general wellness"
        protein_tip = "Eat a rainbow of vegetables daily — aim for at least 5 different colours to maximise nutrients."

    # ── Per-goal food pools ─────────────────────────────────────────────────
    if goal == "Weight loss":
        breakfasts = [
            "Greek yoghurt (0%) with cucumber & 1 boiled egg",
            "Overnight oats (40g oats, skim milk, no sugar) with blueberries",
            "2 boiled eggs with sliced avocado (¼) on 1 rye crispbread",
            "Smoothie: spinach, cucumber, lemon, ginger, 1 scoop protein powder",
            "Cottage cheese (150g) with sliced strawberries & chia seeds",
            "Veggie omelette (2 eggs, mushrooms, spinach, no oil spray)",
            "1 slice whole grain toast with smashed avocado & poached egg",
        ]
        lunches = [
            "Large mixed salad with grilled chicken (150g), lemon-olive oil dressing",
            "Tuna & cucumber lettuce wraps (no mayo) with cherry tomatoes",
            "Lentil & vegetable soup (low sodium) with 1 rye crispbread",
            "Zucchini noodles with homemade tomato sauce & turkey mince (100g)",
            "Cauliflower rice bowl with black beans, salsa & grilled peppers",
            "Grilled white fish (150g) with steamed broccoli & lemon",
            "Chicken & vegetable broth with kale & 1 small wholegrain roll",
        ]
        dinners = [
            "Baked salmon (150g) with asparagus & side salad",
            "Grilled chicken breast (150g) with ratatouille vegetables",
            "Stir-fried tofu & bok choy with cauliflower rice",
            "Prawn & vegetable skewers with cucumber-tomato salad",
            "Turkey meatballs in tomato sauce with courgette noodles",
            "Baked cod with spinach & garlic (no butter)",
            "Stuffed bell peppers with lean mince & diced tomatoes",
        ]
        snacks = [
            "10 almonds + herbal tea",
            "1 medium apple",
            "Carrot & celery sticks with 2 tbsp hummus",
            "1 boiled egg + cucumber slices",
            "150g low-fat Greek yoghurt",
            "1 small pear",
            "Rice cake with 1 tsp almond butter",
        ]
    elif goal in ["Muscle gain", "Improve fitness"]:
        breakfasts = [
            "4 scrambled eggs with whole grain toast & sliced avocado",
            "Protein oats: 80g oats, 1 scoop whey, banana & peanut butter",
            "Greek yoghurt (200g full fat) with granola, honey & mixed berries",
            "Whole grain pancakes (3) with Greek yoghurt & blueberry compote",
            "Smoothie: banana, oats, milk, 2 scoops protein, peanut butter",
            "Smoked salmon on 2 whole grain bagels with cream cheese",
            "4-egg veggie omelette with cheese, peppers & whole grain toast",
        ]
        lunches = [
            "Grilled chicken breast (200g) with brown rice (150g) & broccoli",
            "Tuna pasta (whole grain, 200g) with sweetcorn & light mayo",
            "Beef & vegetable stir-fry with egg noodles (200g)",
            "Quinoa power bowl with chickpeas, feta, roasted sweet potato",
            "Turkey & avocado whole grain wrap with spinach & tomato",
            "Salmon fillet (180g) with couscous & roasted Mediterranean veg",
            "Chicken Caesar salad (large) with whole grain croutons",
        ]
        dinners = [
            "Beef steak (200g) with mashed sweet potato & green beans",
            "Baked chicken thighs (200g) with roasted potatoes & coleslaw",
            "Salmon (200g) with whole grain pasta & creamy pesto sauce",
            "Pork tenderloin with apple sauce, roasted carrots & rice",
            "Lamb mince curry with basmati rice & naan bread",
            "Grilled sea bass with quinoa & roasted asparagus",
            "Turkey bolognese with whole grain spaghetti & parmesan",
        ]
        snacks = [
            "Protein shake + banana",
            "200g cottage cheese + pineapple chunks",
            "Handful of mixed nuts & dried fruit (50g)",
            "2 rice cakes with peanut butter & honey",
            "Hard-boiled eggs (2) + whole grain crackers",
            "Greek yoghurt (200g) + granola",
            "Chocolate milk (300ml) — excellent post-workout recovery",
        ]
    elif goal == "Better sleep":
        breakfasts = [
            "Warm oatmeal with banana, warm milk & a pinch of cinnamon",
            "Whole grain toast with almond butter & sliced banana",
            "Chamomile-infused overnight oats with cherries & honey",
            "Warm porridge with pumpkin seeds (magnesium-rich) & berries",
            "Smoothie: banana, warm almond milk, dates, pinch of nutmeg",
            "Scrambled eggs (2) with spinach & warm herbal tea",
            "Greek yoghurt with walnuts (tryptophan) & honey",
        ]
        lunches = [
            "Turkey salad wrap (tryptophan-rich) with lettuce & tomato",
            "Lentil soup with whole grain bread & side salad",
            "Grilled salmon with quinoa & steamed kale",
            "Chickpea & spinach curry with basmati rice",
            "Tuna salad with avocado on whole grain bread",
            "Chicken & vegetable soup with brown rice",
            "Tofu & edamame bowl with sesame dressing",
        ]
        dinners = [
            "Warm turkey stew with root vegetables & mashed potato",
            "Baked salmon with sweet potato & steamed green beans",
            "Chamomile-glazed chicken with roasted carrots & quinoa",
            "Lentil dahl with warm naan & cucumber raita",
            "Pasta with tuna, spinach & light cream sauce (early dinner)",
            "Grilled chicken with roasted pumpkin & herbed couscous",
            "Tofu stir-fry with bok choy, sesame oil & brown rice",
        ]
        snacks = [
            "Warm almond milk with a pinch of turmeric & honey",
            "A small bowl of tart cherries (natural melatonin source)",
            "1 banana + 10 almonds (tryptophan + magnesium combo)",
            "Warm chamomile tea + 2 oat biscuits",
            "Kiwi fruit × 2 (shown to improve sleep quality)",
            "Warm milk + pinch of cinnamon",
            "Small handful of pumpkin seeds (magnesium)",
        ]
    elif goal == "Stress management":
        breakfasts = [
            "Omega-3 smoothie: flaxseed, banana, spinach, almond milk",
            "Smoked salmon on whole grain toast with avocado & lemon",
            "Dark chocolate (2 squares) overnight oats with walnuts",
            "Eggs florentine (2 poached eggs on spinach & whole grain muffin)",
            "Blueberry & walnut Greek yoghurt parfait with honey",
            "Matcha latte with oat milk + whole grain toast with nut butter",
            "Veggie omelette with dark leafy greens & whole grain toast",
        ]
        lunches = [
            "Mackerel salad with mixed leaves, beetroot & whole grain crackers",
            "Avocado & chickpea bowl with lemon-tahini dressing",
            "Lentil & spinach soup (iron & B-vitamin rich) with rye bread",
            "Salmon & quinoa power bowl with edamame & ginger dressing",
            "Dark leafy green wrap with hummus, roasted veg & feta",
            "Miso soup with tofu, seaweed & brown rice",
            "Walnut-crusted chicken salad with blueberries & balsamic",
        ]
        dinners = [
            "Baked salmon with turmeric roasted vegetables & brown rice",
            "Dark leafy greens pasta with sardines, garlic & olive oil",
            "Chicken & broccoli stir-fry with cashews & brown rice",
            "Lentil bolognese with whole grain spaghetti & fresh basil",
            "Grilled mackerel with roasted beetroot & herbed couscous",
            "Tofu & edamame curry with spinach & basmati rice",
            "Turkey & vegetable one-pot with sweet potato & thyme",
        ]
        snacks = [
            "Dark chocolate (70%+) × 2 squares + green tea",
            "Walnuts & blueberries (30g each) — top anti-stress combo",
            "Avocado on 1 rice cake with lemon",
            "Matcha tea with oat milk (L-theanine for calm focus)",
            "Banana + almond butter (magnesium & potassium)",
            "Mixed seeds (pumpkin, sunflower) — magnesium powerhouse",
            "Chamomile tea + 1 small square dark chocolate",
        ]
    elif goal == "Increase energy levels":
        breakfasts = [
            "Power oats: 80g oats, banana, honey, chia seeds & almond milk",
            "Whole grain toast with eggs (2) & sliced avocado + orange juice",
            "Energy smoothie: mango, banana, spinach, ginger & coconut water",
            "Quinoa breakfast bowl with berries, honey & toasted almonds",
            "Granola with Greek yoghurt, mango & passionfruit",
            "Whole grain bagel with smoked salmon, cream cheese & capers",
            "Porridge with apple, cinnamon & walnuts + green tea",
        ]
        lunches = [
            "Sweet potato & black bean burrito bowl with brown rice & salsa",
            "Grilled chicken with roasted sweet potato, quinoa & kale",
            "Whole grain pasta with tuna, sweetcorn & rocket",
            "Energy bowl: brown rice, salmon, edamame, avocado & sesame",
            "Chickpea & spinach curry with basmati rice & mango chutney",
            "Falafel wrap with hummus, roasted veg & tabbouleh",
            "Grilled prawn & mango salad with wild rice",
        ]
        dinners = [
            "Steak (150g) with roasted sweet potato wedges & salad",
            "Chicken & vegetable stir-fry with udon noodles & ginger",
            "Baked cod with quinoa, roasted Mediterranean vegetables",
            "Lamb tagine with chickpeas, apricots & couscous",
            "Prawn & avocado pasta with lemon-garlic sauce",
            "Turkey & sweet potato curry with brown rice",
            "Salmon teriyaki with steamed edamame & brown rice",
        ]
        snacks = [
            "Medjool dates × 2 + almonds (quick natural energy boost)",
            "Banana + peanut butter on rice cakes",
            "Trail mix: nuts, seeds & dried mango",
            "Coconut water + 1 orange (electrolytes + vitamin C)",
            "Energy balls: oats, honey, dark chocolate chips, peanut butter",
            "Mango & Greek yoghurt with a drizzle of honey",
            "Apple slices with almond butter & a sprinkle of cinnamon",
        ]
    else:  # General wellness / default
        breakfasts = [
            "Oatmeal with banana, honey & chia seeds",
            "Greek yoghurt with mixed berries & granola",
            "Scrambled eggs (2) with spinach & whole grain toast",
            "Smoothie: banana, spinach, almond milk & protein powder",
            "Whole grain pancakes with fresh fruit & maple syrup",
            "Avocado toast with poached egg & cherry tomatoes",
            "Veggie omelette with mushrooms, peppers & onions",
        ]
        lunches = [
            "Grilled chicken salad with olive oil dressing",
            "Lentil soup with whole grain bread",
            "Tuna wrap with lettuce, tomato & avocado",
            "Quinoa bowl with chickpeas, cucumber & feta",
            "Turkey & avocado sandwich on whole grain bread",
            "Black bean soup with whole grain crackers",
            "Greek salad with grilled shrimp & pita bread",
        ]
        dinners = [
            "Baked salmon with steamed broccoli & brown rice",
            "Stir-fried tofu with vegetables & quinoa",
            "Chicken stir-fry with bell peppers & brown rice",
            "Grilled fish tacos with cabbage slaw & salsa",
            "Beef & vegetable stew with whole grain roll",
            "Baked chicken breast with sweet potato & green beans",
            "Homemade vegetable curry with basmati rice",
        ]
        snacks = [
            "Apple with almond butter",
            "Banana & a handful of walnuts",
            "Carrot sticks with hummus",
            "Orange & a handful of almonds",
            "Blueberries & cottage cheese",
            "Mixed nuts & dried fruit",
            "Strawberries & dark chocolate (2 squares)",
        ]

    # ── BMI-based tweak note ────────────────────────────────────────────────
    if bmi < 18.5:
        bmi_note = f"⚠️ Your BMI ({bmi}) is below healthy range — portions are sized **larger** to help you gain weight healthily. Add extra olive oil, nuts and full-fat dairy wherever possible."
    elif bmi >= 30:
        bmi_note = f"💙 Your BMI ({bmi}) is noted — portions are **calorie-controlled** and focused on whole, filling foods to support your journey. Every healthy meal is a win!"
    elif bmi >= 25:
        bmi_note = f"📌 Your BMI ({bmi}) is slightly above healthy range — this plan uses **moderate portions** with plenty of vegetables and lean protein."
    else:
        bmi_note = f"✅ Your BMI ({bmi}) is in the healthy range — this plan is designed to **maintain and optimise** your health."

    # ── Age-based tweak note ────────────────────────────────────────────────
    if age >= 50:
        age_note = "🦴 Over 50: Plan includes calcium-rich foods (dairy, leafy greens) and vitamin D sources to support bone health."
    elif age <= 25:
        age_note = "⚡ Under 25: Plan supports your active metabolism with complex carbs and adequate protein for growth and energy."
    else:
        age_note = ""

    # ── Build the plan using shuffled day order ─────────────────────────────
    # Shuffle using name+goal as seed so same user gets same plan, different users get different
    import hashlib
    seed = int(hashlib.md5(f"{name}{goal}{age}".encode()).hexdigest(), 16) % 10000
    rng  = random.Random(seed)
    days = list(range(7))
    rng.shuffle(days)

    plan = f"""### 🥗 Your Personalised 7-Day Meal Plan, {name}!

**👤 Profile:** {age}y · {gender} · {weight}kg · Goal: *{goal}*
**🔥 Daily Target:** ~{kcal} kcal ({goal_note})
{bmi_note}
{age_note}
---
"""
    day_names = ["📅 Monday","📅 Tuesday","📅 Wednesday","📅 Thursday","📅 Friday","📅 Saturday","📅 Sunday"]
    for i, d in enumerate(days):
        plan += f"""
**{day_names[i]}**
- 🌅 Breakfast: {breakfasts[d]}
- 🌞 Lunch: {lunches[d]}
- 🌙 Dinner: {dinners[d]}
- 🍎 Snack: {snacks[d]}
"""

    plan += f"""
---
**💡 Your #1 Nutrition Tip, {name}:**
{protein_tip}

> 🌟 You're fuelling your body for *{goal.lower()}* — every meal you choose wisely is a powerful step forward. You've got this! 💪
"""
    return plan

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

    "meal_plan": build_meal_plan(profile),

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

**💪 Daily Habits (15 Minutes/Day)**
- Morning: 5 min of box breathing before checking your phone
- Afternoon: A 10-min walk outside (nature reduces cortisol by 20%)
- Evening: Write 3 things you're grateful for in a journal

**💪 Weekly Habits**
- Exercise 3–4 times/week (even a 20-min walk counts!)
- Connect with someone you care about — social connection is the #1 stress buffer
- Limit caffeine after 2 PM — it raises cortisol for up to 6 hours

**🚨 Signs You Need Extra Support**
If stress feels overwhelming for more than 2 weeks, please speak to a doctor or mental health professional. There is no shame in asking for help — it's the bravest thing you can do.

> 💚 {name}, you are stronger than your stress. One breath at a time, one day at a time. You've got this! 💪
    """,

    "general": f"""
### 💪 Health Tips Personalised for {name}

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
    msg  = user_msg.lower()
    name = profile["name"]

    WORKOUT_WORDS = [
        "workout", "work out", "exercise", "gym", "training", "train",
        "fitness", "strength", "cardio", "hiit", "muscle", "weight loss",
        "lose weight", "gain muscle", "build muscle", "run", "running",
        "jog", "jogging", "push", "pull", "squat", "plank", "abs",
        "core", "upper body", "lower body", "legs", "arms", "chest",
        "back", "glutes", "sport", "active", "physical",
        "plan", "routine", "schedule", "programme", "program",
        "lift", "lifting", "weights", "dumbbell", "barbell", "resistance",
        "beginner", "intermediate", "advanced", "fat", "burn", "calories",
    ]
    MEAL_WORDS = [
        "meal", "food", "eat", "eating", "diet", "nutrition", "recipe",
        "breakfast", "lunch", "dinner", "snack", "cook", "cooking",
        "protein", "carb", "calorie", "vegetable", "fruit",
        "what to eat", "what should i eat", "menu",
    ]
    MEDITATE_WORDS = [
        "meditat", "calm", "relax", "mindful", "breathe", "breathing",
        "peace", "zen", "anxiety relief", "panic", "unwind",
    ]
    STRESS_WORDS = [
        "stress", "anxious", "anxiety", "worry", "overwhelm",
        "pressure", "mental health", "burnout", "depressed", "sad",
    ]
    WATER_WORDS  = ["water", "hydrat", "drink", "thirst", "fluid", "dehydrat"]
    SLEEP_WORDS  = ["sleep", "insomnia", "tired", "rest", "fatigue", "energy", "wake up", "nap", "bedtime"]
    BMI_WORDS    = ["bmi", "overweight", "underweight", "obese", "body mass", "healthy weight", "ideal weight"]

    if any(w in msg for w in WORKOUT_WORDS):
        return get_response("workout", profile)
    elif any(w in msg for w in MEAL_WORDS):
        return get_response("meal_plan", profile)
    elif any(w in msg for w in MEDITATE_WORDS):
        return get_response("meditation", profile)
    elif any(w in msg for w in STRESS_WORDS):
        return get_response("stress", profile)
    elif any(w in msg for w in WATER_WORDS):
        return get_response("hydration", profile)
    elif any(w in msg for w in SLEEP_WORDS):
        return get_response("sleep", profile)
    elif any(w in msg for w in BMI_WORDS):
        return get_response("bmi_advice", profile)
    else:
        tips = [
            f"Great question, {name}! 🌟 Focus on the basics: drink {round(profile['weight'] * 35 / 1000, 1)}L of water daily, sleep 7–9 hours, move your body 30 min/day, and eat mostly whole foods. These habits alone will transform your health! 💚",
            f"Love your energy, {name}! 💪 Health is built in small daily decisions. The water you drank, the walk you took, the meal you cooked — it all counts. Keep going! 🔥",
            f"Great one, {name}! 🧠 Pick ONE healthy habit this week and do it every day. Consistency beats perfection every time. What will you start today? 🌟",
            f"You’re on the right track, {name}! 🎯 Pair new habits with things you already do — drink water when you brush teeth, stretch while watching TV. Small changes, massive results! 🔥",
            f"Awesome, {name}! 🏆 Try asking me: **workout plan**, **meal plan**, **meditation**, **sleep tips**, **hydration**, or **stress management** — I’m here for all of it! 💪",
        ]
        return random.choice(tips)


# ════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ════════════════════════════════════════════════════════════════════════════
LEVELS = [
    (0,    "🌱 Seedling",     100),
    (100,  "💪 Sprout",       250),
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
    ("💬", "Chatterbox",       "Send 10 messages to FlexCoach",          "chat_10"),
    ("🔥", "7-Day Streak",     "Use the app 7 days in a row",            "streak_7"),
    ("🌟", "Centurion",        "Earn 500 XP total",                      "xp_500"),
    ("🏆", "FlexCoach Legend", "Earn 2000 XP total",                     "xp_2000"),
    ("🌅", "Early Bird",       "Open the app before 8 AM",               "early_bird"),
    ("🎯", "Goal Getter",      "Complete 5 daily challenges",            "challenges_5"),
]
DAILY_CHALLENGES = [
    ("💧", "Drink 3 glasses of water before noon.",     "water_count",          3),
    ("🧘", "Do a meditation session today.",             "meditation_done",       True),
    ("💬", "Ask FlexCoach for a health tip.",            "chat_count",            1),
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
    "login":      ["Welcome back, champion! 💪","Another day to be amazing! ✨","Let's make today count! 🌟"],
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
        "voice_enabled":        True,
        "voice_speed":          0.95,
        "voice_pitch":          1.15,
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


def speak(text: str, force: bool = False):
    """Speak text via browser Web Speech API using a female English voice (Aria)."""
    if not st.session_state.get("voice_enabled", True) and not force:
        return
    import re
    clean = text
    clean = re.sub(r"\*\*(.*?)\*\*", r"\1", clean)
    clean = re.sub(r"\*(.*?)\*",     r"\1", clean)
    clean = re.sub(r"[#_`>~]",       "",    clean)
    clean = re.sub(r":[a-z_]+:",      "",    clean)
    clean = re.sub(
        "["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002700-\U000027BF"
        u"\U000024C2-\U0001F251"
        "]+", " ", clean, flags=re.UNICODE)
    clean = re.sub(r"\s+", " ", clean).strip()
    if not clean:
        return
    # Cap at 280 chars for natural speech length
    if len(clean) > 280:
        clean = clean[:280].rsplit(" ", 1)[0] + "."
    spd   = float(st.session_state.get("voice_speed", 0.92))
    pitch = float(st.session_state.get("voice_pitch", 1.2))
    js_text = clean.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
    js = f"""
    <script>
    (function() {{
        if (!window.speechSynthesis) return;
        window.speechSynthesis.cancel();
        var u = new SpeechSynthesisUtterance('{js_text}');
        u.rate   = {spd};
        u.pitch  = {pitch};
        u.volume = 1.0;
        function pickVoice() {{
            var voices = window.speechSynthesis.getVoices();
            // Priority list — female English voices across browsers/OS
            var names = [
                "samantha","karen","victoria","moira","tessa","fiona",
                "allison","ava","susan","zira","aria","hazel","eva",
                "google uk english female","microsoft zira",
                "google us english","eloquence"
            ];
            var chosen = null;
            for (var n of names) {{
                chosen = voices.find(v => v.name.toLowerCase().includes(n) && v.lang.startsWith("en"));
                if (chosen) break;
            }}
            // Fallback: any English female-sounding voice
            if (!chosen) {{
                chosen = voices.find(v => v.lang.startsWith("en-") && v.name.toLowerCase().includes("female"));
            }}
            // Last resort: first English voice
            if (!chosen) {{
                chosen = voices.find(v => v.lang.startsWith("en"));
            }}
            if (chosen) u.voice = chosen;
        }}
        if (window.speechSynthesis.getVoices().length > 0) {{
            pickVoice(); window.speechSynthesis.speak(u);
        }} else {{
            window.speechSynthesis.onvoiceschanged = function() {{
                pickVoice(); window.speechSynthesis.speak(u);
            }};
        }}
    }})();
    </script>
    """
    components.html(js, height=0, scrolling=False)

def speak_aria(key: str, name: str = ""):
    """Speak a pre-written Aria compliment by key. Safe — never crashes."""
    if not st.session_state.get("voice_enabled", True):
        return
    n = name or st.session_state.get("user_name", "champion")
    lines = {
        "login":        [
            f"Welcome back, {n}! I missed you. Let's crush today together!",
            f"Hey {n}! You showed up — that's already a win. Let's go!",
            f"Good to see you again, {n}! Your health journey continues right now.",
        ],
        "login_streak": [
            f"Wow, {n}! Your streak is on fire! Consistency is your superpower!",
            f"Look at you go, {n}! Another day, another step closer to your goal!",
            f"Incredible dedication, {n}! Every single day you show up for yourself!",
        ],
        "water":        [
            f"Yes! Staying hydrated, {n}! Your body loves you for this!",
            f"Every sip counts, {n}! You're doing amazing!",
            f"Hydration hero mode activated, {n}! Keep it up!",
        ],
        "water_goal":   [
            f"Oh my goodness, {n}! You hit your full water goal! That is incredible!",
            f"Water goal smashed, {n}! Your cells are literally dancing with joy right now!",
            f"You did it, {n}! Full hydration achieved! You are a true health champion!",
        ],
        "meal":         [
            f"Fantastic, {n}! Fuelling your body right is one of the best things you can do!",
            f"Your meal plan is ready, {n}! Eating well is self-love in action!",
            f"Love this energy, {n}! Nutrition is the foundation of everything — great choice!",
        ],
        "workout":      [
            f"Let's go, {n}! Your workout plan is ready! Time to build the strongest version of you!",
            f"You are going to crush this, {n}! Every rep is a vote for your future self!",
            f"Beast mode activated, {n}! Your body is capable of amazing things — believe it!",
        ],
        "meditation":   [
            f"Beautiful choice, {n}. Taking time to breathe is true strength.",
            f"Your mind deserves this peace, {n}. Let's find your calm together.",
            f"Mindfulness is your superpower, {n}. You are doing something truly powerful right now.",
        ],
        "bmi":          [
            f"Great work tracking your health, {n}! Knowledge is the first step to change!",
            f"You are so smart for keeping track, {n}! Data-driven health is the way forward!",
            f"Knowing your numbers is powerful, {n}! You are in control of your journey!",
        ],
        "med":          [
            f"Well done, {n}! Taking your medication on time shows real commitment to your health!",
            f"Consistency is your superpower, {n}! Every dose is a step toward feeling your best!",
            f"You did it, {n}! Your health routine is rock solid and I am so proud of you!",
        ],
        "all_meds":     [
            f"All medications taken, {n}! You are absolutely crushing your health goals today!",
            f"Perfect score on medications today, {n}! Your discipline is truly inspiring!",
        ],
        "challenge":    [
            f"Daily challenge complete, {n}! You are absolutely legendary!",
            f"Look at you go, {n}! Challenge crushed! You are on a completely different level!",
            f"Champion behaviour, {n}! You set a goal and you delivered. I am so proud of you!",
        ],
        "level_up":     [
            f"Oh wow, {n}! You just levelled up! You are unstoppable! Keep going, champion!",
            f"New level unlocked, {n}! All your hard work is paying off in the most amazing way!",
            f"Level up, {n}! You are literally levelling up in life right now! I am cheering so loud for you!",
        ],
        "badge":        [
            f"New badge unlocked, {n}! You earned this — every single action you took got you here!",
            f"Badge achieved, {n}! Your dedication is creating real results. I see you!",
        ],
        "greeting_morning": [
            f"Good morning, {n}! Today is a brand new opportunity to be the healthiest version of you!",
            f"Rise and shine, {n}! Your body is ready for an amazing day. Let's make it count!",
        ],
        "greeting_afternoon": [
            f"Good afternoon, {n}! You are halfway through the day — keep making healthy choices!",
            f"Hey {n}! Afternoon check-in — how are you feeling? Let's keep the momentum going!",
        ],
        "greeting_evening": [
            f"Good evening, {n}! You've made it through another day. I hope you took good care of yourself!",
            f"Evening, {n}! Time to wind down and recover. You deserve rest after everything you've done today!",
        ],
        "chat":         [
            f"Great question, {n}! I love how curious you are about your health!",
            f"You are asking all the right questions, {n}! That curiosity is going to take you far!",
            f"Love your dedication, {n}! Every question brings you closer to your goals!",
        ],
        "profile_saved": [
            f"Profile updated, {n}! Every time you update your stats, you are taking your health seriously. Love that!",
        ],
    }
    pool = lines.get(key, [f"You're doing great, {n}! Keep it up!"])
    speak(random.choice(pool))


def voice_controls():
    """Render Aria voice panel in sidebar — prominent & beautiful."""
    n = st.session_state.get("user_name", "friend")
    enabled = st.session_state.get("voice_enabled", True)

    # Aria avatar card
    status_color = "#00e676" if enabled else "#444"
    status_text  = "LIVE" if enabled else "OFF"
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0a1f10,#0d2a18);
                border:1.5px solid {status_color};border-radius:16px;
                padding:1rem 1.1rem;margin:0.5rem 0 0.8rem;text-align:center">
        <div style="font-size:2.2rem;margin-bottom:4px">👩</div>
        <div style="font-size:0.95rem;font-weight:700;color:#00e676;letter-spacing:0.05em">ARIA</div>
        <div style="font-size:0.72rem;color:#aaa;margin-bottom:6px">Your AI Girl Coach</div>
        <span style="background:{status_color};color:#0d0d0d;border-radius:999px;
                     padding:2px 10px;font-size:0.7rem;font-weight:700">{status_text}</span>
    </div>
    """, unsafe_allow_html=True)

    enabled = st.toggle(
        "🎙️ Aria Voice On/Off",
        value=enabled,
        key="voice_toggle_widget",
        help="Aria cheers you on, celebrates wins & speaks health tips!",
    )
    st.session_state.voice_enabled = enabled

    if enabled:
        st.markdown("<div style='font-size:0.75rem;color:#888;margin:4px 0 2px'>Speed · Pitch</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            spd = st.slider("Spd", 0.6, 1.4,
                float(st.session_state.get("voice_speed", 0.92)), 0.05,
                key="spd_slider", label_visibility="collapsed")
        with col2:
            pit = st.slider("Pit", 0.8, 1.8,
                float(st.session_state.get("voice_pitch", 1.25)), 0.05,
                key="pit_slider", label_visibility="collapsed")
        st.session_state.voice_speed = spd
        st.session_state.voice_pitch = pit

        col1, col2 = st.columns(2)
        with col1:
            if st.button("👋 Meet Aria"):
                speak(
                    f"Hey {n}! I am Aria, your personal FlexCoach girl coach. "
                    f"I am here to cheer you on every single day, celebrate every win no matter how small, "
                    f"and remind you how absolutely incredible you are. "
                    f"Together, {n}, we are going to build the healthiest, strongest, happiest version of you. "
                    f"Let's do this!", force=True)
        with col2:
            if st.button("🔇 Stop"):
                import streamlit.components.v1 as _c
                _c.html("<script>window.speechSynthesis && window.speechSynthesis.cancel();</script>",
                        height=0)

        # Aria compliment button
        if st.button("💚 Aria Compliment"):
            compliments = [
                f"Hey {n}, I just want to remind you — you are doing better than you think. Every single healthy choice you make is moving you forward. I am so proud of you!",
                f"{n}, you are genuinely one of the most motivated people I know. The fact that you are here, taking care of yourself, means everything. Keep going!",
                f"I see you, {n}. Every glass of water, every workout, every healthy meal — it all adds up to something amazing. You are building the life you deserve!",
                f"You know what I love about you, {n}? You never give up. Even on hard days, you come back. That is what champions are made of. You are a champion!",
                f"{n}, your body is working so hard for you every single day. It deserves all the love and care you are giving it. You are doing beautifully!",
                f"Just a little reminder, {n} — progress is progress, no matter how small. You are not the same person you were when you started. You are growing every day!",
                f"Hey superstar! That is what you are, {n}. A health superstar in the making. I believe in you completely and I am here for every step of your journey!",
            ]
            import random as _r
            speak(_r.choice(compliments), force=True)
    else:
        st.markdown("<div style='font-size:0.78rem;color:#666;text-align:center;padding:4px'>Turn on to hear Aria! 🎙️</div>", unsafe_allow_html=True)


def show_reward():
    r = st.session_state.get("pending_reward")
    if not r: return
    icon = "🎊" if r.get("level_up") else ("🏅" if r.get("badge") else "✨")
    st.markdown(
        f'<div class="reward-toast"><span style="font-size:1.3rem">{icon}</span> {r["msg"]}</div>',
        unsafe_allow_html=True)
    # Aria speaks the right line
    name = st.session_state.get("user_name", "champion")
    if r.get("level_up"):
        speak_aria("level_up", name)
    elif r.get("badge"):
        speak_aria("badge", name)
    else:
        import re
        raw    = r["msg"]
        spoken = re.sub(r"\*\*(.*?)\*\*", r"\1", raw)
        spoken = re.sub(r"[+0-9]+ XP", "experience points", spoken)
        speak(spoken)
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
        "xp": bonus, "msg": f"{random.choice(pool)} **+{bonus} XP** for showing up today! 💪",
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
        <span style='font-size:3.5rem'>💪</span>
        <h1 style='margin:0;color:#00e676'>FlexCoach</h1>
        <p style='color:#666;margin-top:0.2rem'>Your personalised AI health companion — 100% Free!</p>
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
            f'<p style="color:#aaa;font-size:0.88rem">📊 BMI preview: '
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
    st.markdown("## 💪 FlexCoach")
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
    voice_controls()
    st.divider()
    if st.button("🔄 Edit Profile"):
        st.session_state.profile_complete = False; st.rerun()
    st.caption("Not a substitute for medical advice.")

st.markdown("# 💪 FlexCoach")
tod_h = datetime.datetime.now().hour
greeting = "Good morning" if tod_h < 12 else "Good afternoon" if tod_h < 17 else "Good evening"
st.markdown(f"**{greeting}, {st.session_state.user_name}! 👋** You're doing great — keep it up!")
show_reward()
# Aria greets the user on page load (only once per session per page visit)
_greet_key = f"greeted_{today}_{page if 'page' in dir() else 'home'}"
if not st.session_state.get(_greet_key):
    st.session_state[_greet_key] = True
    _greet_msgs = [
        f"{greeting} {st.session_state.user_name}! Welcome back to FlexCoach. You're doing an amazing job — let's crush today together!",
        f"Hey {st.session_state.user_name}! So great to see you. Every time you open this app, you're choosing your health. That is something to be proud of!",
        f"{greeting} superstar! It's {st.session_state.user_name}'s time to shine. What are we working on today?",
        f"Welcome back, {st.session_state.user_name}! You showed up today — and that is already a win. Let's make it count!",
    ]
    speak(random.choice(_greet_msgs))
st.divider()

# ─── DASHBOARD ───────────────────────────────────────────────────────────────
if page == "🏠 Dashboard":
    st.subheader("🏠 Your Dashboard")
    lvl_idx = LEVELS.index(current_level)
    next_lvl = LEVELS[min(lvl_idx+1, len(LEVELS)-1)]
    xp_needed = max(next_lvl[0] - st.session_state.xp, 0)
    st.markdown(f"""
    <div class='flex-card' style='border-left:4px solid #4caf50'>
        <div style='display:flex;justify-content:space-between;align-items:center'>
            <div>
                <div style='font-size:1.05rem;font-weight:700'>{current_level[1]}</div>
                <div style='font-size:0.82rem;color:#888'>{st.session_state.xp} XP · {xp_needed} XP to next level</div>
            </div>
            <div style='font-size:2rem'>{current_level[1].split()[0]}</div>
        </div>
        <div style='background:#252545;border-radius:999px;height:10px;margin-top:0.8rem;overflow:hidden'>
            <div style='height:100%;width:{xp_pct:.0f}%;background:linear-gradient(90deg,#00c853,#00e676);border-radius:999px'></div>
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
    <div class='flex-card' style='text-align:center;padding:1.2rem'>
        <span style='font-size:1.5rem'>💭</span>
        <p style='color:#aaa;font-style:italic;margin:0.5rem 0 0'>{random.choice(QUOTES)}</p>
    </div>
    """, unsafe_allow_html=True)

# ─── CHAT ────────────────────────────────────────────────────────────────────
elif page == "💬 Chat":
    st.subheader("💬 Chat with FlexCoach")
    st.caption(f"{st.session_state.user_name} · {st.session_state.user_age}y · {st.session_state.user_height}cm · {st.session_state.user_weight}kg")

    quick = {
        "💪 Workout":   "Give me a workout plan and exercise routine",
        "🥗 Meal plan": "Give me a 7-day meal plan with recipes",
        "🧘 Meditate":  "Teach me how to meditate and breathe for stress relief",
        "💧 Water tip": "Give me tips to stay hydrated and drink more water",
        "😴 Sleep":     "How can I improve my sleep quality and get better rest",
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
            st.markdown(f'<div class="coach-bubble">💪 {msg["content"]}</div>', unsafe_allow_html=True)

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.spinner("FlexCoach is thinking…"):
            reply = get_chat_response(st.session_state.messages[-1]["content"], profile)
            st.session_state.messages.append({"role":"assistant","content":reply})
            st.session_state.chat_count += 1
            award_xp(XP_REWARDS["chat"], "chat", "chat_10" if st.session_state.chat_count >= 10 else None)
            check_challenge("chat_count")
            # Aria reads the first sentence of the reply
            import re as _re
            _first = _re.split(r'(?<=[.!?])\s', reply.strip(), maxsplit=1)[0]
            speak(_first)
            # Aria reads first sentence of reply
            _first_line = reply.strip().split("\n")[0][:200]
            speak(_first_line)
        st.rerun()

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Ask anything…", label_visibility="collapsed",
                                   placeholder="e.g. What should I eat after a workout?")
        submitted = st.form_submit_button("Send 💪")
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
        st.markdown(f'<div class="flex-card">{reply}</div>', unsafe_allow_html=True)
        if not st.session_state.meal_plan_done:
            st.session_state.meal_plan_done = True
            award_xp(XP_REWARDS["meal_plan"], "meal_plan", "meal_plan_done")
            check_challenge("meal_plan_done")
            show_reward()
        speak_aria("meal", st.session_state.user_name)
        _meal_cheers = [
            f"Fantastic, {st.session_state.user_name}! Your personalised meal plan is ready. You are taking such great care of yourself!",
            f"Nutrition genius alert! {st.session_state.user_name}, you just set yourself up for an amazing week of healthy eating!",
            f"Love your dedication, {st.session_state.user_name}! A great meal plan is the foundation of a healthy life. You are crushing it!",
        ]
        speak(random.choice(_meal_cheers))

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
        st.markdown(f'<div class="flex-card">{reply}</div>', unsafe_allow_html=True)
        if not st.session_state.meditation_done:
            st.session_state.meditation_done = True
            award_xp(XP_REWARDS["meditation"], "meditation", "meditation_done")
            check_challenge("meditation_done")
            show_reward()
        speak_aria("meditation", st.session_state.user_name)
        speak(f"Beautiful, {st.session_state.user_name}. Take a deep breath and follow the guide. You are giving your mind the gift of peace. That is true self-love.")

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
        st.markdown(f'<div class="flex-card">{reply}</div>', unsafe_allow_html=True)
        if not st.session_state.workout_done:
            st.session_state.workout_done = True
            award_xp(XP_REWARDS["workout"], "workout", "workout_done")
            check_challenge("workout_done")
            show_reward()
        speak_aria("workout", st.session_state.user_name)
        _wkt_cheers = [
            f"Yes, {st.session_state.user_name}! Your workout plan is ready. Beast mode activated — let's go!",
            f"I love your commitment, {st.session_state.user_name}! Every rep and every step brings you closer to your goal. You've got this!",
            f"Workout warrior mode on! {st.session_state.user_name}, your body is going to thank you for this. Let's crush it!",
        ]
        speak(random.choice(_wkt_cheers))

# ─── WATER TRACKER ────────────────────────────────────────────────────────────
elif page == "💧 Water Tracker":
    st.subheader("💧 Daily Water Tracker")
    st.markdown(f"Goal: **{WATER_GOAL} glasses/day** ({WATER_GOAL*250} ml) — based on your weight of **{st.session_state.user_weight} kg**")
    count    = st.session_state.water_count
    progress = min(count / WATER_GOAL, 1.0)
    drops_html = "".join(f'<span class="drop {"" if i<count else "empty"}">💧</span>' for i in range(WATER_GOAL))
    st.markdown(
        f'<div class="flex-card" style="text-align:center"><h3>Today\'s intake</h3>{drops_html}'
        f'<p style="margin-top:0.8rem;font-size:1.1rem"><strong>{count}</strong> / {WATER_GOAL} glasses</p></div>',
        unsafe_allow_html=True)
    st.progress(progress)

    col1, col2, col3 = st.columns(3)
    if col1.button("➕ Add glass"):
        if st.session_state.water_count < WATER_GOAL:
            st.session_state.water_count += 1
            award_xp(XP_REWARDS["water_glass"], "water")
            check_challenge("water_count")
            _water_cheers = [
                f"Great job drinking your water, {st.session_state.user_name}! Your body loves you for it.",
                f"Hydration hero in the making! Keep sipping, {st.session_state.user_name}!",
                f"Every glass counts! You are doing brilliantly, {st.session_state.user_name}!",
                f"That is the spirit! One glass at a time, {st.session_state.user_name}!",
            ]
            speak(random.choice(_water_cheers))
            if st.session_state.water_count >= WATER_GOAL and not st.session_state.water_goal_hit_today:
                st.session_state.water_goal_hit_today = True
                award_xp(XP_REWARDS["water_goal"], "water_goal", "water_goal_hit")
                check_challenge("water_goal_hit_today")
                speak(f"Amazing, {st.session_state.user_name}! You hit your full water goal for today! That is absolutely incredible. Your body is thriving!")
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
        st.markdown(f'<div class="flex-card">{get_response("hydration", profile)}</div>', unsafe_allow_html=True)

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
        <div class='flex-card' style='text-align:center'>
            <h2>Your BMI</h2>
            <div style='font-size:3rem;font-weight:700;color:#00e676'>{bmi}</div>
            <span class='bmi-badge {css}'>{cat}</span>
            <p style='margin-top:1rem;color:#aaa'>Healthy range: <strong>18.5 – 24.9</strong></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="flex-card">{get_response("bmi_advice", profile)}</div>', unsafe_allow_html=True)
        if not st.session_state.bmi_logged_today:
            st.session_state.bmi_logged_today = True
            award_xp(XP_REWARDS["bmi_log"], "bmi", "bmi_logged")
            check_challenge("bmi_logged_today")
            show_reward()
        speak(f"Well done, {st.session_state.user_name}! Tracking your BMI is such a smart, data-driven approach to your health. Knowledge is power and you have got plenty of it!")

    if st.session_state.bmi_history:
        st.markdown("#### History")
        for entry in reversed(st.session_state.bmi_history[-10:]):
            _, css = bmi_category(entry["bmi"])
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;padding:0.5rem 0;border-bottom:1px solid #252545">'
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
            <div class='flex-card' style='border-left:4px solid {color}'>
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
                        _med_name = st.session_state.medications[i]["name"]
                        _med_cheers = [
                            f"Well done, {st.session_state.user_name}! You took your {_med_name}. Consistency is your superpower!",
                            f"Perfect! {_med_name} taken. You are so disciplined, {st.session_state.user_name} — keep it up!",
                            f"Yes! Another healthy habit checked off. You are amazing, {st.session_state.user_name}!",
                        ]
                        speak(random.choice(_med_cheers))
                        if all(m.get("taken") for m in st.session_state.medications) and not st.session_state.all_meds_taken_today:
                            st.session_state.all_meds_taken_today = True
                            award_xp(XP_REWARDS["all_meds"], "med", "all_meds_taken")
                            check_challenge("all_meds_taken_today")
                            speak(f"Outstanding, {st.session_state.user_name}! All medications taken for today. You are absolutely nailing your health routine. I am so proud of you!")
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
        st.markdown(f'<div class="flex-card">{tips}</div>', unsafe_allow_html=True)

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
            st.success("Profile updated! 💪"); st.rerun()

    st.divider()
    if st.button("💡 Get my health summary"):
        st.markdown(f'<div class="flex-card">{get_response("general", profile)}</div>', unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.divider()
st.caption("💪 FlexCoach · 100% Free · No API Key needed · Not a substitute for medical advice.")
