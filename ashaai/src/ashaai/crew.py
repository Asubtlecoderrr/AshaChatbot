from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import BaseTool
from crewai_tools import (
    FileReadTool,
    FileSearchTool
)
from tools.custom_tool import HerKeyJobAPITool,HerKeyLearningAPITool,conversationOutput
from crewai.knowledge import Knowledge
from crewai.memory import LongTermMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage

knowledge_base = Knowledge(
    path='knowledge_base/',
    chunk_size=500,
    chunk_overlap=50,
    recursive=True
)


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Ashaai():
    """Ashaai crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    user_id = 'r'
    
    #Tools
    resume_reader_tool = FileReadTool(file_path=f'resume/{user_id}.pdf')
    herkey_learning_tool = HerKeyLearningAPITool()
    
    #db path
    db_path = f"ashaaiDB//memory_{user_id}.db"
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def conversational_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['conversational_agent'],
            verbose=True,
            allow_delegation=True,
            knowledge=knowledge_base
        )

    @agent
    def resume_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['resume_analyst'],
            tools=[self.resume_reader_tool],
            verbose=True,
        )
    
    @agent
    def job_search_agent(self) -> Agent:
        op = self.conversational_task.output.json_dict
        return Agent(
            config=self.agents_config['job_search_agent'],
            tools=[HerKeyJobAPITool(skills=op.get("skills"), location=op.get("location"))],
            verbose=True
        )
        
    @agent
    def learning_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['learning_advisor'],
            tools=[self.herkey_learning_tool],
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    
    @task
    def cohort_classification_task(self) -> Task:
        return Task(
            config=self.tasks_config['cohort_classification_task'],
        )

    @task
    def intent_classification_task(self) -> Task:
        return Task(
            config=self.tasks_config['intent_classification_task'],
        )
    
    @task
    def resume_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['resume_analysis_task'],
            context=[self.cohort_classification_task]
        )
        
    @task 
    def job_search_task(self) -> Task:        
        return Task(
            config=self.tasks_config['job_search_task'],
            tools=[HerKeyJobAPITool()],
            context=[self.conversational_task],
        )
        
    @task
    def recommend_learning_task(self) -> Task:
        return Task(
            config=self.tasks_config['recommend_learning_task'],
        )
    
    @task
    def conversational_task(self) -> Task:
        return Task(
            config=self.tasks_config['conversational_task'],
            output_json=conversationOutput
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Ashaai crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True,
            long_term_memory=LongTermMemory(
                storage=LTMSQLiteStorage(db_path=db_path)
            )
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
