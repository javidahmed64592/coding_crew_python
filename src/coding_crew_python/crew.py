from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from src.coding_crew_python.tools import codebase_tools

list_files_tool = codebase_tools.ListFilesTool()
read_file_tool = codebase_tools.ReadFileTool()
write_file_tool = codebase_tools.WriteFileTool()
run_ruff_tool = codebase_tools.RunRuffTool()
run_mypy_tool = codebase_tools.RunMypyTool()
run_pytest_tool = codebase_tools.RunPytestTool()
analyze_coverage_tool = codebase_tools.AnalyzeCoverageTool()


@CrewBase
class CodingCrewPython:
    """CodingCrewPython crew"""

    agents_config: dict[str, str]
    tasks_config: dict[str, str]

    tasks: list[Task]

    @agent
    def manager(self) -> Agent:
        return Agent(
            config=self.agents_config["manager"],
            verbose=True,
            allow_delegation=True,
            tools=[list_files_tool, read_file_tool],
        )

    @agent
    def code_quality_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["code_quality_specialist"],
            verbose=True,
            tools=[read_file_tool, run_ruff_tool],
        )

    @agent
    def code_type_checker(self) -> Agent:
        return Agent(
            config=self.agents_config["code_type_checker"],
            verbose=True,
            tools=[read_file_tool, run_mypy_tool],
        )

    @agent
    def code_tester(self) -> Agent:
        return Agent(
            config=self.agents_config["code_tester"],
            verbose=True,
            tools=[read_file_tool, run_pytest_tool, analyze_coverage_tool],
        )

    @agent
    def code_documenter(self) -> Agent:
        return Agent(
            config=self.agents_config["code_documenter"],
            verbose=True,
            tools=[read_file_tool],
        )

    @task
    def code_quality_task(self) -> Task:
        return Task(
            config=self.tasks_config["code_quality_task"],
            output_file="reports/code_quality_report.md",
        )

    @task
    def type_checking_task(self) -> Task:
        return Task(
            config=self.tasks_config["type_checking_task"],
            output_file="reports/type_checking_report.md",
        )

    @task
    def unit_test_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["unit_test_analysis_task"],
            output_file="reports/unit_test_analysis_report.md",
        )

    @task
    def documentation_sync_task(self) -> Task:
        return Task(
            config=self.tasks_config["documentation_sync_task"],
            output_file="reports/documentation_sync_report.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CodingCrewPython crew"""
        return Crew(
            manager_agent=self.manager(),
            agents=[
                self.code_quality_specialist(),
                self.code_type_checker(),
                self.code_tester(),
                self.code_documenter(),
            ],
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
