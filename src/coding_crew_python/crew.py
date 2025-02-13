from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class CodingCrewPython:
    """CodingCrewPython crew"""

    agents_config: dict[str, str]
    tasks_config: dict[str, str]

    tasks: list[Task]

    @agent
    def manager(self) -> Agent:
        return Agent(config=self.agents_config["manager"], verbose=True, allow_delegation=True)

    @agent
    def code_quality_specialist(self) -> Agent:
        return Agent(config=self.agents_config["code_quality_specialist"], verbose=True)

    @agent
    def code_type_checker(self) -> Agent:
        return Agent(config=self.agents_config["code_type_checker"], verbose=True)

    @agent
    def code_tester(self) -> Agent:
        return Agent(config=self.agents_config["code_tester"], verbose=True)

    @agent
    def code_documenter(self) -> Agent:
        return Agent(config=self.agents_config["code_documenter"], verbose=True)

    @agent
    def researcher(self) -> Agent:
        return Agent(config=self.agents_config["researcher"], verbose=True)

    @task
    def code_quality_task(self) -> Task:
        return Task(config=self.tasks_config["code_quality_task"], output_file="code_quality_report.md")

    @task
    def type_checking_task(self) -> Task:
        return Task(config=self.tasks_config["type_checking_task"], output_file="type_checking_report.md")

    @task
    def unit_test_analysis_task(self) -> Task:
        return Task(config=self.tasks_config["unit_test_analysis_task"], output_file="unit_test_analysis_report.md")

    @task
    def unit_test_writing_task(self) -> Task:
        return Task(config=self.tasks_config["unit_test_writing_task"], output_file="unit_tests.py")

    @task
    def documentation_sync_task(self) -> Task:
        return Task(config=self.tasks_config["documentation_sync_task"], output_file="documentation_sync_report.md")

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
                self.researcher(),
            ],
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
