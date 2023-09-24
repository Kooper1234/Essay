openai.api_key = 'OPENAI_API_KEY'
import streamlit as st
import openai

def generate_essay(prompt):
    response = openai.Completion.create(
      engine="text-davinci-003", 
      prompt=prompt, 
      max_tokens=500  # Limiting to 500 tokens for this example. Adjust as needed.
    )
    return response.choices[0].text.strip()

# Streamlit UI
st.title('College Essay Generator')

# Get user info
name = st.text_input('Name:')
about = st.text_area('Tell something about yourself:')
essay_prompt = st.text_area('Essay Prompt:')

if st.button('Generate Essay'):
    # Construct the prompt for OpenAI
    full_prompt = f"Based on the information: \nName: {name}\nAbout: {about}\nThe essay prompt is: {essay_prompt}\n\nEssay:\n"
    essay = generate_essay(full_prompt)
    st.text_area('Generated Essay:', essay)
