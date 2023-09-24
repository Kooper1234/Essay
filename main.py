import streamlit as st
import openai
import os

# Set the API key (Assuming you've set it in your environment variables on Streamlit Cloud)
openai.api_key = st.secrets["OPENAI_API_KEY"]

if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.questions = []

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def cached_generate_questions(prompt):
    question_prompt = f"Given the essay topic '{prompt}', what are some personal and introspective questions that can help in creating a detailed and custom essay? Avoid asking for facts or methods."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question_prompt,
        temperature=0.5,
        max_tokens=150  # Limiting tokens for generating questions
    )
    return [q.strip() for q in response.choices[0].text.split('\n') if q]

# Streamlit Interface
st.title('College Essay Generator')

# Step 1: Get the main essay prompt
essay_prompt = st.text_input('Please enter the general essay prompt or theme:')

if essay_prompt and not st.session_state.initialized:
    st.session_state.questions = cached_generate_questions(essay_prompt)
    st.session_state.initialized = True


details = []
for idx, q in enumerate(st.session_state.questions):
    key = f"input_{idx}_{q}"  # Create a unique key for each question
    answer = st.text_input(q, key=key)
    if answer:
        details.append(answer)
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

# Step 1: Get the main essay prompt
essay_prompt = st.text_input('Please enter the general essay prompt or theme:')

details = []
if essay_prompt:
    # Step 2: Use AI to generate specific questions based on the main prompt
    questions = generate_questions(essay_prompt)
    
    for q in questions:
        answer = st.text_input(q)
        if answer:
            details.append(answer)

    # Step 3: Ask for word count
    word_count = st.number_input('How many words should the essay be?', min_value=50, max_value=1000, value=500, step=50)
    tokens = int(word_count * 1.5)  # Rough token estimate

    # Step 4: If all details are provided, generate the essay
    if len(details) == len(questions):  # All questions answered
        full_prompt = f"Based on the theme '{essay_prompt}', considering the following specifics: " + ' '.join(details) + "\n\nWrite an essay:\n"
        essay = generate_essay(full_prompt, tokens)
        st.write(essay)






