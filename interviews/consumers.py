import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import get_user_model

User = get_user_model()


class InterviewConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f'interview_{self.session_id}'

        token = self.get_token_from_query()
        self.user = await self.get_user_from_token(token)

        if not self.user or isinstance(self.user, AnonymousUser):
            await self.close()
            return

        session = await self.get_session()
        if not session:
            await self.close()
            return

        self.session = session

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connected to interview session',
            'session_id': self.session_id
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'begin_interview':
                await self.handle_begin_interview()
            elif message_type == 'send_answer':
                answer = data.get('message', '').strip()
                if answer:
                    await self.handle_answer(answer)
                else:
                    await self.send(text_data=json.dumps({
                        'type': 'error',
                        'message': 'Answer cannot be empty'
                    }))
            elif message_type == 'end_interview':
                await self.handle_end_interview()

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON'
            }))

    async def handle_begin_interview(self):
        from agents.interview_agent import get_interviewer_response

        if self.session.status != 'ongoing':
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Session must be started first'
            }))
            return

        session_config = await self.get_session_config()
        user_profile = await self.get_user_profile()

        await self.send(text_data=json.dumps({
            'type': 'interviewer_typing',
            'message': 'Interviewer is preparing first question...'
        }))

        opening_message = await database_sync_to_async(
            get_interviewer_response
        )(
            session_config=session_config,
            user_profile=user_profile,
            conversation_history=[],
            last_score=None
        )

        await self.save_message('interviewer', opening_message)

        await self.send(text_data=json.dumps({
            'type': 'interviewer_message',
            'message': opening_message,
            'questions_asked': self.session.questions_asked,
            'total_questions': self.session.total_questions
        }))

    async def handle_answer(self, answer):
        from agents.interview_agent import (
            get_interviewer_response,
            evaluate_answer
        )

        self.session = await self.get_session()

        if self.session.questions_asked >= self.session.total_questions:
            await self.send(text_data=json.dumps({
                'type': 'interview_complete',
                'message': 'Interview is complete!'
            }))
            return

        last_question = await self.get_last_question()

        await self.send(text_data=json.dumps({
            'type': 'evaluating',
            'message': 'Evaluating your answer...'
        }))

        evaluation = None
        if last_question:
            evaluation = await database_sync_to_async(
                evaluate_answer
            )(
                question=last_question,
                answer=answer,
                interview_type=self.session.interview_type,
                difficulty=self.session.difficulty
            )

        await self.save_candidate_message(
            answer,
            evaluation['score'] if evaluation else None,
            evaluation['feedback'] if evaluation else None
        )

        if evaluation:
            await self.send(text_data=json.dumps({
                'type': 'evaluation_result',
                'score': evaluation['score'],
                'feedback': evaluation['feedback'],
                'strong_points': evaluation['strong_points'],
                'weak_points': evaluation['weak_points'],
            }))

        await self.increment_questions()
        self.session = await self.get_session()

        if self.session.questions_asked >= self.session.total_questions:
            await self.send(text_data=json.dumps({
                'type': 'interview_complete',
                'message': 'Interview complete! You can now generate your report.'
            }))
            return

        await self.send(text_data=json.dumps({
            'type': 'interviewer_typing',
            'message': 'Preparing next question...'
        }))

        session_config = await self.get_session_config()
        user_profile = await self.get_user_profile()
        history = await self.get_conversation_history()

        next_question = await database_sync_to_async(
            get_interviewer_response
        )(
            session_config=session_config,
            user_profile=user_profile,
            conversation_history=history,
            last_score=evaluation['score'] if evaluation else None
        )

        await self.save_message('interviewer', next_question)

        await self.send(text_data=json.dumps({
            'type': 'interviewer_message',
            'message': next_question,
            'questions_asked': self.session.questions_asked,
            'total_questions': self.session.total_questions
        }))

    async def handle_end_interview(self):
        await self.end_session()
        await self.send(text_data=json.dumps({
            'type': 'session_ended',
            'message': 'Interview session ended successfully'
        }))

    def get_token_from_query(self):
        query_string = self.scope.get('query_string', b'').decode()
        for param in query_string.split('&'):
            if param.startswith('token='):
                return param.split('=', 1)[1]
        return None

    @database_sync_to_async
    def get_user_from_token(self, token):
        if not token:
            return None
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            return User.objects.get(id=user_id)
        except (TokenError, User.DoesNotExist):
            return None

    @database_sync_to_async
    def get_session(self):
        from interviews.models import InterviewSession
        try:
            return InterviewSession.objects.get(
                id=self.session_id,
                user=self.user
            )
        except InterviewSession.DoesNotExist:
            return None

    @database_sync_to_async
    def get_session_config(self):
        return {
            'interview_type': self.session.interview_type,
            'difficulty': self.session.difficulty,
            'target_company': self.session.target_company,
            'total_questions': self.session.total_questions,
            'questions_asked': self.session.questions_asked,
        }

    @database_sync_to_async
    def get_user_profile(self):
        return {
            'experience_level': self.user.experience_level,
            'target_role': self.user.target_role,
            'skills': self.user.skills or [],
            'resume_text': self.user.resume_text or '',
        }

    @database_sync_to_async
    def get_last_question(self):
        msg = self.session.messages.filter(
            role='interviewer'
        ).last()
        return msg.content if msg else None

    @database_sync_to_async
    def get_conversation_history(self):
        messages = self.session.messages.all().order_by('timestamp')
        history = []
        for msg in messages:
            if msg.role in ['interviewer', 'candidate']:
                history.append({
                    'role': msg.role,
                    'content': msg.content
                })
        return history

    @database_sync_to_async
    def save_message(self, role, content):
        from interviews.models import Message
        return Message.objects.create(
            session=self.session,
            role=role,
            content=content
        )

    @database_sync_to_async
    def save_candidate_message(self, content, score, feedback):
        from interviews.models import Message
        return Message.objects.create(
            session=self.session,
            role='candidate',
            content=content,
            score=score,
            feedback=feedback
        )

    @database_sync_to_async
    def increment_questions(self):
        from interviews.models import InterviewSession
        InterviewSession.objects.filter(
            id=self.session_id
        ).update(
            questions_asked=self.session.questions_asked + 1
        )

    @database_sync_to_async
    def end_session(self):
        from django.utils import timezone
        from interviews.models import InterviewSession
        InterviewSession.objects.filter(
            id=self.session_id
        ).update(
            status='completed',
            ended_at=timezone.now()
        )