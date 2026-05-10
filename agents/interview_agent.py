import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage, AIMessage

load_dotenv()


def get_llm():
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-70b-8192",
        temperature=0.7,
        max_tokens=1000
    )


# ─────────────────────────────────────────
# INTERVIEWER AGENT
# ─────────────────────────────────────────

def build_interviewer_system_prompt(session_config, user_profile):
    return f"""
You are an expert technical interviewer conducting a 
{session_config['interview_type']} interview for a 
{session_config['target_company']} company.

Candidate Profile:
- Experience Level: {user_profile.get('experience_level', 'fresher')}
- Target Role: {user_profile.get('target_role', 'SDE')}
- Skills: {', '.join(user_profile.get('skills', []))}
- Resume Projects: {user_profile.get('resume_text', 'Not provided')[:500]}

Interview Config:
- Type: {session_config['interview_type']}
- Difficulty: {session_config['difficulty']}
- Company Style: {session_config['target_company']}
- Total Questions: {session_config['total_questions']}

Your behavior rules:
1. Ask ONE question at a time — never multiple
2. Be professional but friendly
3. If answer is weak (score < 4) → ask simpler follow up
4. If answer is strong (score > 7) → go deeper or harder
5. If answer is average (4-7) → move to next related topic
6. Always base questions on candidate skills when possible
7. For {session_config['target_company']} style interviews:
   - google/microsoft → deep DSA + system design
   - flipkart/zomato/razorpay → practical + problem solving
   - tcs/infosys/wipro → basic CS + aptitude style
   - startup → practical coding + culture fit
8. Start with a warm introduction in first message
9. Keep responses concise and clear
10. After {session_config['total_questions']} questions say:
    "That concludes our interview. Thank you for your time!"

Current question number: {session_config.get('questions_asked', 0) + 1}
of {session_config['total_questions']}
"""


def get_interviewer_response(
    session_config,
    user_profile,
    conversation_history,
    last_score=None
):
    llm = get_llm()

    system_prompt = build_interviewer_system_prompt(
        session_config,
        user_profile
    )

    # Add score context if available
    if last_score is not None:
        if last_score < 4:
            system_prompt += "\n\nPrevious answer was weak. Ask a simpler follow-up or hint."
        elif last_score > 7:
            system_prompt += "\n\nPrevious answer was strong. Go deeper or increase difficulty."
        else:
            system_prompt += "\n\nPrevious answer was average. Move to next topic."

    messages = [SystemMessage(content=system_prompt)]

    # Add conversation history
    for msg in conversation_history:
        if msg['role'] == 'candidate':
            messages.append(HumanMessage(content=msg['content']))
        elif msg['role'] == 'interviewer':
            messages.append(AIMessage(content=msg['content']))

    response = llm.invoke(messages)
    return response.content


# ─────────────────────────────────────────
# EVALUATOR AGENT
# ─────────────────────────────────────────

def build_evaluator_system_prompt():
    return """
You are an expert technical interview evaluator.
Your job is to evaluate candidate answers objectively.

You must respond in this EXACT format and nothing else:

SCORE: <number between 1-10>
FEEDBACK: <2-3 sentences of specific feedback>
STRONG_POINTS: <what candidate did well>
WEAK_POINTS: <what candidate missed or got wrong>

Scoring Guide:
1-3   → Very weak, major concepts missing
4-5   → Basic understanding, significant gaps
6-7   → Good understanding, minor gaps
8-9   → Strong answer, well explained
10    → Perfect, nothing to add

Be strict but fair. Base score only on technical accuracy
and communication clarity.
"""


def evaluate_answer(question, answer, interview_type, difficulty):
    llm = get_llm()

    system_prompt = build_evaluator_system_prompt()

    user_message = f"""
Interview Type: {interview_type}
Difficulty: {difficulty}
Question: {question}
Candidate Answer: {answer}

Evaluate this answer now.
"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]

    response = llm.invoke(messages)
    return parse_evaluation(response.content)


def parse_evaluation(evaluation_text):
    result = {
        'score': 5.0,
        'feedback': '',
        'strong_points': '',
        'weak_points': ''
    }

    lines = evaluation_text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if line.startswith('SCORE:'):
            try:
                score_str = line.replace('SCORE:', '').strip()
                result['score'] = float(score_str)
            except ValueError:
                result['score'] = 5.0

        elif line.startswith('FEEDBACK:'):
            result['feedback'] = line.replace(
                'FEEDBACK:', ''
            ).strip()

        elif line.startswith('STRONG_POINTS:'):
            result['strong_points'] = line.replace(
                'STRONG_POINTS:', ''
            ).strip()

        elif line.startswith('WEAK_POINTS:'):
            result['weak_points'] = line.replace(
                'WEAK_POINTS:', ''
            ).strip()

    return result