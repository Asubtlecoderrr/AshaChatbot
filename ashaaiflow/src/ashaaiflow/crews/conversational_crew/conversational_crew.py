from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.memory import LongTermMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai.knowledge.source.crew_docling_source import CrewDoclingSource
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from ...tools.custom_tool import get_context_tool
import os
from crewai import LLM
llm = LLM(model="gemini/gemini-1.5-flash", temperature=0.5)

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ConversationalCrew():
    """ConversationalCrew crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    context_tool = get_context_tool()
    
    # content_source = CrewDoclingSource(
    #     file_paths=[f"../src/ashaaiflow/knowledge/knowledgeBase/*"], 
    # )
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def conversational_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['conversational_agent'],
            verbose=True,
            llm=llm,
            tools=[self.context_tool],
            
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task

    @task
    def conversational_task(self) -> Task:
        return Task(
            config=self.tasks_config['conversational_task'],
            output_file='ConversationalCrewreport.md',
            tools=[self.context_tool],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ConversationalCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        
            # knowledge_sources=[self.content_source],
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
