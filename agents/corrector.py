from crewai import Agent

from .llm import get_llm


def create_corrector_agent(
    temperature: float = 0.2,
    max_tokens: int = 1200,
):
    llm = get_llm(
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return Agent(
        role="Senior English Grammar Correction Teacher",
        goal=(
            "Correct English grammar, spelling, punctuation, word choice, "
            "sentence structure, and context errors accurately. "
            "Produce clear and natural English while preserving the user's "
            "intended meaning."
        ),
        backstory=(
            "You are an English teacher with 20 years of classroom experience. "
            "You are excellent at correcting English sentences and explaining "
            "mistakes in a simple way. You never change the intended meaning "
            "unless the original sentence is clearly ambiguous."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )