import os
import streamlit as st
import anthropic
import asyncio
import re

st.set_page_config(
   page_title="Toster",
   page_icon="🧊",
   layout="centered",
   initial_sidebar_state="expanded",
)

class TosterApp:
    def __init__(self):
        self.history = []
        self.api_key = st.secrets["secrets"]["CLAUDE_API_KEY"]
        self.client = anthropic.Client(self.api_key)

    def is_legal_text(self, text):
        legal_keywords = ['terms and conditions', 'terms of use', 'privacy policy', 'acceptable use policy', 'user agreement', 'tos', 'tou', 't&c', 't&cs', 'end-user license agreement','eula','licence', 'agreement', 'agreements', 'disclaimer', 'party', 'parties', 'policy', 'liability', 
                          'indemnify', 'jurisdiction', 'binding', 'governing law'] 
        text_lower = text.lower()
        return any(re.search(r'\b' + kw + r'\b', text_lower) for kw in legal_keywords)

    async def analyze_text_with_claude(self, text, prompt):
        # Check if the text seems like a legal agreement
        if not self.is_legal_text(text):
            return "The provided text does not seem to be a legal agreement."

        user_prompt = prompt + text

        # Add user's prompt to history
        self.history.append(user_prompt)
        # Join all history with AI prompt
        joined_history = ''.join(self.history) + "\n\nAssistant:"

        try:
            resp = await self.client.acompletion(
                prompt=joined_history,
                stop_sequences=['Human:'],
                model="claude-v1",
                max_tokens_to_sample=700,
                temperature=0.3
            )

            # Add Claude's response to history
            response_text = resp['completion']
            response_text_with_disclaimer = response_text + "\n\nToster provides AI-driven insights powered by Anthropic. Consult a legal expert for professional advice."
            self.history.append(f"\n\nAssistant: {response_text_with_disclaimer}")
            
            return response_text_with_disclaimer
        except Exception as e:
            return str(e)

# Streamlit interface
def main():
    # Extract prompt from secrets
    user_prompt = st.secrets["multi_line"]["prompt"]

    toster = TosterApp()

    # New look and feel 
    st.title(':bookmark_tabs: Toster')
    st.markdown("User agreements made clear.")

    user_input = st.text_area("Paste entire ToS, Privacy Policy, or any other user agreement here")

    if st.button('Decode'):
        with st.spinner('Decoding the text. A glass of water and deep breaths will prepare you best for what comes next.'):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(toster.analyze_text_with_claude(user_input, user_prompt))
                st.write(result)
                st.markdown("[Decode Another Agreement](/)")
            except Exception as e:
                st.error(f'An error occurred: {str(e)}')

if __name__ == "__main__":
    main()
