from crewai import Agent

from .llm import get_llm


def create_planner_agent(temperature: float = 0.2, max_tokens: int = 1200):
    llm = get_llm(
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return Agent(
        role="English Grammar Analysis Planner",
        goal=(
            "Create a clear analysis plan for identifying grammar, spelling, "
            "word choice, sentence structure, and context problems in English."
        ),
        backstory=(
            "You are an experienced English grammar teacher with 20 years "
            "of teaching experience. Before correcting a sentence, you carefully "
            "plan what needs to be examined."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )