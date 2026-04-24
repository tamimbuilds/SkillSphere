import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillsphere.settings')
django.setup()

from skills.models import Skill

skills_data = [
    # Android App Development
    ('Kotlin', 'android'), ('Java', 'android'), ('Jetpack Compose', 'android'), ('Android SDK', 'android'),
    ('Retrofit', 'android'), ('Dagger Hilt', 'android'), ('Coroutines', 'android'), ('Room DB', 'android'),
    
    # iOS Development
    ('Swift', 'ios'), ('SwiftUI', 'ios'), ('Objective-C', 'ios'), ('Xcode', 'ios'),
    ('CocoaTouch', 'ios'), ('Combine Framework', 'ios'), ('Core Data', 'ios'), ('TestFlight', 'ios'),
    
    # Web App
    ('React', 'web_app'), ('Vue.js', 'web_app'), ('Angular', 'web_app'), ('Next.js', 'web_app'),
    ('Nuxt.js', 'web_app'), ('Svelte', 'web_app'), ('WebAssembly', 'web_app'), ('PWA', 'web_app'),
    
    # Frontend
    ('HTML5', 'frontend'), ('CSS3', 'frontend'), ('JavaScript', 'frontend'), ('TypeScript', 'frontend'),
    ('Tailwind CSS', 'frontend'), ('SASS/SCSS', 'frontend'), ('Bootstrap', 'frontend'), ('Three.js', 'frontend'),
    
    # Backend
    ('Python', 'backend'), ('Django', 'backend'), ('Flask', 'backend'), ('Node.js', 'backend'),
    ('Express.js', 'backend'), ('Go', 'backend'), ('Rust', 'backend'), ('PostgreSQL', 'backend'),
    ('MongoDB', 'backend'), ('Redis', 'backend'), ('GraphQL', 'backend'),
    
    # DevOps
    ('Docker', 'devops'), ('Kubernetes', 'devops'), ('Jenkins', 'devops'), ('GitHub Actions', 'devops'),
    ('Terraform', 'devops'), ('AWS', 'devops'), ('Azure', 'devops'), ('Google Cloud', 'devops'),
    ('Nginx', 'devops'), ('CI/CD', 'devops'),
    
    # Fullstack
    ('MERN Stack', 'fullstack'), ('MEAN Stack', 'fullstack'), ('Django + React', 'fullstack'),
    ('Laravel + Vue', 'fullstack'), ('Firebase', 'fullstack'), ('Supabase', 'fullstack'),
    
    # UI/UX Design
    ('Figma', 'ui_ux'), ('Adobe XD', 'ui_ux'), ('Sketch', 'ui_ux'), ('Prototyping', 'ui_ux'),
    ('Wireframing', 'ui_ux'), ('User Research', 'ui_ux'), ('Interaction Design', 'ui_ux'),
    ('Visual Design', 'ui_ux'),
]

for name, cat in skills_data:
    Skill.objects.get_or_create(skill_name=name, category=cat)

print(f"Successfully seeded {len(skills_data)} skills.")
