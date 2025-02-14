import subprocess
from pathlib import Path

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from src.coding_crew_python.config.config import inputs

codebase_path = Path(inputs["codebase_path"])


class CodebaseFileInput(BaseModel):
    """Input schema for tools that require a codebase path and a file path."""

    file_path: str = Field(..., description="Path to the file in the codebase.")


class RuffToolInput(BaseModel):
    """Input schema for the Ruff tool."""

    command: str = Field("check", description="Command to run with Ruff tool. Options are 'check' or 'format'.")
    fix: bool = Field(False, description="Whether to fix issues when running the 'check' command with Ruff tool.")


class ListFilesTool(BaseTool):
    name: str = "List Files"
    description: str = "List all files in the codebase directory."

    def _run(self) -> list[str]:
        return [str(file) for file in codebase_path.rglob("*") if file.is_file()]


class ReadFileTool(BaseTool):
    name: str = "Read File"
    description: str = "Read the contents of a file in the codebase."
    args_schema: type[BaseModel] = CodebaseFileInput

    def _run(self, file_path: str) -> str:
        path = codebase_path / file_path
        return path.read_text()


class WriteFileTool(BaseTool):
    name: str = "Write File"
    description: str = "Write contents to a file in the codebase."
    args_schema: type[BaseModel] = CodebaseFileInput

    def _run(self, file_path: str, content: str) -> str:
        path = codebase_path / file_path
        path.write_text(content)
        return f"File {file_path} written successfully."


class RunRuffTool(BaseTool):
    name: str = "Run Ruff"
    description: str = "Run the Ruff tool to check for code quality issues or format code."

    def _run(self, command: str = "check", fix: bool = False) -> str:
        if command not in ["check", "format"]:
            msg = "Invalid command for Ruff tool. Use 'check' or 'format'."
            raise ValueError(msg)

        cmd = ["ruff", command, str(codebase_path)]
        if command == "check" and fix:
            cmd.append("--fix")

        result = subprocess.run(cmd, capture_output=True, text=True, check=False)  # noqa
        return result.stdout


class RunMypyTool(BaseTool):
    name: str = "Run MyPy"
    description: str = "Run the MyPy tool to check for type hint issues."

    def _run(self) -> str:
        result = subprocess.run(["mypy", str(codebase_path)], capture_output=True, text=True, check=False)  # noqa
        return result.stdout


class RunPytestTool(BaseTool):
    name: str = "Run Pytest"
    description: str = "Run unit tests using pytest."

    def _run(self) -> str:
        result = subprocess.run(["pytest", str(codebase_path)], capture_output=True, text=True, check=False)  # noqa
        return result.stdout


class AnalyzeCoverageTool(BaseTool):
    name: str = "Analyze Coverage"
    description: str = "Analyze code coverage using pytest-cov."

    def _run(self) -> str:
        result = subprocess.run(["pytest", "--cov", str(codebase_path)], capture_output=True, text=True, check=False)  # noqa
        return result.stdout
