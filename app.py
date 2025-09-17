import streamlit as st
import openai 
import json
import time

# --- Configuration ---
st.set_page_config(page_title="Local LM Book Crafter", layout="wide", initial_sidebar_state="expanded")

# --- Local LM Server Setup ---
try:
    client = openai.OpenAI(
        base_url="URL_HERE",
        api_key="local-key"
    )
    client.models.list()
    st.sidebar.success("✅ Connected to Local LM Server")
except openai.APIConnectionError as e:
    st.error(f"🚨 Failed to connect to Local LM Server at http://127.0.0.1:1234/v1")
    st.error(f"Please ensure your local server is running and accessible. Details: {e.__cause__}")
    st.stop()
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
    st.stop()

# --- Initialize Session State ---
if 'book_content' not in st.session_state:
    st.session_state.book_content = ""
if 'start_generation' not in st.session_state:
    st.session_state.start_generation = False
if 'concept' not in st.session_state:
    st.session_state.concept = ""
if 'num_sections' not in st.session_state:
    st.session_state.num_sections = 10

# --- Core Book Generation Functions ---

def make_local_lm_request(prompt):
    """Handles requests to the Local LM Server with OpenAI's library."""
    try:
        messages = [{"role": "user", "content": prompt}]
        
        request_params = {
            "model": "local-model",
            "messages": messages,
            "temperature": 0.65, 
        }
        
        response = client.chat.completions.create(**request_params)
        return response.choices[0].message.content.strip()

    except Exception as e:
        st.error(f"API Request Failed: {e}")
        time.sleep(2)
        return None

def extract_json_from_response(response_text):
    """More robustly extracts a JSON list from a model's text response."""
    try:
        start = response_text.find('[')
        end = response_text.rfind(']') + 1
        if start != -1 and end != 0:
            json_str = response_text[start:end]
            return json.loads(json_str)
        else:
            return None
    except json.JSONDecodeError:
        return None

def step_1_planning(concept, num_sections):
    """Step 1: Create a structured outline of strategic principles."""
    with st.spinner("Step 1: Architecting the book's structure... 🧠"):
        prompt = f"""
        You are a master strategist and editor like Aristotle mentoring a great leader. Analyze the following core concept and break it down into a logical sequence of exactly {num_sections} core principles.
        These principles must be aphoristic, concise, and profound, suitable for a timeless strategy book. They should build upon each other logically.

        **Core Concept:**
        ---
        {concept}
        ---

        Return ONLY a JSON-formatted list of strings. Each string is a chapter title/principle. The JSON must start with '[' and end with ']'.
        """
        response_text = make_local_lm_request(prompt)
        if response_text is None: return None
        
        plan = extract_json_from_response(response_text)
        
        if plan and isinstance(plan, list) and all(isinstance(item, str) for item in plan):
            st.success("✔ Step 1: Book architecture complete.")
            with st.expander("View Generated Principles"):
                for i, principle in enumerate(plan):
                    st.markdown(f"**Principle {i+1}:** {principle}")
            return plan
        else:
            st.error("Error: The AI failed to generate a valid JSON outline.")
            st.text_area("Model Response to Debug:", response_text, height=200)
            return None

