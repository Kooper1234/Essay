import streamlit as st
import openai

# Set up the OpenAI API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_essay(prompt, details, word_count):
    detail_string = ". ".join(details)
    essay_prompt = f"Write an essay on the topic: '{prompt}'. Consider the following personal insights: {detail_string}. The essay should be approximately {word_count} words."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=essay_prompt,
        temperature=0.7,
        max_tokens=word_count * 5  # Assuming an average of 5 tokens per word
    )
    return response.choices[0].text.strip()

# Streamlit Interface
st.title('College Essay Generator')

# Get the main essay prompt
essay_prompt = st.text_input('Please enter the general essay prompt or theme:')

# Set of predefined questions
predefined_questions = [
    "What personal experience deeply influenced your viewpoint on this topic?",
    "How has this topic impacted your life or the lives of those around you?",
    "Why is this topic personally significant to you?",
    "Describe a challenge you faced related to this topic and how you overcame it.",
    "What emotions does this topic evoke for you?"
]

details = []
for idx, q in enumerate(predefined_questions):
    key = f"input_{idx}"
    answer = st.text_input(q, key=key)
    if answer:
        details.append(answer)

# Ask for word count
word_count = st.number_input("How many words should the essay be?", min_value=100, value=500, step=50)

if st.button("Generate Essay"):
    essay = generate_essay(essay_prompt, details, word_count)
    st.text_area("Generated Essay:", value=essay, height=300)






