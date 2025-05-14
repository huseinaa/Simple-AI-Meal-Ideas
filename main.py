from SimplerLLM.language.llm import LLM, LLMProvider

gemini_llm_instance = LLM.create(provider=LLMProvider.GEMINI, model_name="gemini-1.5-flash")
openai_llm_instance = LLM.create(provider=LLMProvider.OPENAI, model_name="gpt-4o-mini")

meal = "Lunch"
ingredients = "chicken, avocado, mixed greens, basic vegetables (tomatoes, lemon, cucumber), chickpeas, tuna, basic fruits, rice"
specifications = "high protein low calorie"

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
The ouput should only be the 6 meal plan ideas with the respective ingredients used, and a simple 2-3 line structured instructions to how we can do it, and nothing else in the following format:
1. Meal Name
    **Ingredients: **
    **Instructions: **

2. Meal Name
    **Ingredients: **
    **Instructions: **

3. Meal Name
    **Ingredients: **
    **Instructions: **

4. Meal Name
    **Ingredients: **
    **Instructions: **

5. Meal Name
    **Ingredients: **
    **Instructions: **

6. Meal Name
    **Ingredients: **
    **Instructions: **
"""

final_prompt = prompt.format(meal=meal, ingredients=ingredients, specifications=specifications)

try:
    gemini_response = gemini_llm_instance.generate_response(prompt=final_prompt, max_tokens=600)
    print(gemini_response)
except Exception as e:
    print(f"Gemini failed with error: {e}")
    for attempt in range(1, 4):
        try:
            openai_response = openai_llm_instance.generate_response(prompt=final_prompt, max_tokens=600)
            print(f"OpenAI response (attempt {attempt}): {openai_response}")
            break
        except Exception as oe:
            print(f"OpenAI attempt {attempt} failed with error: {oe}")