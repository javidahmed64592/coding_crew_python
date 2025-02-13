import subprocess
from pathlib import Path

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class CodebasePathInput(BaseModel):
    """Input schema for tools that require a codebase path."""

    codebase_path: str = Field(..., description="Path to the codebase directory.")
    command: str = Field("check", description="Command to run with Ruff tool. Options are 'check' or 'format'.")
    fix: bool = Field(False, description="Whether to fix issues when running the 'check' command with Ruff tool.")


class ListFilesTool(BaseTool):
    name: str = "List Files"
    description: str = "List all files in the codebase directory."
    args_schema: type[BaseModel] = CodebasePathInput

    def _run(self, codebase_path: str) -> list[str]:
        path = Path(codebase_path)
        return [str(file) for file in path.rglob("*") if file.is_file()]


class ReadFileTool(BaseTool):
    name: str = "Read File"
    description: str = "Read the contents of a file in the codebase."
    args_schema: type[BaseModel] = CodebasePathInput

    def _run(self, codebase_path: str, file_path: str) -> str:
        path = Path(codebase_path) / file_path
        return path.read_text()


class WriteFileTool(BaseTool):
    name: str = "Write File"
    description: str = "Write contents to a file in the codebase."
    args_schema: type[BaseModel] = CodebasePathInput

    def _run(self, codebase_path: str, file_path: str, content: str) -> str:
        path = Path(codebase_path) / file_path
        path.write_text(content)
        return f"File {file_path} written successfully."


class RunRuffTool(BaseTool):
    name: str = "Run Ruff"
    description: str = "Run the Ruff tool to check for code quality issues or format code."
    args_schema: type[BaseModel] = CodebasePathInput

    def _run(self, codebase_path: str, command: str = "check", fix: bool = False) -> str:
        if command not in ["check", "format"]:
            msg = "Invalid command for Ruff tool. Use 'check' or 'format'."
            raise ValueError(msg)

        cmd = ["ruff", command, codebase_path]
        if command == "check" and fix:
            cmd.append("--fix")

        result = subprocess.run(cmd, capture_output=True, text=True, check=False)  # noqa
        return result.stdout


class RunMypyTool(BaseTool):
    name: str = "Run MyPy"
    description: str = "Run the MyPy tool to check for type hint issues."
    args_schema: type[BaseModel] = CodebasePathInput

    def _run(self, codebase_path: str) -> str:
        result = subprocess.run(["mypy", codebase_path], capture_output=True, text=True, check=False)  # noqa
        return result.stdout


class RunPytestTool(BaseTool):
    name: str = "Run Pytest"
    description: str = "Run unit tests using pytest."
    args_schema: type[BaseModel] = CodebasePathInput

    def _run(self, codebase_path: str) -> str:
        result = subprocess.run(["pytest", codebase_path], capture_output=True, text=True, check=False)  # noqa
        return result.stdout


class AnalyzeCoverageTool(BaseTool):
    name: str = "Analyze Coverage"
    description: str = "Analyze code coverage using pytest-cov."
    args_schema: type[BaseModel] = CodebasePathInput

    def _run(self, codebase_path: str) -> str:
        result = subprocess.run(["pytest", "--cov", codebase_path], capture_output=True, text=True, check=False)  # noqa
        return result.stdout
