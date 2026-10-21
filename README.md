
# Grammify AgentBot

Grammify AgentBot is a Streamlit writing assistant that reviews English sentences and suggests improvements to grammar, spelling, punctuation, word choice, and sentence structure. It aims to preserve the writer’s intended meaning while explaining the language rules behind its suggestions.

## Who it’s for

Grammify is intended for people who write or study in English and want to understand possible sentence issues. It is a writing and learning aid, not a replacement for human review.

## Features

- Accepts an English sentence through a text input area.
- Identifies possible writing issues.
- Shows the original sentence, a corrected version, and a more natural version.
- Explains the language rule behind the suggested correction.
- Lets users adjust model temperature and maximum output tokens in the sidebar.
- Displays an error message and technical details if a check fails.

## How it works

Grammify sends the submitted sentence through a sequential CrewAI workflow:

1. **Planner** prepares an analysis plan.
2. **Researcher** explains relevant language rules.
3. **Corrector** drafts a suggested correction.
4. **Reflection** asks the corrector to review the result and return the original sentence, identified mistakes, correction, natural version, and rule explanation.

The workflow uses an OpenAI-compatible client connected to the Hugging Face router and the `openai/gpt-oss-120b:fastest` model. The app parses the response and displays the results.

## Technology

- Python
- Streamlit
- CrewAI
- OpenAI Python client
- Hugging Face router
- `python-dotenv`

## Requirements

- Python installed on your computer
- A Hugging Face access token for model requests

## Setup

The following instructions are for Windows PowerShell. Run them from the project folder.

### 1. Create a virtual environment

```powershell
python -m venv .venv
```

### 2. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure your Hugging Face token

Create a file named `.env` in the project root and add your token:

```text
HF_TOKEN=your_hugging_face_token
```

The `.env` file is listed in `.gitignore`. Keep your token private and never commit or share the file.

## Run the app

With the virtual environment active and `.env` configured, run:

```powershell
streamlit run app.py
```

Streamlit will print a local URL in the terminal. Open that URL in your browser to use Grammify.

## Example

Enter a sentence such as:

```text
She go to school every day.
```

Select **Grammify It!** to see the model’s analysis, suggested correction, natural version, and explanation. Results may vary depending on the model response.

## Configuration

The app reads `HF_TOKEN` from the root `.env` file. The sidebar provides these model settings:

| Setting | Default | Available range |
| --- | ---: | ---: |
| Temperature | 0.2 | 0.0–1.0 |
| Maximum output tokens | 1200 | 300–3000 |

## Limitations

Grammify uses model-generated suggestions, which may be imperfect or miss context. Review the results before relying on them. Submitted text is sent to the Hugging Face router for model inference.

## Project structure

```text
grammify-ai/
├── app.py
├── requirements.txt
├── agents/
│   ├── crew.py
│   ├── llm.py
│   ├── planner.py
│   ├── researcher.py
│   └── corrector.py
└── assets/
    └── grammify_baby_mascot.png
```
````
