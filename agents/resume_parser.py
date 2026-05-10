import os
import pdfplumber
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()


def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return ""
    return text.strip()


def parse_resume_with_ai(resume_text):
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile",
        temperature=0.1,
        max_tokens=1000
    )

    system_prompt = """
You are a resume parser. Extract information from the resume text.
Respond in this EXACT format and nothing else:

SKILLS: skill1, skill2, skill3, skill4
EXPERIENCE_YEARS: <number or 0 for fresher>
PROJECTS: project1 name | project2 name | project3 name
EDUCATION: <degree and college name>
SUMMARY: <2 sentence professional summary>

Rules:
- SKILLS: only technical skills (Python, Django, React etc.)
- Maximum 15 skills
- EXPERIENCE_YEARS: just a number like 0 or 2
- PROJECTS: just project names separated by |
- Keep everything on single lines
"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(
            content=f"Parse this resume:\n\n{resume_text[:3000]}"
        )
    ]

    response = llm.invoke(messages)
    return parse_ai_response(response.content)


def parse_ai_response(response_text):
    result = {
        'skills': [],
        'experience_years': 0,
        'projects': [],
        'education': '',
        'summary': ''
    }

    lines = response_text.strip().split('\n')

    for line in lines:
        line = line.strip()

        if line.startswith('SKILLS:'):
            skills_str = line.replace('SKILLS:', '').strip()
            result['skills'] = [
                s.strip()
                for s in skills_str.split(',')
                if s.strip()
            ]

        elif line.startswith('EXPERIENCE_YEARS:'):
            try:
                years_str = line.replace(
                    'EXPERIENCE_YEARS:', ''
                ).strip()
                result['experience_years'] = int(
                    float(years_str)
                )
            except ValueError:
                result['experience_years'] = 0

        elif line.startswith('PROJECTS:'):
            projects_str = line.replace('PROJECTS:', '').strip()
            result['projects'] = [
                p.strip()
                for p in projects_str.split('|')
                if p.strip()
            ]

        elif line.startswith('EDUCATION:'):
            result['education'] = line.replace(
                'EDUCATION:', ''
            ).strip()

        elif line.startswith('SUMMARY:'):
            result['summary'] = line.replace(
                'SUMMARY:', ''
            ).strip()

    return result


def process_resume(user):
    if not user.resume:
        return {'error': 'No resume uploaded'}

    resume_text = extract_text_from_pdf(user.resume.path)

    if not resume_text:
        return {'error': 'Could not extract text from PDF'}

    parsed_data = parse_resume_with_ai(resume_text)

    user.resume_text = resume_text
    user.skills = parsed_data['skills']
    user.profile_completed = True
    user.save()

    return {
        'success': True,
        'skills': parsed_data['skills'],
        'projects': parsed_data['projects'],
        'education': parsed_data['education'],
        'summary': parsed_data['summary'],
        'experience_years': parsed_data['experience_years']
    }