import streamlit as st
import openai

# Set up the OpenAI API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def cached_generate_questions(prompt):
    question_prompt = f"Given the essay topic '{prompt}', what are some personal and introspective questions that can help in crafting a detailed and custom essay? Avoid asking for facts or methods."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question_prompt,
        temperature=0.5,
        max_tokens=150
    )
    return [q.strip() for q in response.choices[0].text.split('\n') if q]

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

# Generate questions if not done already
if 'questions' not in st.session_state or essay_prompt != st.session_state.get("previous_prompt", ""):
    st.session_state.questions = cached_generate_questions(essay_prompt)
    st.session_state.previous_prompt = essay_prompt

details = []
for idx, q in enumerate(st.session_state.questions):
    key = f"input_{idx}_{q}"
    answer = st.text_input(q, key=key)
    if answer:
        details.append(answer)

# Ask for word count
word_count = st.number_input("How many words should the essay be?", min_value=100, value=500, step=50)

if st.button("Generate Essay"):
    essay = generate_essay(essay_prompt, details, word_count)
    st.text_area("Generated Essay:", value=essay, height=300)






