from crewai.flow.flow import Flow, listen, start, router, or_
from crewai import Agent, Crew, Process, Task
from pydantic import BaseModel
from typing import List, Dict
import os
from .crews.conversational_crew.conversational_crew import ConversationalCrew
from .crews.job_crew.job_crew import JobCrew
from .crews.learning_crew.learning_crew import LearningCrew
from .crews.resume_crew.resume_crew import ResumeCrew
from .crews.community_crew.community_crew import CommunityCrew
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from crewai import LLM
from crewai_tools import FileReadTool
from .tools.custom_tool import skillsLocationResponse, get_context_tool
from shared.user_context import cohort_var

llm = LLM(model="gemini/gemini-1.5-flash", temperature=0.2)

class CareerState(BaseModel):
    cohort: str = ""
    intent: str = ""
    skills: str = ""
    location: str = ""
    response: str = """I am sorry I cannot help you with that. I'm here to support you on your career journey! 
                        You can ask me anything related to career guidance — whether you need help analyzing your resume, 
                        finding jobs that match your skills, getting learning recommendations, or even just some motivation or direction. 
                        I can also guide you through community suggestions, or have open conversations to keep things moving forward."""
    user_id: str = None
    user_name: str = None
    user_query : str = "Can you help me find communities related to Women enterpreneurs?"

