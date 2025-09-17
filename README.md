# The PGE-Writer: A Strategic AI Authoring System

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Framework](https://img.shields.io/badge/framework-Streamlit-red.svg)

The PGE-Writer is a sophisticated, multi-step AI authoring system designed to generate coherent, high-quality, long-form non-fiction text. [cite_start]It solves the critical challenges of consistency, accuracy, and logical flow that plague standard single-prompt generation methods[cite: 4].

[cite_start]This system is a practical implementation of the **Perceptual Grid Engine (PGE)**, an original AI architecture designed by Damian Griggs and Jaden Hermann[cite: 2]. By leveraging a structured, iterative process, the PGE-Writer enables even small, local language models to produce manuscripts with a level of quality that rivals massive, cloud-based systems.

## The Core Concept: The Perceptual Grid Engine (PGE)

[cite_start]Traditional AI models often rely on probabilistic, "holistic" pattern matching, which can lead to missed details and logical inconsistencies[cite: 6]. [cite_start]The PGE was inspired by the systematic, deterministic spatial navigation techniques used by blind individuals to build a complete and reliable mental map of an environment[cite: 5, 7].

[cite_start]The PGE-Writer applies this rigorous logic to text generation[cite: 8]:

* [cite_start]**Grid-Based Processing (Chunking):** A long document is first broken down into a logical "grid" of smaller, manageable chunks, such as chapters or core principles[cite: 27].
* [cite_start]**Localized AI Operations:** The AI performs its generation task on each individual chunk, one at a time[cite: 28, 29]. This prevents the model from getting lost or losing context.
* **Cumulative Memory:** This is the key innovation for text coherency. [cite_start]To generate a new chapter, the AI is provided with a constantly updated context that includes concise, automatically generated summaries of the key points from all previous chapters[cite: 30, 34, 35]. [cite_start]This acts as a robust long-term memory, preventing plot holes and repetition[cite: 35].

[cite_start]Ultimately, the PGE replaces unpredictable approximation with a structured, exhaustive process, leading to more reliable and powerful AI systems[cite: 9, 42].

## How It Works: The 3-Step Writing Process

The PGE-Writer code implements the PGE's text-generation architecture in a clear, three-phase methodology:

1.  **Phase 1: Architectural Planning (`step_1_planning`)**
    The system first prompts the AI to analyze the user's core concept and generate a complete, chapter-by-chapter outline. [cite_start]This creates the foundational "grid" for the book, ensuring a logical structure from the start[cite: 27].

2.  **Phase 2: Iterative Generation with Hybrid Memory (`step_2_generation_loop`)**
    The writer iterates through the outline one chapter at a time. For each chapter, it constructs a focused, "hybrid-memory" prompt that gives the AI everything it needs to know—and nothing it doesn't. This prevents context window overflows and keeps the AI on task. [cite_start]After each chapter is written, the system generates a new summary to add to its cumulative memory, perfectly implementing the PGE's core principle[cite: 35].

3.  **Phase 3: Synthesis & Conclusion (`step_3_add_conclusion_and_references`)**
    Once the main body is complete, a final prompt is sent with the full text, instructing the AI to write a powerful concluding chapter and a "Further Reading" section that matches the book's established tone.

## Features

* **High Coherency & Consistency:** The PGE process drastically reduces repetition and logical errors.
* **Persona Adherence:** Maintains a consistent authorial voice and style from start to finish.
* **Local-First:** Designed to work with local LLMs (via LM Studio, Ollama, etc.), ensuring privacy and zero API costs.
* **Efficient:** Achieves high-quality results even on smaller, resource-friendly models (e.g., Llama 3 8B).
* **Interactive UI:** Built with Streamlit for a user-friendly experience.

## Requirements

* Python 3.9+
* A running local LLM server with an OpenAI-compatible endpoint (e.g., [LM Studio](https://lmstudio.ai/), [Ollama](https://ollama.com/)).
* The Python packages listed in `requirements.txt`.

## Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/pge-writer.git](https://github.com/your-username/pge-writer.git)
    cd pge-writer
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: The `requirements.txt` file should contain `streamlit` and `openai`)*

4.  **Set up your Local LLM:**
    * Download and run LM Studio or another compatible server.
    * Load your desired model (e.g., Meta-Llama-3-8B-Instruct.Q4_K_M.gguf).
    * Start the local server at the default address (`http://127.0.0.1:1234`). The code is pre-configured for this endpoint.

## Running the Application

Once your local server is running, execute the following command in your terminal:

```bash
streamlit run app.py
