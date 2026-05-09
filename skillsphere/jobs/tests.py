from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from accounts.models import RecruiterProfile, User
from jobs.models import JobPost
from skills.models import JobSkillRequirement, Skill


class JobDetailViewTests(TestCase):
    def test_candidate_without_profile_can_view_job_detail(self):
        recruiter_user = User.objects.create_user(
            username="recruiter",
            password="pass12345",
            role="recruiter",
        )
        recruiter = RecruiterProfile.objects.create(
            user=recruiter_user,
            company_name="Acme",
            recruiter_name="Rina",
            designation="HR",
            company_email="hr@example.com",
            industry_type="Software",
            company_size=50,
        )
        job = JobPost.objects.create(
            recruiter=recruiter,
            title="Backend Developer",
            description="Build Django applications.",
            required_cgpa=3.0,
            required_experience=2,
            salary_range="$1000-$1500",
            location="Remote",
            deadline=date.today() + timedelta(days=30),
            status="open",
        )
        candidate_user = User.objects.create_user(
            username="candidate-no-profile",
            password="pass12345",
            role="candidate",
        )

        self.client.force_login(candidate_user)
        response = self.client.get(
            reverse("job_detail", kwargs={"pk": job.pk}),
            HTTP_HOST="localhost",
            secure=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Backend Developer")


class JobCreateViewTests(TestCase):
    def setUp(self):
        self.recruiter_user = User.objects.create_user(
            username="create-recruiter",
            password="pass12345",
            role="recruiter",
        )
        self.recruiter = RecruiterProfile.objects.create(
            user=self.recruiter_user,
            company_name="Acme",
            recruiter_name="Rina",
            designation="HR",
            company_email="hr@example.com",
            industry_type="Software",
            company_size=50,
        )
        self.skill = Skill.objects.create(
            skill_name="Django",
            category="backend",
        )

    def test_duplicate_required_skills_are_saved_once(self):
        self.client.force_login(self.recruiter_user)
        response = self.client.post(
            reverse("job_create"),
            {
                "title": "Django Developer",
                "description": "Build Django applications.",
                "required_cgpa": "3.0",
                "required_experience": "2",
                "salary_range": "$1000-$1500",
                "location": "Remote",
                "deadline": date.today() + timedelta(days=30),
                "status": "open",
                "req_skill": [str(self.skill.pk), str(self.skill.pk)],
                "req_level": ["beginner", "expert"],
            },
            HTTP_HOST="localhost",
            secure=True,
        )

        job = JobPost.objects.get(title="Django Developer")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(JobSkillRequirement.objects.filter(job=job).count(), 1)


class JobListViewTests(TestCase):
    def test_recruiter_can_see_own_draft_job_but_candidate_cannot(self):
        recruiter_user = User.objects.create_user(
            username="draft-recruiter",
            password="pass12345",
            role="recruiter",
        )
        recruiter = RecruiterProfile.objects.create(
            user=recruiter_user,
            company_name="Acme",
            recruiter_name="Rina",
            designation="HR",
            company_email="hr@example.com",
            industry_type="Software",
            company_size=50,
        )
        JobPost.objects.create(
            recruiter=recruiter,
            title="Private Draft Role",
            description="Not public yet.",
            required_cgpa=3.0,
            required_experience=2,
            salary_range="$1000-$1500",
            location="Remote",
            deadline=date.today() + timedelta(days=30),
            status="draft",
        )

        self.client.force_login(recruiter_user)
        recruiter_response = self.client.get(
            reverse("job_list"),
            HTTP_HOST="localhost",
            secure=True,
        )
        self.assertContains(recruiter_response, "Private Draft Role")

        candidate_user = User.objects.create_user(
            username="draft-candidate",
            password="pass12345",
            role="candidate",
        )
        self.client.force_login(candidate_user)
        candidate_response = self.client.get(
            reverse("job_list"),
            HTTP_HOST="localhost",
            secure=True,
        )
        self.assertNotContains(candidate_response, "Private Draft Role")
