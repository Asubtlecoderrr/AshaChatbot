import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ashaaiflow.src.ashaaiflow.main import CareerGuidanceFlow
import time

sample_queries = [
    # Gratitude
    {"user_query": "Thanks so much, your advice really helped me!", "intent": "gratitude"},
    {"user_query": "I appreciate all the guidance youve been giving me.", "intent": "gratitude"},

    # Job Search
    {"user_query": "Can you help me find marketing jobs in Bangalore?", "intent": "job_search"},
    {"user_query": "I'm looking for frontend developer roles in Pune.", "intent": "job_search"},
    {"user_query": "Are there any remote opportunities in product management?", "intent": "job_search"},
    {"user_query": "Can you show me available jobs for data scientists in Hyderabad?", "intent": "job_search"},

    # Resume Analysis
    {"user_query": "Can you review my resume for business analyst roles?", "intent": "resume_analysis"},
    {"user_query": "Does my resume look okay for a project manager position?", "intent": "resume_analysis"},
    {"user_query": "Is my resume good enough for tech support jobs?", "intent": "resume_analysis"},

    # Recommend Learning
    {"user_query": "Can you suggest some resources to learn cloud computing?", "intent": "recommend_learning"},
    {"user_query": "I want to upskill in digital marketing. Any good YouTube channels?", "intent": "recommend_learning"},
    {"user_query": "Where can I learn full stack development for beginners?", "intent": "recommend_learning"},

    # Motivation Boost
    {"user_query": "Feeling super low today, nothing's working out.", "intent": "motivation_boost"},
    {"user_query": "I got rejected again. Maybe I'm not good enough.", "intent": "motivation_boost"},
    {"user_query": "Is it normal to feel lost after graduation?", "intent": "motivation_boost"},

    # Guidance
    {"user_query": "How do I switch from teaching to IT?", "intent": "guidance"},
    {"user_query": "Ive been a stay-at-home mom for 5 years. How can I restart my career?", "intent": "guidance"},
    {"user_query": "Whats the best way to get into cybersecurity with no experience?", "intent": "guidance"},
    {"user_query": "Should I go for an MBA or continue in tech?", "intent": "guidance"},

    # Communities
    {"user_query": "Are there any women-in-tech communities I can join?", "intent": "communities"},
    {"user_query": "Where can I find mentorship groups for working moms?", "intent": "communities"},
    {"user_query": "Any online support groups for freelancers?", "intent": "communities"},

    # Out of Scope
    {"user_query": "Where can I buy that new Colleen Hoover book?", "intent": "out_of_scope"},
    {"user_query": "Can you help me book a cab to the airport?", "intent": "out_of_scope"},
    {"user_query": "Whats the best place to vacation in April?", "intent": "out_of_scope"},
    {"user_query": "How do I cook lasagna from scratch?", "intent": "out_of_scope"},

    # Stereotype
    {"user_query": "Are women even good at coding?", "intent": "stereotype"},
    {"user_query": "I dont think girls should go into tech, right?", "intent": "stereotype"},
    {"user_query": "Shouldnt women stick to HR roles?", "intent": "stereotype"},

    # Greeting
    {"user_query": "Hey there! Hows it going?", "intent": "greeting"},
    {"user_query": "Hi! Im new here, excited to get started.", "intent": "greeting"},
    {"user_query": "Hello! Can we talk about my career goals?", "intent": "greeting"},

    # Goodbye
    {"user_query": "Thanks, thats all I needed. Bye!", "intent": "goodbye"},
    {"user_query": "Ill come back later to continue this.", "intent": "goodbye"},
    {"user_query": "Logging off for today. Catch you soon!", "intent": "goodbye"},

    # Conversation Continues
    {"user_query": "Okay, so whats next after I update my resume?", "intent": "conversation_continues"},
    {"user_query": "That sounds good, what should I do now?", "intent": "conversation_continues"},
    {"user_query": "Alright, Ive done that. Whats the next step?", "intent": "conversation_continues"},

    # More Job Search
    {"user_query": "Can you find social media jobs in Delhi?", "intent": "job_search"},
    {"user_query": "Any content writing roles in Mumbai?", "intent": "job_search"},

    # More Resume Analysis
    {"user_query": "Does my CV align with UI/UX roles?", "intent": "resume_analysis"},

    # More Learning
    {"user_query": "What are some free courses on Python programming?", "intent": "recommend_learning"},

    # More Guidance
    {"user_query": "How do I transition from sales to product management?", "intent": "guidance"},
    {"user_query": "I have a gap in my resume. How do I explain it?", "intent": "guidance"},
    {"user_query": "What skills should I focus on for data science?", "intent": "guidance"},
]

accuracy_count_intent = 0
accuracy_count_skills = 0   
accuracy_count_location = 0

for user_query in sample_queries:
    user_query_text = user_query["user_query"]
    expected_intent = user_query["intent"]

    content_flow = CareerGuidanceFlow()
    content_flow.state.user_query = user_query_text
    result = content_flow.kickoff()
    intent = content_flow.state.intent
    
    
    if intent == expected_intent:
        accuracy_count_intent += 1
    
    time.sleep(10)

accuracy_intent = accuracy_count_intent / len(sample_queries) * 100
print(f"Accuracy for Intent: {accuracy_intent:.2f}%")


   