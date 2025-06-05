import streamlit as st
import difflib
import json
import re

# Predefined dataset about Thoughtful AI
THOUGHTFUL_AI_DATA = {
    "questions": [
        {
            "question": "What does the eligibility verification agent (EVA) do?",
            "answer": "EVA automates the process of verifying a patient's eligibility and benefits information in real-time, eliminating manual data entry errors and reducing claim rejections."
        },
        {
            "question": "What does the claims processing agent (CAM) do?",
            "answer": "CAM streamlines the submission and management of claims, improving accuracy, reducing manual intervention, and accelerating reimbursements."
        },
        {
            "question": "How does the payment posting agent (PHIL) work?",
            "answer": "PHIL automates the posting of payments to patient accounts, ensuring fast, accurate reconciliation of payments and reducing administrative burden."
        },
        {
            "question": "Tell me about Thoughtful AI's Agents.",
            "answer": "Thoughtful AI provides a suite of AI-powered automation agents designed to streamline healthcare processes. These include Eligibility Verification (EVA), Claims Processing (CAM), and Payment Posting (PHIL), among others."
        },
        {
            "question": "What are the benefits of using Thoughtful AI's agents?",
            "answer": "Using Thoughtful AI's Agents can significantly reduce administrative costs, improve operational efficiency, and reduce errors in critical processes like claims management and payment posting."
        }
    ]
}

# Generic fallback responses for questions outside the dataset
FALLBACK_RESPONSES = [
    "I'm a specialized assistant for Thoughtful AI's healthcare automation agents. I can help you learn about EVA, CAM, PHIL, and other Thoughtful AI services. Could you ask me something specific about our agents?",
    "I'm designed to assist with questions about Thoughtful AI's automation solutions. Please feel free to ask about our healthcare agents like EVA, CAM, or PHIL.",
    "I specialize in information about Thoughtful AI's healthcare automation agents. How can I help you learn more about our solutions?"
]

class ThoughtfulAIAgent:
    def __init__(self):
        self.questions = [item["question"] for item in THOUGHTFUL_AI_DATA["questions"]]
        self.qa_dict = {item["question"]: item["answer"] for item in THOUGHTFUL_AI_DATA["questions"]}
    
    def normalize_text(self, text):
        """Normalize text for better matching"""
        # Convert to lowercase and remove extra whitespace
        text = text.lower().strip()
        # Remove common punctuation
        text = re.sub(r'[^\w\s]', '', text)
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def find_best_match(self, user_question, threshold=0.4):
        """Find the best matching question using fuzzy string matching"""
        try:
            normalized_user_question = self.normalize_text(user_question)
            normalized_questions = [self.normalize_text(q) for q in self.questions]
            
            # Use difflib to find the best match
            matches = difflib.get_close_matches(
                normalized_user_question, 
                normalized_questions, 
                n=1, 
                cutoff=threshold
            )
            
            if matches:
                # Find the original question corresponding to the best match
                best_match_index = normalized_questions.index(matches[0])
                original_question = self.questions[best_match_index]
                return original_question, self.qa_dict[original_question]
            
            return None, None
            
        except Exception as e:
            st.error(f"Error during question matching: {str(e)}")
            return None, None
    
    def get_response(self, user_question):
        """Get response for user question"""
        if not user_question or not user_question.strip():
            return "Please ask me a question about Thoughtful AI's healthcare automation agents."
        
        # Try to find a match in the predefined dataset
        matched_question, answer = self.find_best_match(user_question)
        
        if answer:
            return answer
        else:
            # Return a random fallback response
            import random
            return random.choice(FALLBACK_RESPONSES)

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        welcome_message = """
        Hello! I'm your Thoughtful AI customer support assistant. 
        
        I can help you learn about our healthcare automation agents:
        - **EVA** (Eligibility Verification Agent)
        - **CAM** (Claims Processing Agent) 
        - **PHIL** (Payment Posting Agent)
        
        What would you like to know about our AI-powered healthcare solutions?
        """
        st.session_state.messages.append({"role": "assistant", "content": welcome_message})
    
    if "agent" not in st.session_state:
        st.session_state.agent = ThoughtfulAIAgent()

def display_chat_history():
    """Display chat message history"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_user_input():
    """Handle user input and generate response"""
    if prompt := st.chat_input("Ask me about Thoughtful AI's healthcare agents..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        try:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.agent.get_response(prompt)
                st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            error_message = f"I apologize, but I encountered an error while processing your question. Please try again. Error: {str(e)}"
            with st.chat_message("assistant"):
                st.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})

def main():
    """Main application function"""
    # Set page configuration
    st.set_page_config(
        page_title="Thoughtful AI Support Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # App header
    st.title("Thoughtful AI Customer Support Assistant")
    st.markdown("---")
    
    # Create two columns for layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display chat history
        display_chat_history()
        
        # Handle user input
        handle_user_input()
    
    with col2:
        # Sidebar information
        st.subheader("💡 What I can help with:")
        st.markdown("""
        - **EVA**: Eligibility verification
        - **CAM**: Claims processing  
        - **PHIL**: Payment posting
        - **General**: Thoughtful AI services
        """)
        
        st.subheader("🔍 Sample Questions:")
        sample_questions = [
            "What does EVA do?",
            "Tell me about CAM",
            "How does PHIL work?",
            "What are the benefits of using Thoughtful AI's agents?"
        ]
        
        for question in sample_questions:
            if st.button(question, key=f"sample_{question}", use_container_width=True):
                # Simulate user asking the sample question
                st.session_state.messages.append({"role": "user", "content": question})
                response = st.session_state.agent.get_response(question)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
        
        # Clear chat button
        st.markdown("---")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            # Re-add welcome message
            welcome_message = """
            Hello! I'm your Thoughtful AI customer support assistant. 
            
            I can help you learn about our healthcare automation agents:
            - **EVA** (Eligibility Verification Agent)
            - **CAM** (Claims Processing Agent) 
            - **PHIL** (Payment Posting Agent)
            
            What would you like to know about our AI-powered healthcare solutions?
            """
            st.session_state.messages.append({"role": "assistant", "content": welcome_message})
            st.rerun()

if __name__ == "__main__":
    main()
