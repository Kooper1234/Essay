import streamlit as st
import openai
openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_essay(prompt, max_tokens):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=max_tokens
    )
    return response.choices[0].text.strip()

# Streamlit Interface
st.title('College Essay Generator')

# Step 1: Get the general essay prompt from the user
essay_prompt = st.text_input('Please enter the general essay prompt or theme:')

if essay_prompt:
    # Step 2: Break down the prompt into specifics
    st.write('Help us understand more about your prompt for a personalized essay.')
    
    detail_1 = st.text_input(f"Elaborate on a specific point related to '{essay_prompt}' (e.g., a personal experience, a particular aspect, etc.):")
    detail_2 = st.text_input(f"Describe any additional aspect or perspective you'd like to cover related to '{essay_prompt}':")
    detail_3 = st.text_input(f"Is there a takeaway or lesson you want to be highlighted in relation to '{essay_prompt}'?")

    # Step 3: Ask for word count
    word_count = st.number_input('How many words should the essay be?', min_value=50, max_value=1000, value=500, step=50)
    tokens = int(word_count * 1.5)  # Rough token estimate

    # Step 4: If all details are provided, generate the essay
    if all([detail_1, detail_2, detail_3]):
        full_prompt = f"Based on the theme '{essay_prompt}', considering the following specifics: \
                        \n1. {detail_1} \
                        \n2. {detail_2} \
                        \n3. {detail_3} \
                        \n\nWrite an essay:\n"

        essay = generate_essay(full_prompt, tokens)
        st.write(essay)







