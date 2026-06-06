import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()


def get_llm():
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile",
        temperature=0.1,
        max_tokens=2000
    )


def generate_report(session):
    """
    Generate complete evaluation report for a session.
    Analyzes all Q&A pairs and produces structured feedback.
    """

    # Get all messages from session
    messages = session.messages.all().order_by('timestamp')

    # Build Q&A pairs
    qa_pairs = []
    current_question = None

    for msg in messages:
        if msg.role == 'interviewer':
            current_question = msg.content
        elif msg.role == 'candidate' and current_question:
            qa_pairs.append({
                'question': current_question,
                'answer': msg.content,
                'score': msg.score or 0,
                'feedback': msg.feedback or ''
            })
            current_question = None

    if not qa_pairs:
        return None

    # Calculate scores
    scores = [qa['score'] for qa in qa_pairs if qa['score']]
    average_score = sum(scores) / len(scores) if scores else 0

    # Build prompt for report agent
    qa_text = ""
    for i, qa in enumerate(qa_pairs, 1):
        qa_text += f"""
Question {i}: {qa['question']}
Answer: {qa['answer']}
Score: {qa['score']}/10
Feedback: {qa['feedback']}
---"""

    system_prompt = """
You are an expert interview coach generating a detailed report.
Respond in this EXACT format:

OVERALL_FEEDBACK: <2-3 sentences overall assessment>
STRONG_TOPICS: topic1, topic2, topic3
WEAK_TOPICS: topic1, topic2, topic3
TECHNICAL_SCORE: <number 1-10>
COMMUNICATION_SCORE: <number 1-10>
TIP_1: <specific improvement tip>
TIP_2: <specific improvement tip>
TIP_3: <specific improvement tip>

Be specific and constructive. Base everything on actual answers given.
"""

    user_message = f"""
Interview Type: {session.interview_type}
Difficulty: {session.difficulty}
Company: {session.target_company}
Average Score: {average_score:.1f}/10

Questions and Answers:
{qa_text}

Generate the report now.
"""

    llm = get_llm()
    messages_list = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]

    response = llm.invoke(messages_list)
    parsed = parse_report(response.content)

    # Add calculated data
    parsed['average_score'] = round(average_score, 1)
    parsed['overall_score'] = round(
        (parsed['technical_score'] + parsed['communication_score']) / 2, 1
    )
    parsed['question_breakdown'] = qa_pairs
    parsed['total_questions_asked'] = len(qa_pairs)

    return parsed


def parse_report(report_text):
    result = {
        'overall_feedback': '',
        'strong_topics': [],
        'weak_topics': [],
        'technical_score': 5.0,
        'communication_score': 5.0,
        'improvement_tips': []
    }

    lines = report_text.strip().split('\n')

    for line in lines:
        line = line.strip()

        if line.startswith('OVERALL_FEEDBACK:'):
            result['overall_feedback'] = line.replace(
                'OVERALL_FEEDBACK:', ''
            ).strip()

        elif line.startswith('STRONG_TOPICS:'):
            topics_str = line.replace('STRONG_TOPICS:', '').strip()
            result['strong_topics'] = [
                t.strip()
                for t in topics_str.split(',')
                if t.strip()
            ]

        elif line.startswith('WEAK_TOPICS:'):
            topics_str = line.replace('WEAK_TOPICS:', '').strip()
            result['weak_topics'] = [
                t.strip()
                for t in topics_str.split(',')
                if t.strip()
            ]

        elif line.startswith('TECHNICAL_SCORE:'):
            try:
                result['technical_score'] = float(
                    line.replace('TECHNICAL_SCORE:', '').strip()
                )
            except ValueError:
                result['technical_score'] = 5.0

        elif line.startswith('COMMUNICATION_SCORE:'):
            try:
                result['communication_score'] = float(
                    line.replace('COMMUNICATION_SCORE:', '').strip()
                )
            except ValueError:
                result['communication_score'] = 5.0

        elif line.startswith('TIP_'):
            tip = line.split(':', 1)[-1].strip()
            if tip:
                result['improvement_tips'].append(tip)

    return result