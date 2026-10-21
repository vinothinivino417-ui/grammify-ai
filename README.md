# Grammify AgentBot

Grammify AgentBot is a Streamlit app that reviews English text and suggests corrections for grammar, spelling, punctuation, word choice, and sentence structure, while aiming to preserve the writer's intended meaning.

## Problem and intended users

Grammify helps people who write or study in English understand possible sentence issues and see a corrected, more natural version. It is intended as a writing and learning aid, not a replacement for human review.

## Features

- Accepts an English sentence in a text area.
- Displays the original sentence, detected issues, a corrected sentence, a natural version, and an explanation of the applicable rule.
- Uses sidebar controls for model temperature (0.0-1.0, default 0.2) and maximum output tokens (300-3000, default 1200).
- Shows an error message and technical details if a check fails.

## How it works

The app passes the submitted sentence to a sequential CrewAI workflow. A planner prepares an analysis plan, a researcher explains relevant language rules, and a corrector drafts the correction. A final reflection task asks the corrector agent to review the result and return the original, mistakes, correction, natural version, and rule explanation.

The agents use a custom OpenAI-compatible client pointed at the Hugging Face router and the `openai/gpt-oss-120b:fastest` model. The response is parsed by the app and shown in the results area.

## Technologies

- Python
- Streamlit for the user interface
- CrewAI for the agent workflow
- OpenAI Python client for chat-completion requests
- Hugging Face router as the model API endpoint
- python-dotenv to load the local API token

## Installation and setup

These commands are for Windows PowerShell, run from the project folder.

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the dependencies declared in `requirements.txt`:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Create a file named `.env` in the project root and add your Hugging Face access token:

   ```text
   HF_TOKEN=your_hugging_face_token
   ```

   The token is required to send model requests. `.env` is listed in `.gitignore`; do not commit it or share its contents.

## Run the app

With the virtual environment active and `.env` configured, run:

```powershell
streamlit run app.py
```

Streamlit will print a local URL in the terminal. Open it in a browser, enter an English sentence, and select **Grammify It!** to see the analysis.

## Example usage

The app's input placeholder uses:

```text
She go to school every day.
```

The app displays the submitted sentence, issues identified by the model, its suggested correction and natural version, and a grammar-rule explanation. Exact results depend on the model response.

## Configuration and limitations

`HF_TOKEN` is read from the root `.env` file. Model temperature and maximum output tokens can be adjusted in the app sidebar; their defaults are 0.2 and 1200 respectively. Submitted text is sent to the Hugging Face router for model inference. Model-generated corrections may be imperfect, so review suggestions before relying on them.

## Project structure

```text
grammify-ai/
├── app.py                 # Streamlit interface and result rendering
├── requirements.txt       # Python dependencies
├── agents/
│   ├── crew.py            # CrewAI tasks and sequential workflow
│   ├── llm.py             # Hugging Face router LLM adapter
│   ├── planner.py         # Planner agent
│   ├── researcher.py      # Researcher agent
│   └── corrector.py       # Correction agent
└── assets/
    └── grammify_baby_mascot.png
```