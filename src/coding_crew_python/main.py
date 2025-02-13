#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from coding_crew_python.crew import CodingCrewPython

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

inputs = {"current_year": str(datetime.now().year)}


def run() -> None:
    """
    Run the crew.
    """

    try:
        CodingCrewPython().crew().kickoff(inputs=inputs)
    except Exception as e:
        msg = f"An error occurred while running the crew: {e}"
        raise Exception(msg)


def train() -> None:
    """
    Train the crew for a given number of iterations.
    """
    try:
        CodingCrewPython().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        msg = f"An error occurred while training the crew: {e}"
        raise Exception(msg)


def replay() -> None:
    """
    Replay the crew execution from a specific task.
    """
    try:
        CodingCrewPython().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        msg = f"An error occurred while replaying the crew: {e}"
        raise Exception(msg)


def test() -> None:
    """
    Test the crew execution and returns the results.
    """
    try:
        CodingCrewPython().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        msg = f"An error occurred while testing the crew: {e}"
        raise Exception(msg)
