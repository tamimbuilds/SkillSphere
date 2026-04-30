from datetime import timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import CandidateProfile, User
from skills.models import Assessment, CandidateSkill, Question, Score, Skill


class AssessmentFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='candidate1',
            password='testpass123',
            role='candidate',
        )
        self.profile = CandidateProfile.objects.create(
            user=self.user,
            full_name='Candidate One',
            specialized_sector='frontend',
            university='Test University',
            department='CSE',
            cgpa=3.8,
            graduation_year=2026,
            resume_file=SimpleUploadedFile('resume.pdf', b'pdf-content'),
        )
        self.skill = Skill.objects.create(
            skill_name='React',
            category='frontend',
            description='Frontend framework',
        )
        self.candidate_skill = CandidateSkill.objects.create(
            candidate=self.profile,
            skill=self.skill,
            proficiency_level='Intermediate',
            years_of_experience='2',
        )
        for set_number in range(1, 4):
            for i in range(10):
                Question.objects.create(
                    skill=self.skill,
                    sector='frontend',
                    set_number=set_number,
                    question_order=i + 1,
                    question_text=f'Set {set_number} Question {i + 1}',
                    option_a='Option A',
                    option_b='Option B',
                    option_c='Option C',
                    option_d='Option D',
                    correct_option='A',
                )

    def test_candidate_assessment_submission_creates_first_attempt_score(self):
        self.client.login(username='candidate1', password='testpass123')
        url = reverse('add_assessment', args=[self.candidate_skill.pk])

        payload = {}
        for question in Question.objects.filter(skill=self.skill, set_number=1):
            payload[f'question_{question.pk}'] = 'A'

        response = self.client.post(url, payload)

        self.assertRedirects(response, reverse('my_skills'))
        self.assertEqual(Assessment.objects.filter(user=self.user, candidate_skill=self.candidate_skill).count(), 10)

        score = Score.objects.get(user=self.user, candidate_skill=self.candidate_skill, attempt_number=1)
        self.assertEqual(score.correct_answers, 10)
        self.assertEqual(score.total_questions, 10)
        self.assertEqual(score.score, 100.0)
        self.assertTrue(score.passed)
        self.assertEqual(score.question_set_number, 1)

        self.candidate_skill.refresh_from_db()
        self.assertTrue(self.candidate_skill.verified)

    def test_failed_attempt_uses_next_question_set(self):
        self.client.login(username='candidate1', password='testpass123')
        url = reverse('add_assessment', args=[self.candidate_skill.pk])

        first_payload = {}
        for question in Question.objects.filter(skill=self.skill, set_number=1):
            first_payload[f'question_{question.pk}'] = 'B'

        first_response = self.client.post(url, first_payload)
        self.assertRedirects(first_response, reverse('my_skills'))

        second_payload = {}
        for question in Question.objects.filter(skill=self.skill, set_number=2):
            second_payload[f'question_{question.pk}'] = 'A'

        second_response = self.client.post(url, second_payload)
        self.assertRedirects(second_response, reverse('my_skills'))

        self.assertEqual(Score.objects.filter(user=self.user, candidate_skill=self.candidate_skill).count(), 2)

        first_score = Score.objects.get(user=self.user, candidate_skill=self.candidate_skill, attempt_number=1)
        second_score = Score.objects.get(user=self.user, candidate_skill=self.candidate_skill, attempt_number=2)

        self.assertFalse(first_score.passed)
        self.assertEqual(first_score.question_set_number, 1)
        self.assertTrue(second_score.passed)
        self.assertEqual(second_score.question_set_number, 2)

        second_answers = Assessment.objects.filter(score_record=second_score)
        self.assertEqual(second_answers.count(), 10)
        self.assertTrue(all(answer.question.set_number == 2 for answer in second_answers))

    def test_expired_assessment_does_not_create_score(self):
        self.client.login(username='candidate1', password='testpass123')
        url = reverse('add_assessment', args=[self.candidate_skill.pk])

        self.client.get(url)
        session = self.client.session
        session['assessment_started_%s_%s' % (self.candidate_skill.pk, 1)] = (
            timezone.now() - timedelta(minutes=11)
        ).isoformat()
        session.save()

        payload = {}
        for question in Question.objects.filter(skill=self.skill, set_number=1):
            payload[f'question_{question.pk}'] = 'A'

        response = self.client.post(url, payload)

        self.assertRedirects(response, reverse('my_skills'))
        self.assertEqual(Score.objects.filter(user=self.user, candidate_skill=self.candidate_skill).count(), 0)
        self.assertEqual(Assessment.objects.filter(user=self.user, candidate_skill=self.candidate_skill).count(), 0)
