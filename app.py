import os
import streamlit as st
from Claude import Claude
import re

class TosterApp:
    def __init__(self):
        self.history = []
        self.claude = Claude()

    def is_legal_text(self, text):
        legal_keywords = ['terms and conditions', 'terms of use', 'privacy policy', 'acceptable use policy', 'user agreement', 'tos', 'tou', 't&c', 't&cs', 'end-user license agreement','eula','licence', 'agreement', 'agreements', 'disclaimer', 'party', 'parties', 'policy', 'liability', 
                          'indemnify', 'jurisdiction', 'binding', 'governing law'] 
        text_lower = text.lower()
        return any(re.search(r'\b' + kw + r'\b', text_lower) for kw in legal_keywords)

    def analyze_text_with_claude(self, text, prompt):
        # Check if the text seems like a legal agreement
        if not self.is_legal_text(text):
            return "The provided text does not seem to be a legal agreement."

        user_prompt = prompt + text

        # Add user's prompt to history
        self.history.append(user_prompt)
        # Join all history with AI prompt
        joined_history = ''.join(self.history) + "\n\nAssistant:"

        try:
            # Get Claude's response
            response_text = self.claude.response(joined_history)
            response_text_with_disclaimer = response_text + "\n\nToster provides AI-driven insights powered by Anthropic's Claude. Consult legal, ethical, and privacy experts for professional advice."
            self.history.append(f"\n\nAssistant: {response_text_with_disclaimer}")
            
            return response_text_with_disclaimer
        except Exception as e:
            return str(e)

# Streamlit interface
def main():
    # Extract API key and prompt from secrets
    user_prompt = st.secrets["multi_line"]["prompt"]

    toster = TosterApp()

    # New look and feel
    st.image('toster_logo.png', width=50)
    st.title('Toster')
    st.markdown("User agreements made clear.")

    user_input = st.text_area("Paste entire ToS, Privacy Policy, or any other user agreement here")

    if st.button('Decode'):
        with st.spinner('Decoding the text...'):
            try:
                result = toster.analyze_text_with_claude(user_input, user_prompt)
                st.write(result)
                st.markdown("[Decode Another Agreement](/)")
            except Exception as e:
                st.error(f'An error occurred: {str(e)}')

if __name__ == "__main__":
    main()
