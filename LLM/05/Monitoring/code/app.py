import streamlit as st

from assistant import create_assistant
from db_save import save_conversation
from db_feedback import save_feedback
from judge import evaluate_relevance


assistant = create_assistant()

st.title("Course Assistant")

user_input = st.text_input("Enter your question:")

if st.button("Ask"):
    with st.spinner("Processing..."):
        answer = assistant.rag(user_input)
        st.success("Completed!")
        st.write(answer)

        record = assistant.last_call
        st.write(f"Response time: {record.response_time:.2f}s")
        st.write(f"Prompt tokens: {record.prompt_tokens}")
        st.write(f"Completion tokens: {record.completion_tokens}")
        st.write(f"Cost: ${record.cost:.4f}")

        try:
            conversation_id = save_conversation(record, user_input, "llm-zoomcamp")
            st.session_state.conversation_id = conversation_id
        except Exception as e:
            st.info(f"DB save skipped (PostgreSQL not running): {e}")

        try:
            relevance, explanation = evaluate_relevance(user_input, answer)
            if "conversation_id" in st.session_state:
                save_feedback(
                    st.session_state.conversation_id,
                    "judge",
                    relevance=relevance,
                    explanation=explanation,
                )
            st.write(f"Relevance: {relevance}")
            st.write(f"Explanation: {explanation}")
        except Exception as e:
            st.warning(f"Judge skipped: {e}")


col1, col2 = st.columns(2)
with col1:
    if st.button("+1"):
        if "conversation_id" not in st.session_state:
            st.warning("No saved conversation yet (DB not available).")
        else:
            try:
                save_feedback(st.session_state.conversation_id, "user", score=1)
                st.write("Thanks!")
            except Exception as e:
                st.warning(f"Feedback not saved: {e}")

with col2:
    if st.button("-1"):
        if "conversation_id" not in st.session_state:
            st.warning("No saved conversation yet (DB not available).")
        else:
            try:
                save_feedback(st.session_state.conversation_id, "user", score=-1)
                st.write("Thanks for the feedback!")
            except Exception as e:
                st.warning(f"Feedback not saved: {e}")
