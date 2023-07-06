import openai
import os
from dotenv import load_dotenv, find_dotenv
import streamlit as st

#main function
def gpt_classify_sentiment(prompt, emotions):
    system_prompt = f'''You are an emotionally intelligent assistant.
    Classify the sentiment if the user's text with ONLY ONE OF THE FOLLOWING EMOTIONS: {emotions}.
    After classifying the text, respond with the emotion ONLY.'''
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ],
        max_tokens=20,
        temperature=0
    )

    r = response['choices'][0].message.content

    if r == '':
        r ='N/A'

    return r

#streamlit frontend
if __name__ == '__main__':
    #loading OpenAI API-Key
    load_dotenv(find_dotenv(), override=True)
    openai.api_key = os.getenv('OPENAI_API_KEY')

    #frontend
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        st.title('Zero-Shot Sentiment Analysis')
    with col2:
        st.image('ai.png', width=70)

    with st.form(key='my_form'):
        default_emotions = 'positive, negative, neutral'
        emotions = st.text_input('Emotions: ', value=default_emotions)

        text = st.text_area(label='Text to classify: ')
        submit_button = st.form_submit_button(label='Check!')

        if submit_button:
            emotion = gpt_classify_sentiment(text, emotions)
            result = f'{text} => {emotion} \n'
            st.write(result)

            st.divider()

            #saving the History
            if 'history' not in st.session_state:
                if result:
                    st.session_state['history'] = result
                else:
                    st.session_state['history'] = ''
            else:
                st.session_state['history'] += result

            if st.session_state['history']:
                st.text_area(label='History', value=st.session_state['history'], height=400)