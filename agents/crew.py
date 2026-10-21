from crewai import Crew, Process, Task

from .corrector import create_corrector_agent
from .planner import create_planner_agent
from .researcher import create_researcher_agent


def create_grammar_crew(
    temperature: float = 0.2,
    max_tokens: int = 1200,
):
    """
    Create the Grammify AI multi-agent grammar correction crew.

    Workflow:
        Planner → Researcher → Corrector → Reflection
    """

    planner = create_planner_agent(
        temperature=temperature,
        max_tokens=max_tokens,
    )

    researcher = create_researcher_agent(
        temperature=temperature,
        max_tokens=max_tokens,
    )

    corrector = create_corrector_agent(
        temperature=temperature,
        max_tokens=max_tokens,
    )

    # ---------------------------------------------------------
    # Task 1: Planning
    # ---------------------------------------------------------

    planning_task = Task(
        description="""
Analyze the user's English sentence and create a correction plan.

USER SENTENCE:
{sentence}

Identify what should be checked, including:
- Grammar
- Spelling
- Punctuation
- Verb tense
- Subject-verb agreement
- Word choice
- Sentence structure
- Context and intended meaning

Do NOT correct the sentence yet.

Return a concise but useful analysis plan.
""",
        expected_output="""
A structured analysis plan listing the possible language issues
that need to be investigated.
""",
        agent=planner,
    )

    # ---------------------------------------------------------
    # Task 2: Research
    # ---------------------------------------------------------

    research_task = Task(
        description="""
Using the planner's analysis, investigate the English language
rules relevant to the user's sentence.

USER SENTENCE:
{sentence}

Explain:
1. Which grammar or language rules apply.
2. Why the original sentence may be incorrect.
3. Whether the problem is grammar, spelling, punctuation,
   word choice, context, or sentence structure.
4. What rule should be followed.

Do not simply repeat the planner's answer.
Provide a clear linguistic explanation.

Do NOT produce the final answer yet.
""",
        expected_output="""
A clear explanation of the relevant English grammar,
spelling, punctuation, vocabulary, and context rules.
""",
        agent=researcher,
        context=[planning_task],
    )

    # ---------------------------------------------------------
    # Task 3: Correction
    # ---------------------------------------------------------

    correction_task = Task(
        description="""
Correct the user's English sentence using the planning analysis
and grammar research.

USER SENTENCE:
{sentence}

Create a draft correction containing:

1. Original sentence
2. Mistakes found
3. Explanation of each mistake
4. Corrected sentence
5. A more natural English alternative, if appropriate

Preserve the user's original meaning.

Do not invent information that is not present in the sentence.
""",
        expected_output="""
A complete draft grammar correction with explanations and
a corrected English sentence.
""",
        agent=corrector,
        context=[planning_task, research_task],
    )

    # ---------------------------------------------------------
    # Task 4: Reflection / Self-Review
    # ---------------------------------------------------------

    reflection_task = Task(
        description="""
Review the correction produced by the previous task as a strict
English grammar teacher.

USER SENTENCE:
{sentence}

Check the proposed correction for:

- Grammar accuracy
- Spelling
- Punctuation
- Verb tense
- Subject-verb agreement
- Word choice
- Sentence structure
- Context
- Preservation of the user's intended meaning

If anything is wrong, fix it.

Then produce the FINAL answer in exactly this structure:

ORIGINAL:
<original sentence>

MISTAKES:
- <mistake and explanation>
- <mistake and explanation>

CORRECTED:
<correct English sentence>

NATURAL VERSION:
<more natural version, or the corrected sentence if no change is needed>

RULE:
<short explanation of the grammar rule>

If the original sentence is already correct, clearly say so
and do not invent mistakes.
""",
        expected_output="""
A final, verified English grammar correction with:
original sentence, mistakes, corrected sentence,
natural version, and grammar rule.
""",
        agent=corrector,
        context=[planning_task, research_task, correction_task],
    )

    # ---------------------------------------------------------
    # Create Crew
    # ---------------------------------------------------------

    crew = Crew(
        agents=[
            planner,
            researcher,
            corrector,
        ],
        tasks=[
            planning_task,
            research_task,
            correction_task,
            reflection_task,
        ],
        process=Process.sequential,
        verbose=False,
    )

    return crew