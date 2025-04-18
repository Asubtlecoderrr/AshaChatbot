#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from ashaai.crew import Ashaai

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    # Initial inputs: Start with just the conversational intent (it'll handle the rest)
    inputs = "Hi could you help me find a job"

    try:
        asha = Ashaai()
        crew_instance = asha.crew()

        # Start the crew with inputs for the Conversational Agent
        conversation_output = crew_instance.kickoff(inputs=inputs, agent_name="conversational_agent")
        
        # Check the output of the conversation agent for delegation
        
        intent = conversation_output.output.json_dict["agent_to_call"]
        
        if intent == "job_search":
            print("✅ Conversational agent is ready for job search. Delegating tasks...")
            # Trigger job search task based on the output from conversational agent
            job_search_output = crew_instance.run_task("job_search_task", inputs=conversation_output)
            print(f"Job Search Result: {job_search_output}")

        elif "resume" in intent.lower() :
            print("✅ Conversational agent is ready for resume analysis. Delegating tasks...")
            # Trigger resume analysis task
            resume_analysis_output = crew_instance.run_task("resume_analysis_task", inputs=conversation_output)
            print(f"Resume Analysis Result: {resume_analysis_output}")

        elif "learning" in intent.lower():
            print("✅ Conversational agent is ready for learning recommendations. Delegating tasks...")
            # Trigger learning recommendations task
            learning_advice_output = crew_instance.run_task("recommend_learning_task", inputs=conversation_output)
            print(f"Learning Recommendations: {learning_advice_output}")
        
        else:
            print(conversation_output.output.json_dict["response"])

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         "topic": "AI LLMs"
#     }
#     try:
#         Ashaai().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         Ashaai().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")

# def test():
#     """
#     Test the crew execution and returns the results.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         "current_year": str(datetime.now().year)
#     }
#     try:
#         Ashaai().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while testing the crew: {e}")
