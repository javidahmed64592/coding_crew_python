#!/usr/bin/env python
import sys
import warnings
from pathlib import Path

from coding_crew_python.crew import CodingCrewPython
from src.coding_crew_python.config.config import inputs

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

if not (codebase := Path(inputs["codebase_path"])):
    msg = "Please provide the path to the codebase as an argument."
    raise ValueError(msg)

if not codebase.is_dir():
    msg = "The codebase path provided is not a directory."
    raise ValueError(msg)


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
    num_required_inputs = 2
    if len(sys.argv) < num_required_inputs + 1:
        msg = "Please provide the number of iterations and the output file as arguments."
        raise ValueError(msg)

    try:
        CodingCrewPython().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        msg = f"An error occurred while training the crew: {e}"
        raise Exception(msg)


def replay() -> None:
    """
    Replay the crew execution from a specific task.
    """
    num_required_inputs = 1
    if len(sys.argv) < num_required_inputs + 1:
        msg = "Please provide the task ID as an argument."
        raise ValueError(msg)

    try:
        CodingCrewPython().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        msg = f"An error occurred while replaying the crew: {e}"
        raise Exception(msg)


def test() -> None:
    """
    Test the crew execution and returns the results.
    """
    num_required_inputs = 2
    if len(sys.argv) < num_required_inputs + 1:
        msg = "Please provide the number of iterations and the OpenAI model name as arguments."
        raise ValueError(msg)

    try:
        CodingCrewPython().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        msg = f"An error occurred while testing the crew: {e}"
        raise Exception(msg)
