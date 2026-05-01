from django.core.management.base import BaseCommand
from skills.models import Skill

class Command(BaseCommand):
    help = 'Seeds initial skills into the database'

    def handle(self, *args, **kwargs):
        skills_data = [
            # Frontend
            {'skill_name': 'React.js', 'category': 'frontend', 'description': 'A JavaScript library for building user interfaces.'},
            {'skill_name': 'Vue.js', 'category': 'frontend', 'description': 'The Progressive JavaScript Framework.'},
            {'skill_name': 'Angular', 'category': 'frontend', 'description': 'A platform for building mobile and desktop web applications.'},
            {'skill_name': 'Next.js', 'category': 'frontend', 'description': 'The React Framework for Production.'},
            {'skill_name': 'Tailwind CSS', 'category': 'frontend', 'description': 'A utility-first CSS framework.'},
            
            # Backend
            {'skill_name': 'Django', 'category': 'backend', 'description': 'A high-level Python web framework.'},
            {'skill_name': 'Node.js', 'category': 'backend', 'description': "JavaScript runtime built on Chrome's V8 JavaScript engine."},
            {'skill_name': 'Spring Boot', 'category': 'backend', 'description': 'Build-anything with Spring.'},
            {'skill_name': 'PostgreSQL', 'category': 'backend', 'description': 'The World\'s Most Advanced Open Source Relational Database.'},
            {'skill_name': 'Redis', 'category': 'backend', 'description': 'The open source, in-memory data store used by millions of developers.'},
            
            # Fullstack
            {'skill_name': 'MERN Stack', 'category': 'fullstack', 'description': 'MongoDB, Express, React, Node.'},
            {'skill_name': 'PERN Stack', 'category': 'fullstack', 'description': 'PostgreSQL, Express, React, Node.'},
            {'skill_name': 'Django + React', 'category': 'fullstack', 'description': 'Fullstack development with Django and React.'},
            
            # Mobile
            {'skill_name': 'React Native', 'category': 'mobile', 'description': 'Learn once, write anywhere.'},
            {'skill_name': 'Flutter', 'category': 'mobile', 'description': 'Build apps for any screen.'},
            
            # Android
            {'skill_name': 'Kotlin', 'category': 'android', 'description': 'A modern programming language that makes developers happier.'},
            {'skill_name': 'Android Jetpack', 'category': 'android', 'description': 'A suite of libraries to help developers follow best practices.'},
            
            # iOS
            {'skill_name': 'Swift', 'category': 'ios', 'description': 'The powerful programming language that is also easy to learn.'},
            {'skill_name': 'SwiftUI', 'category': 'ios', 'description': 'Build better apps. Less code.'},
            
            # DevOps
            {'skill_name': 'Docker', 'category': 'devops', 'description': 'Accelerate how you build, share, and run modern applications.'},
            {'skill_name': 'Kubernetes', 'category': 'devops', 'description': 'Production-Grade Container Orchestration.'},
            {'skill_name': 'AWS', 'category': 'devops', 'description': 'Cloud computing services.'},
            
            # Data Science
            {'skill_name': 'Python for Data Science', 'category': 'data_science', 'description': 'NumPy, Pandas, Scikit-learn, etc.'},
            {'skill_name': 'TensorFlow', 'category': 'data_science', 'description': 'An end-to-end open source platform for machine learning.'},
            {'skill_name': 'PyTorch', 'category': 'data_science', 'description': 'An open source machine learning framework.'},
            
            # UI/UX
            {'skill_name': 'Figma', 'category': 'ui_ux', 'description': 'The collaborative interface design tool.'},
            {'skill_name': 'Adobe XD', 'category': 'ui_ux', 'description': 'Fast and powerful UI/UX design and prototyping tool.'},
            
            # Web App (General)
            {'skill_name': 'Laravel', 'category': 'web_app', 'description': 'The PHP Framework for Web Artisans.'},
            {'skill_name': 'Ruby on Rails', 'category': 'web_app', 'description': 'Web development that doesn\'t hurt.'},
        ]

        self.stdout.write('Starting skill seeding...')
        
        created_count = 0
        for skill in skills_data:
            obj, created = Skill.objects.get_or_create(
                skill_name=skill['skill_name'],
                category=skill['category'],
                defaults={'description': skill['description']}
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created skill: {obj.skill_name} ({obj.category})'))
            else:
                self.stdout.write(f'Skill already exists: {obj.skill_name}')

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {created_count} new skills.'))
