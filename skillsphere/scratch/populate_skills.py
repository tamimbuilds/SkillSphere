
import os
import django
import sys

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillsphere.settings')
django.setup()

from skills.models import Skill

def populate_skills():
    skills_data = [
        # Android
        ('Kotlin', 'android', 'Primary language for Android.'),
        ('Java (Android)', 'android', 'Legacy Android development.'),
        ('Jetpack Compose', 'android', 'Modern UI toolkit for Android.'),
        ('Android SDK', 'android', 'Software development kit for Android.'),
        ('Retrofit', 'android', 'Type-safe HTTP client for Android.'),
        
        # iOS
        ('Swift', 'ios', 'Primary language for iOS.'),
        ('Objective-C', 'ios', 'Legacy iOS development.'),
        ('SwiftUI', 'ios', 'Declarative UI framework for iOS.'),
        ('UIKit', 'ios', 'Traditional UI framework for iOS.'),
        ('Core Data', 'ios', 'Data persistence for iOS.'),
        
        # Web App
        ('React', 'web_app', 'Library for user interfaces.'),
        ('Next.js', 'web_app', 'React framework for production.'),
        ('Vue.js', 'web_app', 'Progressive JS framework.'),
        ('Nuxt.js', 'web_app', 'Vue framework.'),
        ('Angular', 'web_app', 'Platform for web apps.'),
        
        # Frontend
        ('HTML5', 'frontend', 'Standard markup.'),
        ('CSS3', 'frontend', 'Styling language.'),
        ('JavaScript', 'frontend', 'Core web scripting.'),
        ('Tailwind CSS', 'frontend', 'Utility-first CSS.'),
        ('TypeScript', 'frontend', 'Typed JavaScript.'),
        ('Sass', 'frontend', 'CSS extension.'),
        
        # Backend
        ('Python', 'backend', 'Versatile backend language.'),
        ('Django', 'backend', 'Python web framework.'),
        ('Node.js', 'backend', 'JavaScript runtime.'),
        ('Express.js', 'backend', 'Node.js framework.'),
        ('PostgreSQL', 'backend', 'Relational database.'),
        ('MongoDB', 'backend', 'NoSQL database.'),
        
        # DevOps
        ('Docker', 'devops', 'Containerization.'),
        ('Kubernetes', 'devops', 'Orchestration.'),
        ('AWS', 'devops', 'Cloud services.'),
        ('CI/CD', 'devops', 'Automation.'),
        ('Terraform', 'devops', 'Infrastructure as code.'),
        
        # Fullstack
        ('MERN Stack', 'fullstack', 'MongoDB, Express, React, Node.'),
        ('Django + React', 'fullstack', 'Django and React combination.'),
        ('T3 Stack', 'fullstack', 'Next.js, TS, Tailwind.'),
        ('LAMP Stack', 'fullstack', 'Linux, Apache, MySQL, PHP.'),
        
        # UI/UX
        ('Figma', 'ui_ux', 'Collaborative interface design tool.'),
        ('Adobe XD', 'ui_ux', 'UI/UX design and prototyping.'),
        ('User Research', 'ui_ux', 'Understanding user needs.'),
        ('Wireframing', 'ui_ux', 'Creating low-fidelity blueprints.'),
        ('Prototyping', 'ui_ux', 'Building interactive models.'),
        ('Typography', 'ui_ux', 'Designing with text.'),
        ('Sketch', 'ui_ux', 'Vector graphics editor.'),
        ('InVision', 'ui_ux', 'Prototyping and workflow platform.'),
        ('Principle', 'ui_ux', 'Animated and interactive user interface design.'),

        # More Android
        ('Flutter', 'android', 'Cross-platform framework (Google).'),
        ('Android NDK', 'android', 'Native development kit.'),
        ('Firebase', 'android', 'Backend for mobile apps.'),

        # More iOS
        ('Combine', 'ios', 'Reactive programming for Apple platforms.'),
        ('Metal', 'ios', 'GPU-accelerated graphics.'),
        ('XCTest', 'ios', 'Testing framework for iOS.'),

        # More Web App
        ('Svelte', 'web_app', 'Cybernetic web framework.'),
        ('SolidJS', 'web_app', 'Reactive JS library.'),
        ('Remix', 'web_app', 'Full-stack web framework.'),

        # More Frontend
        ('Bootstrap', 'frontend', 'CSS framework.'),
        ('Material UI', 'frontend', 'React component library.'),
        ('Webpack', 'frontend', 'Module bundler.'),

        # More Backend
        ('Go', 'backend', 'Cloud-native backend language.'),
        ('Ruby on Rails', 'backend', 'Productive web framework.'),
        ('FastAPI', 'backend', 'Modern Python web framework.'),
        ('GraphQL', 'backend', 'Query language for APIs.'),

        # More DevOps
        ('Ansible', 'devops', 'Configuration management.'),
        ('Jenkins', 'devops', 'Automation server.'),
        ('Prometheus', 'devops', 'Monitoring system.'),

        # More Fullstack
        ('MEAN Stack', 'fullstack', 'MongoDB, Express, Angular, Node.'),
        ('Ruby on Rails + React', 'fullstack', 'Rails backend with React frontend.'),
        ('Go + Next.js', 'fullstack', 'Go backend with Next.js frontend.'),
    ]

    for name, cat, desc in skills_data:
        Skill.objects.get_or_create(skill_name=name, category=cat, defaults={'description': desc})
        print(f"Added skill: {name} ({cat})")

if __name__ == "__main__":
    populate_skills()