def step_2_generation_loop(outline, concept):
    """
    Step 2: A smarter, hybrid-memory generation loop.
    - Provides focused context to prevent token overflow and repetition.
    - Uses a look-ahead to avoid covering future topics prematurely.
    """
    st.info("Initiating chapter generation with a hybrid-memory protocol...")
    
    # These lists will store the raw text for our memory system
    all_chapters_full_text = []
    all_chapters_summary = []
    
    # This list will store the final, formatted chapters for the book
    final_book_chapters = []
    
    progress_bar = st.progress(0, text="Starting...")

    for i, principle in enumerate(outline):
        progress_value = (i + 1) / len(outline)
        progress_text = f"Writing Chapter {i+1}: '{principle}'..."
        progress_bar.progress(progress_value, text=progress_text)
        
        with st.spinner(progress_text):
            # --- CONSTRUCT THE FOCUSED, HYBRID MEMORY (to stay under the token limit) ---
            
            # 1. The full text of the last chapter for immediate context.
            previous_chapter_text = all_chapters_full_text[-1] if i > 0 else "This is the first chapter. There is no preceding text."
            
            # 2. The summaries of the last 2-3 chapters for recent context.
            recent_summaries = "\n".join(all_chapters_summary[-3:]) if i > 0 else "N/A"
            
            # 3. The titles of the next few chapters to avoid overlap.
            look_ahead_titles = "\n".join(f"- {p}" for p in outline[i+1:i+4]) if i < len(outline) - 1 else "This is the final section of the main body."

            # 4. Construct the prompt
            writing_prompt = f"""
            You are a master strategist and philosopher. Your writing style is direct, profound, and timeless, like Marcus Aurelius or Sun Tzu.
            
            **WRITING INSTRUCTIONS:**
            - Write in short, declarative sentences. State principles directly.
            - Do not use modern business jargon. Write as if you are a philosopher from 2000 years ago.
            - NEVER use the first-person "I".
            - Do NOT use repetitive introductory phrases ("In this chapter...").
            - The tone should be authoritative and wise.

            **CONTEXT & YOUR TASK:**

            1.  **Book's Core Philosophy:** {concept}

            2.  **Full Book Outline:**
                {chr(10).join(f"{idx+1}. {p}" for idx, p in enumerate(outline))}

            3.  **Recent Chapter Summaries (What you just wrote about):**
                {recent_summaries}
            
            4.  **Full Text of Preceding Chapter (Chapter {i}):**
                ---
                {previous_chapter_text}
                ---

            5.  **Upcoming Chapter Topics (Do NOT cover these in detail now):**
                {look_ahead_titles}

            **YOUR CURRENT CHAPTER:**
            Based on all the context above, write a concise and powerful chapter (200-300 words) for the principle: **"{i+1}. {principle}"**.
            Ensure it flows logically from the preceding chapter but stands as its own powerful lesson. Do not repeat concepts from the recent summaries.
            """
            
            generated_text = make_local_lm_request(writing_prompt)
            if generated_text is None: 
                st.error(f"Failed to write Chapter {i+1}. Aborting."); return None
            
            # Add the raw text to our memory list for the next loop
            all_chapters_full_text.append(generated_text)
            
            # Generate and store a summary for the next loop's memory
            summary_prompt = f"Summarize the core message of this text in one single, concise sentence: \n\n{generated_text}"
            chapter_summary = make_local_lm_request(summary_prompt)
            if chapter_summary:
                all_chapters_summary.append(f"Chapter {i+1} ({principle}): {chapter_summary}")
            
            # Store the final, formatted chapter for the book output
            chapter_content = f"### {i+1}. {principle}\n\n{generated_text}"
            final_book_chapters.append(chapter_content)

    progress_bar.empty()
    st.success("✔ Step 2: All chapters generated with hybrid-context memory.")
    return "\n\n---\n\n".join(final_book_chapters)

def step_3_add_conclusion_and_references(book_text, concept, outline):
    """Step 3: Write a concluding chapter and a 'Further Reading' section."""
    with st.spinner("Step 3: Writing conclusion and citing historical precedents... 📜"):
        prompt = f"""
        You are a historical scholar and senior editor. Your task is to provide two final sections for a strategy book, matching its timeless, philosophical tone.

        **Core Philosophy of the Book:**
        {concept}

        **Book Outline (Principles Covered):**
        {', '.join(outline)}
        ---
        **Full Book Text:**
        {book_text}
        ---

        **Your Tasks:**
        1.  **Concluding Chapter:** Write a brief, powerful concluding chapter titled "### On Mastery and the Path Forward". It should synthesize the core philosophy into a final, memorable thought.
        2.  **References Section:** Write a section titled "### Historical Precedents & Further Reading". Suggest classic texts (e.g., from Stoicism, military history), historical events, or philosophical concepts that parallel the strategies discussed.
        """
        final_sections = make_local_lm_request(prompt)
        if final_sections is None: return book_text

        st.success("✔ Step 3: Conclusion and References added.")
        return book_text + f"\n\n---\n\n" + final_sections

# --- Main App Interface ---
st.title("📚 Local LM Strategy Book Crafter")
st.caption("Inspired by ancient strategists, powered by your Local LM. A high-context text generation system.")

col1, col2 = st.columns([0.4, 0.6], gap="large")

with col1:
    st.header("Forge Your Doctrine")
    with st.form("writing_form"):
        concept_input = st.text_area(
            "**Enter Your Core Concept or Philosophy:**", 
            height=300, 
            placeholder="Example: A strategy book on using patience and observation to win negotiations. The core idea is that the one who moves second, with the most information, controls the outcome."
        )
        sections_input = st.slider("**Number of Principles (Chapters):**", 2, 15, 10)
        submitted = st.form_submit_button("Generate Strategy Book", type="primary", use_container_width=True)

        if submitted:
            if not concept_input.strip():
                st.warning("A strategist must first have a core concept.")
            else:
                st.session_state.concept = concept_input
                st.session_state.num_sections = sections_input
                st.session_state.start_generation = True
                st.session_state.book_content = ""

if st.session_state.start_generation:
    outline = step_1_planning(st.session_state.concept, st.session_state.num_sections)
    if outline:
        initial_book = step_2_generation_loop(outline, st.session_state.concept)
        if initial_book:
            final_book = step_3_add_conclusion_and_references(initial_book, st.session_state.concept, outline)
            st.session_state.book_content = final_book
    st.session_state.start_generation = False

with col2:
    st.header("The Generated Manuscript")
    if st.session_state.book_content:
        st.markdown(st.session_state.book_content)
        st.download_button(
            label="Download Manuscript (.md)", 
            data=st.session_state.book_content, 
            file_name="strategy_book.md",
            mime="text/markdown",
            use_container_width=True
        )
    else:
        st.info("Your generated book will appear here once the process is complete.")