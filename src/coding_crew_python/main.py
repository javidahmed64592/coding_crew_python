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
    num_required_inputs = 1
    if len(sys.argv) < num_required_inputs + 1:
        msg = "Please provide the path to the codebase as an argument."
        raise ValueError(msg)

    inputs["codebase_path"] = sys.argv[1]

    try:
        CodingCrewPython().crew().kickoff(inputs=inputs)
    except Exception as e:
        msg = f"An error occurred while running the crew: {e}"
        raise Exception(msg)


def train() -> None:
    """
    Train the crew for a given number of iterations.
    """
    num_required_inputs = 2
    if len(sys.argv) < num_required_inputs + 1:
        msg = "Please provide the number of iterations and the path to the codebase as arguments."
        raise ValueError(msg)

    inputs["codebase_path"] = sys.argv[2]

    try:
        CodingCrewPython().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[3], inputs=inputs)
    except Exception as e:
        msg = f"An error occurred while training the crew: {e}"
        raise Exception(msg)


def replay() -> None:
    """
    Replay the crew execution from a specific task.
    """
    num_required_inputs = 2
    if len(sys.argv) < num_required_inputs + 1:
        msg = "Please provide the task ID and the path to the codebase as arguments."
        raise ValueError(msg)

    inputs["codebase_path"] = sys.argv[2]

    try:
        CodingCrewPython().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        msg = f"An error occurred while replaying the crew: {e}"
        raise Exception(msg)


def test() -> None:
    """
    Test the crew execution and returns the results.
    """
    num_required_inputs = 3
    if len(sys.argv) < num_required_inputs + 1:
        msg = (
            "Please provide the number of iterations, the OpenAI model name, and the path to the codebase as arguments."
        )
        raise ValueError(msg)

    inputs["codebase_path"] = sys.argv[3]

    try:
        CodingCrewPython().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        msg = f"An error occurred while testing the crew: {e}"
        raise Exception(msg)
