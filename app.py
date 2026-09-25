import streamlit as st

from diet import (
    bmi_calculator,
    bmi_category,
    bmr_calculator,
    tdee_calculator,
    calorie_target,
    protein_target
)

from rag import search_knowledge
from api import ask_llm


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🏋️",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("AI Health Assistant")

st.write(
    "Personalized wellness assistant powered by "
    "GPT-OSS-120B + RAG."
)


# =========================================================
# SIDEBAR - HEALTH PROFILE
# =========================================================

st.sidebar.header("Your Health Profile")

gender = st.sidebar.selectbox(
    "Gender",
    ["Male", "Female"]
)

age = st.sidebar.slider(
    "Age",
    min_value=10,
    max_value=100,
    value=25
)

weight = st.sidebar.slider(
    "Weight (kg)",
    min_value=30,
    max_value=200,
    value=70
)

height = st.sidebar.slider(
    "Height (cm)",
    min_value=100,
    max_value=250,
    value=170
)

activity = st.sidebar.selectbox(
    "Activity Level",
    [
        "Sedentary",
        "Lightly Active",
        "Moderately Active",
        "Very Active",
        "Extra Active"
    ]
)

goal = st.sidebar.selectbox(
    "Your Goal",
    [
        "Lose Weight",
        "Maintain Weight",
        "Gain Weight"
    ]
)

diet_type = st.sidebar.selectbox(
    "Diet Type",
    [
        "Vegetarian",
        "Non-Vegetarian",
        "Vegan"
    ]
)

allergies = st.sidebar.text_area(
    "Food Allergies",
    "",
    placeholder="Example: peanuts, milk, soy"
)


# =========================================================
# CALCULATIONS
# =========================================================

bmi = bmi_calculator(
    weight,
    height
)

bmi_status = bmi_category(
    bmi
)

bmr = bmr_calculator(
    gender,
    age,
    weight,
    height
)

tdee = tdee_calculator(
    bmr,
    activity
)

calories = calorie_target(
    tdee,
    goal
)

protein = protein_target(
    weight,
    goal
)


# =========================================================
# HEALTH DASHBOARD
# =========================================================

st.header("Health Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "BMI",
    bmi
)

col2.metric(
    "BMR",
    f"{bmr:.0f} kcal"
)

col3.metric(
    "TDEE",
    f"{tdee:.0f} kcal"
)

col4.metric(
    "Daily Calories",
    f"{calories:.0f} kcal"
)

st.info(
    f"**BMI Category:** {bmi_status}  \n"
    f"**Estimated Protein Target:** {protein} g/day"
)


# =========================================================
# PROFILE SUMMARY
# =========================================================

with st.expander("View Health Profile"):

    profile_col1, profile_col2 = st.columns(2)

    with profile_col1:

        st.write(f"**Gender:** {gender}")
        st.write(f"**Age:** {age}")
        st.write(f"**Weight:** {weight} kg")
        st.write(f"**Height:** {height} cm")

    with profile_col2:

        st.write(f"**Activity:** {activity}")
        st.write(f"**Goal:** {goal}")
        st.write(f"**Diet Type:** {diet_type}")
        st.write(
            f"**Food Allergies:** "
            f"{allergies if allergies else 'None reported'}"
        )
        st.write(f"**BMI:** {bmi}")
        st.write(
            f"**Protein Target:** {protein} g/day"
        )


# =========================================================
# AI FEATURES
# =========================================================

st.divider()

tab1, tab2 = st.tabs(
    [
        "🍽️ Diet Recommendations",
        "🤖 AI Health Assistant"
    ]
)


# =========================================================
# TAB 1 - DIET RECOMMENDATION
# =========================================================

with tab1:

    st.header("Personalized Diet Recommendation")

    st.write(
        "Generate a simple one-day diet plan based on "
        "your health profile, diet type, goal and allergies."
    )

    st.caption(
        f"Target: approximately {calories:.0f} kcal/day "
        f"and {protein:.0f} g protein/day"
    )

    if st.button(
        "Get Diet Recommendations",
        type="primary",
        key="diet_button"
    ):

        # -------------------------------------------------
        # RAG SEARCH
        # -------------------------------------------------

        with st.spinner(
            "Searching nutrition knowledge..."
        ):

            try:

                search_query = f"""
Diet Type: {diet_type}

Goal: {goal}

Food Allergy:
{allergies if allergies else "None reported"}

Find useful nutrition information about:

healthy foods,
protein sources,
calories,
breakfast,
morning snacks,
lunch,
evening snacks,
dinner,
meal planning.
"""

                documents = search_knowledge(
                    search_query,
                    k=4
                )

                context = "\n\n".join(
                    [
                        doc.page_content
                        for doc in documents
                    ]
                )

            except Exception as e:

                context = ""

                st.warning(
                    f"Knowledge base unavailable: {e}"
                )


        # -------------------------------------------------
        # DIET RECOMMENDATION PROMPT
        # -------------------------------------------------

        diet_prompt = f"""
You are a helpful AI nutrition assistant.

Use the following nutrition knowledge
to create a simple one-day diet plan.

NUTRITION KNOWLEDGE:

{context}


USER INFORMATION:

Age: {age}

Gender: {gender}

Height: {height} cm

Weight: {weight} kg

Activity Level: {activity}

Goal: {goal}

Diet Type: {diet_type}

Food Allergy:
{allergies if allergies else "None reported"}

Estimated BMI: {bmi}

Estimated BMR: {bmr} kcal/day

Estimated TDEE: {tdee} kcal/day

Estimated Daily Calorie Target:
{calories} kcal/day

Estimated Protein Target:
{protein} g/day


CREATE THE FOLLOWING:

1. Breakfast
2. Morning Snack
3. Lunch
4. Evening Snack
5. Dinner


FOR EVERY MEAL PROVIDE:

- Food
- Portion
- Approximate calories
- Approximate protein


IMPORTANT RULES:

- Respect the user's diet type.

- Do not recommend foods containing
  the stated allergy.

- If the allergy information is unclear,
  do not assume that a food is safe.

- For packaged or processed foods,
  advise checking the ingredient label
  when allergens may be present.

- Use the provided nutrition knowledge
  when possible.

- Keep the plan simple and practical.

- Calorie and protein values are estimates.

- Do not diagnose diseases.

- Do not prescribe medicines.

- Do not claim to cure diseases.

- Do not claim that this plan is
  a medical prescription.

- This is general wellness information,
  not medical advice.
"""

        diet_messages = [
            {
                "role": "system",
                "content": diet_prompt
            },
            {
                "role": "user",
                "content": (
                    "Create my personalized "
                    "one-day diet plan."
                )
            }
        ]

        # -------------------------------------------------
        # GENERATE DIET PLAN
        # -------------------------------------------------

        with st.spinner(
            "AI is creating your personalized diet plan..."
        ):

            try:

                diet_answer = ask_llm(
                    diet_messages
                )

                st.success(
                    "Personalized diet plan generated."
                )

                st.markdown(
                    diet_answer
                )

            except Exception as e:

                st.error(
                    "Diet recommendation generate "
                    f"nahi ho saki.\n\nError: {e}"
                )


