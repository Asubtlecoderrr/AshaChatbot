from crewai.flow.flow import Flow, listen, start, router, or_
from crewai import Agent, Crew, Process, Task
from pydantic import BaseModel
from .crews.conversational_crew.conversational_crew import ConversationalCrew
from .crews.job_crew.job_crew import JobCrew
from .crews.learning_crew.learning_crew import LearningCrew
from .crews.resume_crew.resume_crew import ResumeCrew
from .crews.community_crew.community_crew import CommunityCrew
from crewai import LLM
from .tools.custom_tool import skillsLocationResponse, ContextReaderTool
from shared.user_context import user_id_var
from concurrent.futures import ThreadPoolExecutor
import json
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
    user_id: int = None
    user_name: str = None
    user_query : str = "Can you help me find communities related to Women enterpreneurs?"

class CareerGuidanceFlow(Flow[CareerState]):
    @start()
    def finding_insights(self):
        user_id_var.set(self.state.user_id)
        print(user_id_var.get(),"####################################################")
        contextTool = ContextReaderTool()
        context_content = contextTool._run()
        
        skills_location_agent = Agent(
            role="Skills and Location Agent",
            goal="Extract skills/keywords and location from the user's input or history",
            backstory="You are an expert in understanding user skills and location.",
            verbose=True,
            llm=llm,
        )

        intent_agent = Agent(
            role="Intent Classifier",
            goal="Classify the user's intent from the user's input or history",
            backstory="You are an expert in understanding user intent and can classify it accurately.",
            verbose=True,
            llm=llm,
        )

        cohort_agent = Agent(
            role="Cohort Classification Agent",
            goal="""Classify the user into one of these cohorts: 
                    'Starter' (new to career), 'Restarter' (after a gap), 
                    or 'Riser' (working and growing).""",
            backstory="You understand life stages and career journeys and can classify with context.",
            verbose=True,
            llm=llm,
        )

        
        skills_location_task = Task(
            name="skills_location_task",
            description=f"""
                Extract the user's skills or any keywords related to career and their location.
                Use this context from past conversations:\n\n{context_content}

                The current user message is: "{self.state.user_query}"
            """,
            expected_output="A dictionary containing 'skills' (can include keywords) and 'location'.",
            agent=skills_location_agent,
            output_pydantic=skillsLocationResponse
        )

        intent_classification_task = Task(
            name="intent_classification_task",
            description=f"""
                Use the following past conversation context to understand the user's intent:\n\n{context_content}

                This is the user's current message: "{self.state.user_query}"

                Also consider what the last assistant message was asking, and assume the user wants to continue that flow if they replied vaguely.
                If query is not related to career guidance, classify it as 'out_of_scope'.

                Choose from these intents:
                - gratitude
                - job_search
                - resume_analysis
                - recommend_learning
                - motivation_boost
                - guidance
                - communities
                - out_of_scope
                - stereotype
                - greeting
                - goodbye
                - conversation_continues
            """,
            expected_output="A single string intent value from the list.",
            agent=intent_agent
        )

        cohort_classification_task = Task(
            name="cohort_classification_task",
            description=f"""
                Based on this context:\n\n{context_content}

                And the user's message: "{self.state.user_query}"

                Classify them as:
                - 'Starter': Just starting out
                - 'Restarter': Returning after a career break
                - 'Riser': Currently working and looking to grow or pivot
            """,
            expected_output="A single string value: Starter | Restarter | Riser",
            agent=cohort_agent
        )

        agent_task_pairs = [
            (intent_agent, intent_classification_task),
            (cohort_agent, cohort_classification_task),
            (skills_location_agent, skills_location_task),
        ]

        def run_agent_task(pair):
            agent, task = pair
            result = agent.execute_task(task)
            return {task.name : result}

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(run_agent_task, pair) for pair in agent_task_pairs]
    
            completed_tasks = []
            
            for future in futures:
                try:
                    task_result = future.result() 
                    completed_tasks.append(task_result)
                except Exception as e:
                    print(f"Error executing task: {e}")
                    
        valid_cohorts = {"Starter", "Restarter", "Riser"}
        for task_result in completed_tasks:
            for task_name, output in task_result.items():
                if task_name == "skills_location_task":
                    try:
                        data = json.loads(output)
                        self.state.skills += data.get("skills", "")
                        self.state.location = data.get("location")
                        print(f"Skills: {self.state.skills}, Location: {self.state.location}")
                    except Exception as e:
                        print(f"Error parsing skills_location_task output: {e}")
                elif task_name == "intent_classification_task":
                    print(f"Intent: {output}")
                    self.state.intent = output
                elif task_name == "cohort_classification_task":
                    print(f"Cohort: {output}")
                    self.state.cohort = output if output in valid_cohorts else "Starter"
        
        # Create a crew for intent classification
        # classifier_crew = Crew(
        #     agents=[intent_agent, cohort_agent,skills_location_agent],
        #     tasks=[intent_classification_task, cohort_classification_task , skills_location_task],
        #     process=Process.sequential,
        #     verbose=True,
        # )
        
        # result = classifier_crew.kickoff()
        # valid_cohorts = {"Starter", "Restarter", "Riser"}
        # self.state.skills += skills_location_task.output.raw["skills"]
        # self.state.location =skills_location_task.output.raw["location"]
        # self.state.intent = intent_classification_task.output.raw
        # self.state.cohort = cohort_classification_task.output.raw if cohort_classification_task.output.raw in valid_cohorts else "Starter"
        # print(f"Intent: {self.state.intent}, Cohort: {self.state.cohort}")
        
        # print(f"User ID: {user_id_var.get()}")
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



    @listen(or_("guidance", "motivation_boost","conversation_continues","greeting","goodbye","gratitude"))
    def provide_guidance(self, _):
        
        inputs = {
            "user_query": self.state.user_query,
            "cohort": self.state.cohort,
            "intent": self.state.intent,
            "user_name": self.state.user_name,
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
            "user_query" : self.state.user_query,
            "cohort": self.state.cohort,
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
        llm_2 = LLM(model="gemini/gemini-1.5-flash",temperature=0.2, max_tokens=4000)
        rephraser_agent = Agent(
            role="Conversational Rephraser",
            goal="Transform structured or robotic responses into friendly, encouraging guidance for women navigating their careers.",
            backstory=(
                "You're a compassionate and insightful career assistant who understands the importance of tone, clarity, and empathy. "
                "You support women at various career stages by making every piece of information feel helpful and personalized."
            ),
            allow_delegation=False,
            verbose=True,
            llm=llm_2,
        )
        rephrase_response_task = Task(
            description= f"""
            You are a career assistant helping women with personalized career guidance.

            The user named {self.state.user_name} has expressed interest in **{self.state.intent}**. 
            The current user query was **{self.state.user_query}**.
            The response curated by another agent is **{self.state.response}**.
            Retrieve the ongoing conversation context using the `ContextTool` and incorporate relevant past messages to ensure 
            this response feels like a natural continuation of the conversation.

            Rephrase the response in a more engaging conversation while keeping all the information intact. If the response includes links, strictly do not remove them—ensure they are retained and clearly shown.

            Strictly only If the agents made some mistake previously or the **{self.state.user_query}** sentiment sounds disappointing, 
            then only you should **apologize sincerely in a friendly, human way**, explain what went wrong, and immediately adjust its response to better match the users needs.
            
            If the response from the other agent didnt answer the query or had an error, address the users query directly in an encouraging and empathetic way.

            You may use the users name (“{self.state.user_name}”) a little, but dont overuse it.
            
            Do not talk about your limitations or apologize for not being able to help.
            Maintain a tone that is friendly, motivational, and bias-free. Avoid greetings.
            """,
            expected_output=(
                "A warm, human, motivating rephrasing of the original response that flows as a conversation. "
                "It should feel natural and clear, while retaining all links and original useful content."
            ),
            agent=rephraser_agent,
            tools=[ContextReaderTool()],
        )
        response = rephraser_agent.execute_task(rephrase_response_task)
        self.state.response = response
        return "Response optimized for engagement and clarity."

def kickoff():
    # Instantiate the flow and run it
    content_flow = CareerGuidanceFlow()
    result = content_flow.kickoff()
    print("Final content:", content_flow.state.response)
