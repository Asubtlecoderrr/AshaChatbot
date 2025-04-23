from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from ...tools.custom_tool import HerKeyJobAPITool, JobAPITool, ContextReaderTool
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
from crewai import LLM
llm = LLM(model="gemini/gemini-1.5-flash", temperature=0.2)

@CrewBase
class JobCrew():
    """JobCrew crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    herkey_job_tool = HerKeyJobAPITool()
    contextTool = ContextReaderTool()    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    
    
    @agent
    def job_search_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['job_search_agent'],
            verbose=True,
            llm=llm,
            tools = [JobAPITool(),self.contextTool,self.herkey_job_tool]
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    
    @task
    def job_search_task(self) -> Task:
        return Task(
            config=self.tasks_config['job_search_task'],
            output_file='JobCrewReport.md',
        )

    @crew
    def crew(self) -> Crew:
        """Creates the JobCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