# =========================================================
# TAB 2 - AI HEALTH ASSISTANT
# =========================================================

with tab2:

    st.header("AI Nutrition Assistant")

    st.caption(
        "Ask questions about nutrition, protein, calories, "
        "vegetarian foods, meal planning and wellness."
    )

    # -----------------------------------------------------
    # QUESTION BOX
    # -----------------------------------------------------

    question = st.text_area(
        "Ask About Health and Nutrition",
        placeholder=(
            "e.g. Good vegetarian sources of protein"
        ),
        height=120
    )

    # -----------------------------------------------------
    # ASK AI BUTTON
    # -----------------------------------------------------

    if st.button(
        "Ask AI",
        type="primary",
        key="ask_ai_button"
    ):

        if not question.strip():

            st.warning(
                "Please enter a health or nutrition question."
            )

        else:

            # ---------------------------------------------
            # RAG SEARCH
            # ---------------------------------------------

            with st.spinner(
                "Searching nutrition knowledge..."
            ):

                try:

                    documents = search_knowledge(
                        question,
                        k=4
                    )

                    context = "\n\n".join(
                        [
                            doc.page_content
                            for doc in documents
                        ]
                    )

                except Exception as e:

                    context = ""

                    st.warning(
                        f"Knowledge base unavailable: {e}"
                    )


            # ---------------------------------------------
            # CHATBOT PROMPT
            # ---------------------------------------------

            chatbot_prompt = f"""
You are an AI health and nutrition assistant.

Use the following knowledge to answer
the user's question.

NUTRITION KNOWLEDGE:

{context}


USER INFORMATION:

Age: {age}

Gender: {gender}

Height: {height} cm

Weight: {weight} kg

Activity Level: {activity}

Goal: {goal}

Diet Type: {diet_type}

Food Allergy:
{allergies if allergies else "None reported"}

Estimated BMI: {bmi}

Estimated BMR: {bmr} kcal/day

Estimated TDEE: {tdee} kcal/day

Estimated Daily Calorie Target:
{calories} kcal/day

Estimated Protein Target:
{protein} g/day


USER QUESTION:

{question}


INSTRUCTIONS:

- Answer clearly.

- Keep the explanation beginner-friendly.

- Use the provided knowledge when possible.

- Do not invent medical facts.

- Do not diagnose diseases.

- Do not prescribe medicines.

- Do not claim to cure diseases.

- Respect the user's diet type.

- Do not recommend foods containing
  the stated food allergy.

- If the allergy information is unclear,
  do not assume that a food is safe.

- Treat BMI, BMR, TDEE, calorie and
  protein values as estimates.

- If the question concerns a serious
  medical problem, recommend consulting
  a qualified healthcare professional.

- If the knowledge base does not contain
  enough information to answer confidently,
  say so instead of inventing an answer.

This application provides general health
and nutrition information for educational
and wellness purposes.

This is not a substitute for professional
medical advice.
"""


            # ---------------------------------------------
            # SEND TO LLM
            # ---------------------------------------------

            messages = [
                {
                    "role": "system",
                    "content": chatbot_prompt
                },
                {
                    "role": "user",
                    "content": question
                }
            ]


            with st.spinner(
                "AI is preparing your answer..."
            ):

                try:

                    answer = ask_llm(
                        messages
                    )

                    st.subheader("AI Response")

                    st.markdown(
                        answer
                    )

                except Exception as e:

                    st.error(
                        "AI response generate nahi ho saka.\n\n"
                        f"Error: {e}"
                    )


# =========================================================
# DISCLAIMER
# =========================================================

st.divider()

st.caption(
    "This application provides general wellness and "
    "nutrition information and is not a substitute for "
    "professional medical advice."
)