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

st.write('Let\'s gather some information to create a personalized college essay for you.')

# Questions for the user
name = st.text_input('What\'s your name?')
hobby = st.text_input('Describe a hobby or activity you are passionate about:')
achievement = st.text_input('Mention a significant achievement or experience you had:')
lesson_learned = st.text_input('Describe a lesson you learned from a challenging experience:')
future_goals = st.text_input('What are your future goals or aspirations?')
word_count = st.number_input('How many words should the essay be?', min_value=50, max_value=1000, value=500, step=50)

# Convert word count to approximate tokens. This is a rough estimate.
tokens = int(word_count * 1.5)  # Assuming each word translates to around 1.5 tokens

# Generating the prompt based on user's input
if all([name, hobby, achievement, lesson_learned, future_goals]):
    full_prompt = f"Write a college essay that incorporates the following details: \
                    \n- A student named {name} who is passionate about {hobby}. \
                    \n- They had a significant experience where {achievement}. \
                    \n- From a challenging situation, they learned that {lesson_learned}. \
                    \n- In the future, they aspire to {future_goals}. \
                    \n\nBegin the essay:\n"

    # Fetch the generated essay
    essay = generate_essay(full_prompt, tokens)
    st.write(essay)
else:
    st.write('Please answer all the questions to generate your essay.')
