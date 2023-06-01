import os
import streamlit as st
import anthropic
import asyncio

history = []

async def analyze_text_with_claude(text):
    c = anthropic.Client(os.getenv('CLAUDE_API_KEY'))

    # Add user's text to history
    history.append(f"\n\nHuman: From your standpoint as an expert in ethics, data privacy, and legal matters, meticulously dissect the following user agreement. Expose potential risks including, but not limited to, data collection, user content rights, advertising, tracking, third-party sharing, dangerous clauses, limitations of liability, arbitration clauses, changes of terms, and waiver of class-action rights. Present a concise one-paragraph overview outlining the main risks and potential consequences for users right at the beginning. Then, break down each risk in detail in separate paragraphs. Each issue should have its dedicated explanation. Finally, express a strong concluding statement reflecting your overall assessment. Here's the document: {text}")
    # Join all history with AI prompt
    joined_history = ''.join(history) + "\n\nAssistant:"

    resp = await c.acompletion(
        prompt=joined_history,
        stop_sequences=['Human:'],
        model="claude-v1",
        max_tokens_to_sample=500,
        temperature=0.3
    )

    # Add Claude's response to history
    response_text = resp['completion']
    response_text_with_disclaimer = response_text + "\n\nToster provides AI-driven insights powered by Anthropic's Claude. Consult legal, ethical, and privacy experts for professional advice."
    history.append(f"\n\nAssistant: {response_text_with_disclaimer}")
    
    return response_text_with_disclaimer



# New look and feel
st.image('toster_logo.png', width=50)  # Adjust width as necessary  # Assumes you have a logo image named 'toster_logo.png'
st.title('Toster')
st.markdown("User agreements made clear.")

user_input = st.text_area("Paste entire ToS, Privacy Policy, or any other user agreement here")  # Change from text input to text area

if st.button('Decode'):  # Rename the button
    with st.spinner('Decoding the text...'):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(analyze_text_with_claude(user_input))
        st.write(result)

