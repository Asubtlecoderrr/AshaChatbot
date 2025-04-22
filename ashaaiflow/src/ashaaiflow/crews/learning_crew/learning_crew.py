from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from ...tools.custom_tool import HerKeyLearningAPITool,YTLearningTool, get_context_tool
from crewai import LLM
llm = LLM(model="gemini/gemini-1.5-flash", temperature=0.2)
from shared.user_context import cohort_var

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class LearningCrew():
    """LearningCrew crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    yt_learning_tool = YTLearningTool()
    context_tool = get_context_tool()

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def learning_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['learning_advisor'],
            verbose=True,
            tools=[HerKeyLearningAPITool(),self.yt_learning_tool,self.context_tool],
            llm=llm,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def recommend_learning_task(self) -> Task:
        return Task(
            config=self.tasks_config['recommend_learning_task'],
            output_file="LearningCrewreport.md"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LearningCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
