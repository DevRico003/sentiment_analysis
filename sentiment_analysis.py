# Import required libraries
import openai  # OpenAI's GPT model
import os  # to interact with the OS
from dotenv import load_dotenv, find_dotenv  # to load environment variables
import streamlit as st  # web app framework

# This function uses OpenAI's GPT model to classify text sentiment.
def gpt_classify_sentiment(prompt, emotions):
    # We instruct the model to classify the sentiment based on the provided emotions.
    system_prompt = f'''You are an emotionally intelligent assistant.
    Classify the sentiment if the user's text with ONLY ONE OF THE FOLLOWING EMOTIONS: {emotions}.
    After classifying the text, respond with the emotion ONLY.'''
    
    # Generate a response from the model.
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ],
        max_tokens=20,
        temperature=0
    )

    # Extract the content of the response
    r = response['choices'][0].message.content

    # If the response is empty, return 'N/A'.
    if r == '':
        r ='N/A'

    return r

# Start of the main program
if __name__ == '__main__':
    # Load the OpenAI API key from the .env file
    load_dotenv(find_dotenv(), override=True)
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Setup Streamlit web interface
    # Create two columns for the UI layout
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        st.title('Zero-Shot Sentiment Analysis')  # Title of the web page
    with col2:
        st.image('ai.png', width=70)  # Display an image

    # Form for user inputs
    with st.form(key='my_form'):
        # Define default emotions
        default_emotions = 'positive, negative, neutral'
        # Text input for emotions
        emotions = st.text_input('Emotions: ', value=default_emotions)

        # Text area for the text to be classified
        text = st.text_area(label='Text to classify: ')
        # Submit button
        submit_button = st.form_submit_button(label='Check!')

        # If the submit button is pressed
        if submit_button:
            # Classify the sentiment of the text
            emotion = gpt_classify_sentiment(text, emotions)
            result = f'{text} => {emotion} \n'
            st.write(result)  # Display the result

            st.divider()  # Divider line

            # Saving the History of results
            if 'history' not in st.session_state:
                if result:
                    st.session_state['history'] = result
                else:
                    st.session_state['history'] = ''
            else:
                st.session_state['history'] += result

            # Display history if it exists
            if st.session_state['history']:
                st.text_area(label='History', value=st.session_state['history'], height=400)