class CareerGuidanceFlow(Flow[CareerState]):
    @start()
    def finding_insights(self):
        
        contextTool = get_context_tool()
        
        skills_location_agent = Agent(
            role="Skills and Location Agent",
            goal="Extract skills and location from the user's input or history",
            backstory="You are an expert in understanding user skills and location.",
            verbose=True,
            llm=llm,
            tools=[contextTool],
        )
        
        intent_agent = Agent(
            role="Intent Classifier",
            goal="""Classify the user's intent from the user's input or history""",
            backstory="You are an expert in understanding user intent and can classify it accurately.",
            verbose=True,
            llm=llm,
        )
        
        cohort_agent = Agent(
            role="Cohort Classification Agent",
            goal ="""  Classify the user into one of the following cohorts from the user's input or history:
                        "Starter" (just launching a career), "Restarter" (returning after a gap), 
                        or "Riser" (already employed and seeking a roadmap forward).""",
            backstory="You are the intelligent classifier who understands career stages and can classify the user into one of the three cohorts.",
            verbose=True,
            llm=llm,
        )
        
        skills_location_task = Task(
            description=f"""Extract the user's skills and location from the context provided.
                        The current user_query is: {self.state.user_query}""",
            expected_output="A dictionary containing 'skills' and 'location'.",
            agent=skills_location_agent,
            output_pydantic=skillsLocationResponse
        )
        
        intent_classification_task = Task(
            description=f"""
                This is the user's current message: "{self.state.user_query}".

                You must use the tool **Read a file's content** to read the context of previous conversations from the `context.txt` file.
                This will help you determine if the user's current message is a continuation of a previous conversation or a new query.

                Classify the intent of the current message into one of the following:
                - "resume_analysis"
                - "job_search"
                - "recommend_learning"
                - "motivation"
                - "guidance"
                - "communities"
                - "out_of_scope" (if the query is unrelated to career guidance)
                - "stereotype" (if it relates to gender stereotypes in careers)
                - "conversation_continues" (if the message is a follow-up or clarification to an earlier query)

                Example:
                User: I am looking for a job in data science.  
                Assistant: Can you share your preferred location?  
                User: Bangalore is my preferred location.  
                → Intent is "job_search" and location is "Bangalore".

                Carefully read the context and classify the intent accordingly.
            """,
            expected_output="A single string value: resume_analysis | job_search | recommend_learning | communities | motivation | out_of_scope | stereotype | guidance | conversation_continues",
            agent=intent_agent,
            tools=[contextTool]
        )

        
        cohort_classification_task = Task(
            description=f"""
                Your job is to classify the user into one of the following cohorts based on their background and current message:
                - "Starter": Just launching their career
                - "Restarter": Returning to work after a gap
                - "Riser": Already employed and looking to grow or pivot

                You must first use the tool **Read a file's content** to read the context of previous conversations from the `context.txt` file.
                Then, consider both the historical context and this current message: "{self.state.user_query}"

                Based on this information, return the most appropriate cohort.
            """,
            expected_output="A single string value: Starter | Restarter | Riser",
            agent=cohort_agent,
            tools=[contextTool]
        )

        # Create a crew for intent classification
        classifier_crew = Crew(
            agents=[intent_agent, cohort_agent,skills_location_agent],
            tasks=[intent_classification_task, cohort_classification_task , skills_location_task],
            process=Process.sequential,
            verbose=True,
        )
        
        result = classifier_crew.kickoff()
        valid_cohorts = {"Starter", "Restarter", "Riser"}
        self.state.skills += result["skills"]
        self.state.location = result["location"]
        self.state.intent = intent_classification_task.output.raw
        self.state.cohort = cohort_classification_task.output.raw if cohort_classification_task.output.raw in valid_cohorts else "Starter"
        print(f"Intent: {self.state.intent}, Cohort: {self.state.cohort}")
        cohort_var.set(self.state.cohort)
        return self.state.intent

    @router(finding_insights)
    def route_by_category(self, intent):
        # Route to different handlers based on category
        return intent.lower()

    
    @listen("stereotype")
    def handle_stereotype(self, _):
        from crewai import LLM
        llm = LLM(model="gemini/gemini-1.5-flash",temperature=0.2, max_tokens=2000)

        prompt = f"""
            You are good at handling stereotypes and biases questions. 
            This is a user_query **{self.state.user_query}** related to stereotypes.
            You need to curate a response that discards the stereotype and provides a positive and encouraging response.
            Respond by:
            - Gently correcting the misconception without using terms like 'harmful', 'dangerous', 'toxic', or 'inaccurate'.
            - Focusing on positive encouragement and real examples of women succeeding.
            - Keeping your tone warm, motivational, and free from judgmental or confrontational language.
            - Framing the response as an uplifting perspective shift rather than a rebuttal.

            End goal: Empower the user, reinforce self-belief, and inspire action. Focus on next steps and keep it free of bias or assumptions
        """

        response = llm.call(prompt)
        self.state.response = response
        return "Handled stereotype query."



    @listen(or_("guidance", "motivation","conversation_continues"))
    def provide_guidance(self, _):
        
        inputs = {
            "user_query": self.state.user_query,
            "cohort": self.state.cohort,
            "intent": self.state.intent
        }
        try:
            result = ConversationalCrew().crew().kickoff(inputs=inputs)
            self.state.response = result.raw
            print(result.raw)
            return "Guidance provided."
        
        except Exception as e:
            self.state.response = "An error occurred, optimizing response."
            return "optimize"
    
    @router(provide_guidance)
    def after_conversational(self, result):
        if result == "optimize":
            return result
   
    @listen("resume_analysis")
    def resume_analysis_func(self, _):        
        
        result = ResumeCrew().crew().kickoff()
        self.state.response = result.raw
        print(result.raw)
        return "optimize"
    
    @router(resume_analysis_func)
    def after_resume(self, result):
        return result 

    @listen("job_search")
    def job_search_func(self, _):        
        inputs = {
            "skills": self.state.skills,
            "location": self.state.location,
            "user_query" : self.state.user_query
        }
        result = JobCrew().crew().kickoff(inputs=inputs)
        self.state.response = result.raw
        print(result.raw)
        return "optimize"

    @router(job_search_func)
    def after_job(self, result):
        return result 
    
    @listen("recommend_learning")
    def recommend_learning_func(self, _):
        inputs = {
            "user_query": self.state.user_query,
            "cohort": self.state.cohort
        }
        result = LearningCrew().crew().kickoff(inputs=inputs)
        self.state.response = result.raw
        return "optimize"
    
    @router(recommend_learning_func)
    def after_recommend_learning(self, result):
        return result 
    
    @listen("communities")
    def communities_func(self, _):
        inputs = {
            "user_query": self.state.user_query,
            "cohort": self.state.cohort,
            "skills": self.state.skills,
            "location": self.state.location
        }
        result = CommunityCrew().crew().kickoff(inputs=inputs)
        self.state.response = result.raw
        print(result.raw)
        return "optimize"
    
    @router(communities_func)
    def communities_router_func(self, result):
        return result 
    
    @listen("optimize")
    def optimize_response(self, _):
        from crewai import LLM
        llm = LLM(model="gemini/gemini-1.5-flash",temperature=0.2, max_tokens=4000)

        prompt = f"""
        You are a career assistant helping women with personalized career guidance.

        The user named {self.state.user_name} has expressed interest in **{self.state.intent}**. the current user query was **{self.state.user_query}**.
        The response curated by other agent is **{self.state.response}**. 
        Rephrase the response in more engaging conversation with all information in response and 
        if it contains links of any kind, strictly do not remove them you need to add links to the response.
        
        If by any chance, I repeat only if the response provided by other agents was not able to answer the user's query or some error occured, 
        you should address the user's query directly and ensure the response is encouraging and empathetic

        You can also use user_name to make it more personalized but **remember not to use it too much and make it sound creepy and forced.**
        
        Strictly restrict mentioniong your limitations or apologizing for not being able to help.
        Your response tone should be friendly and encouraging, focus on next steps and keep it free of bias or assumptions. Dont greet all the time.
        """

        response = llm.call(prompt)
        self.state.response = response
        return "Response optimized for engagement and clarity."

def kickoff():
    # Instantiate the flow and run it
    content_flow = CareerGuidanceFlow()
    result = content_flow.kickoff()
    print("Final content:", content_flow.state.response)