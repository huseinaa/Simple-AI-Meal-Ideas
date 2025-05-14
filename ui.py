import re
import streamlit as st
from SimplerLLM.language.llm import LLM, LLMProvider

st.set_page_config(
    page_title="AI Meal Planner",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🥗 AI Meal Planner")
st.markdown("""
Provide details about your meal preferences, and get customized ideas instantly.
""")

with st.form("meal_form"):
    meal = st.selectbox("Meal of the Day", ["Breakfast", "Lunch", "Dinner", "Snack"], index=1)
    ingredients = st.text_area(
        "Ingredients Available", placeholder="e.g., chicken, avocado, mixed greens, tomatoes, lemon, tuna, cucumber, chickpeas, basic fruits, rice)"
    )
    specifications = st.text_input("Extra Specifications", placeholder="e.g., high protein, vegetarian, salad")
    submitted = st.form_submit_button("Generate Meal Ideas")

gemini_llm_instance = LLM.create(provider=LLMProvider.GEMINI, model_name="gemini-1.5-flash")
openai_llm_instance = LLM.create(provider=LLMProvider.OPENAI, model_name="gpt-4o-mini")

prompt = """
##Instruction
You are an expert in meal planning. Your task is to help me with meal plan ideas based on inputs ill provide delimited between triple backticks in the inputs section which are:
- the meal of the day i want ideas for
- the ingredients available in my house which i can make a meal out of
- any specfications i have for the meal like high protein, vegan, vegeterian, italian, salad, etc...

You should provide me with 3 meal ideas using only the ingredients provided in the inputs, and you can think that the basic ingredients and spices are already provided, but the main ingredients of the meal should be using the ingredients in the input. Keep in mind that you may not need all the ingredients in every meal you can play with them to get delicious various meals.
After that you have to provide another 3 meal ideas which are like the above using the base ingredients, and you may add some ingredients that arent provided to give delicious new meal ideas.
So in total i should have 6 meal ideas, where all of them should be well spiced and delicious; nothing bland.

##Inputs
Meal of the Day: {meal}
Ingredients Available: {ingredients}
Extra Specifications: {specifications}

##Output
The ouput should only be the 6 meal plan ideas with the respective ingredients used, and a very simple short structured instructions to how we can do it, and nothing else in the following format:
1. Meal Name
    **Ingredients:**
    **Instructions:**

2. Meal Name
    **Ingredients:**
    **Instructions:**

3. Meal Name
    **Ingredients:**
    **Instructions:**

4. Meal Name
    **Ingredients:**
    **Instructions:**

5. Meal Name
    **Ingredients:**
    **Instructions:**

6. Meal Name
    **Ingredients:**
    **Instructions:**
"""

def format_response(raw_response):
    raw_response = re.sub(r'^\s*1\.\s*', '', raw_response)
    meal_blocks = re.split(r'(?<=\n)\d\. ', raw_response)
    formatted = ""
    for i, block in enumerate(meal_blocks):
        if block.strip():
            formatted += f"### {i+1}. " + block.strip().replace("**Ingredients:**", "\n**Ingredients:**").replace("**Instructions:**", "\n**Instructions:**") + "\n\n"
    return formatted

if submitted:
    with st.spinner("Generating delicious ideas..."):
        final_prompt = prompt.format(meal=meal, ingredients=ingredients, specifications=specifications)
        try:
            response = gemini_llm_instance.generate_response(prompt=final_prompt, max_tokens=500)
            st.success("Here are your meal plan ideas!")
            st.markdown(format_response(response), unsafe_allow_html=True)
        except Exception as e:
            for attempt in range(1, 4):
                try:
                    response = openai_llm_instance.generate_response(prompt=final_prompt, max_tokens=500)
                    st.success("Here are your meal plan ideas!")
                    st.markdown(format_response(response), unsafe_allow_html=True)
                    break
                except Exception as oe:
                    if attempt == 3:
                        st.error(f"All attempts failed. Please try again later.")