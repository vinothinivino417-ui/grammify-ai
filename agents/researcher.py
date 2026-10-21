from crewai import Agent

from .llm import get_llm


def create_researcher_agent(
    temperature: float = 0.2,
    max_tokens: int = 1200,
):
    llm = get_llm(
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return Agent(
        role="English Grammar Research Specialist",
        goal=(
            "Analyze the grammar issues identified by the planner. "
            "Research and explain the relevant English grammar rules, "
            "spelling rules, word usage, sentence structure, and context."
        ),
        backstory=(
            "You are a highly experienced English grammar researcher and "
            "teacher. You specialize in understanding why an English sentence "
            "is incorrect and determining the exact rule needed to correct it. "
            "You explain rules clearly and avoid making unsupported corrections."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )