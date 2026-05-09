import random
from django.core.management.base import BaseCommand
from django.db import transaction
from skills.models import Skill, Question

class Command(BaseCommand):
    help = 'Seeds assessment questions for all skills. 3 sets of 10 questions per skill.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting question seeding process...')

        CURATED_QUESTION_SETS = {
            ('Node.js', 1): [
                {
                    'question_text': 'Which runtime is commonly used to execute Node.js applications?',
                    'options': {
                        'A': 'Java Virtual Machine only',
                        'B': 'CPython interpreter',
                        'C': 'Chrome V8 JavaScript engine',
                        'D': 'Ruby MRI only',
                    },
                    'correct_option': 'C',
                },
                {
                    'question_text': 'Which file usually stores metadata and dependencies for a Node.js project?',
                    'options': {
                        'A': 'requirements.txt',
                        'B': 'package.json',
                        'C': 'pom.xml',
                        'D': 'composer.json',
                    },
                    'correct_option': 'B',
                },
                {
                    'question_text': 'Which object is commonly used in Express.js route handlers to send a response?',
                    'options': {
                        'A': 'res',
                        'B': 'req',
                        'C': 'next',
                        'D': 'module',
                    },
                    'correct_option': 'A',
                },
                {
                    'question_text': 'Which HTTP method is most appropriate for creating a new resource in a REST API?',
                    'options': {
                        'A': 'POST',
                        'B': 'GET',
                        'C': 'HEAD',
                        'D': 'OPTIONS',
                    },
                    'correct_option': 'A',
                },
                {
                    'question_text': 'Which module system keyword is used by CommonJS to import a module?',
                    'options': {
                        'A': 'include',
                        'B': 'using',
                        'C': 'import-only',
                        'D': 'require',
                    },
                    'correct_option': 'D',
                },
                {
                    'question_text': 'Why is asynchronous programming important in Node.js?',
                    'options': {
                        'A': 'It disables the event loop',
                        'B': 'It makes CSS render faster',
                        'C': 'It helps handle non-blocking I/O operations',
                        'D': 'It prevents all database usage',
                    },
                    'correct_option': 'C',
                },
                {
                    'question_text': 'Which command is commonly used to install a package in a Node.js project?',
                    'options': {
                        'A': 'pip install package',
                        'B': 'composer require package',
                        'C': 'npm install package',
                        'D': 'gem install package',
                    },
                    'correct_option': 'C',
                },
                {
                    'question_text': 'What is middleware in an Express.js application?',
                    'options': {
                        'A': 'A function that can process requests before the final route handler',
                        'B': 'A CSS layout technique',
                        'C': 'A database table type',
                        'D': 'A browser-only animation API',
                    },
                    'correct_option': 'A',
                },
                {
                    'question_text': 'Which practice helps secure user input in a Node.js API?',
                    'options': {
                        'A': 'Validate and sanitize input before using it',
                        'B': 'Store passwords in plain text',
                        'C': 'Commit API keys to the repository',
                        'D': 'Disable error handling',
                    },
                    'correct_option': 'A',
                },
                {
                    'question_text': 'What does the Node.js event loop help manage?',
                    'options': {
                        'A': 'Asynchronous callbacks and non-blocking tasks',
                        'B': 'Image editing layers',
                        'C': 'HTML tag names only',
                        'D': 'Operating system themes',
                    },
                    'correct_option': 'A',
                },
            ],
        }

        SECTOR_TEMPLATES = {
            'android': [
                "What is the primary language used alongside {skill} for Android?",
                "How does {skill} handle activity lifecycles?",
                "Which layout manager works best with {skill}?",
                "What is the best way to handle background tasks using {skill}?",
                "How does {skill} improve Android UI rendering?",
                "Which architecture pattern is recommended when using {skill}?",
                "How do you manage state in Android with {skill}?",
                "What is a common memory leak source when using {skill}?",
                "How does {skill} interact with the Android Manifest?",
                "What is the standard way to test {skill} components in Android?"
            ],
            'ios': [
                "How does {skill} integrate with Swift UI?",
                "What is the primary memory management model used by {skill} in iOS?",
                "How does {skill} handle asynchronous operations?",
                "Which design pattern is most common for {skill} in iOS?",
                "How do you debug {skill} effectively in Xcode?",
                "What is the standard approach to networking with {skill}?",
                "How does {skill} handle Core Data integration?",
                "What is the best way to manage dependencies for {skill}?",
                "How do you optimize {skill} for iOS performance?",
                "What is the standard way to write unit tests for {skill} in iOS?"
            ],
            'frontend': [
                "What is the virtual DOM's relationship with {skill}?",
                "How does {skill} handle cross-site scripting (XSS) prevention?",
                "What is the standard way to manage global state with {skill}?",
                "How do you optimize rendering performance in {skill}?",
                "What is the recommended approach for routing in {skill}?",
                "How does {skill} handle asynchronous data fetching?",
                "Which CSS approach works best with {skill}?",
                "How do you manage component lifecycles in {skill}?",
                "What is the best way to handle forms in {skill}?",
                "How do you test {skill} frontend components effectively?"
            ],
            'backend': [
                "How does {skill} handle database connections?",
                "What is the primary method for securing APIs in {skill}?",
                "How do you implement caching with {skill}?",
                "Which design pattern is best suited for {skill} microservices?",
                "How does {skill} handle asynchronous task queues?",
                "What is the standard approach to error logging in {skill}?",
                "How do you optimize database queries when using {skill}?",
                "What is the best way to manage environment variables in {skill}?",
                "How does {skill} handle rate limiting?",
                "How do you write integration tests for {skill} backend services?"
            ],
            'devops': [
                "How does {skill} integrate into CI/CD pipelines?",
                "What is the primary method for managing infrastructure with {skill}?",
                "How do you handle secrets management in {skill}?",
                "Which containerization strategy works best with {skill}?",
                "How does {skill} handle rolling deployments?",
                "What is the standard approach to monitoring in {skill}?",
                "How do you manage log aggregation with {skill}?",
                "What is the best way to implement auto-scaling in {skill}?",
                "How does {skill} ensure high availability?",
                "How do you test infrastructure changes in {skill}?"
            ],
            'data_science': [
                "What is the primary data structure used by {skill}?",
                "How does {skill} handle missing values in datasets?",
                "What is the best way to optimize {skill} for large datasets?",
                "Which machine learning model works best with {skill}?",
                "How do you evaluate model performance using {skill}?",
                "What is the standard approach to feature scaling in {skill}?",
                "How does {skill} handle cross-validation?",
                "What is the best way to deploy a {skill} model to production?",
                "How do you manage hyperparameter tuning with {skill}?",
                "How does {skill} handle imbalanced datasets?"
            ],
            'mobile': [
                "What is the primary cross-platform strategy for {skill}?",
                "How does {skill} handle native device features?",
                "What is the best way to manage state in a {skill} mobile app?",
                "Which routing library is recommended for {skill}?",
                "How does {skill} handle offline data persistence?",
                "What is the standard approach to push notifications in {skill}?",
                "How do you optimize {skill} for low-end mobile devices?",
                "What is the best way to handle deep linking in {skill}?",
                "How does {skill} ensure app security?",
                "How do you automate testing for {skill} mobile apps?"
            ],
            'ui_ux': [
                "How does {skill} improve the overall user experience?",
                "What is the primary design principle behind {skill}?",
                "How do you ensure accessibility (a11y) when using {skill}?",
                "Which prototyping tool integrates best with {skill} workflows?",
                "How does {skill} handle responsive design?",
                "What is the standard approach to user testing with {skill}?",
                "How do you maintain design consistency using {skill}?",
                "What is the best way to implement micro-animations in {skill}?",
                "How does {skill} address cognitive load?",
                "How do you measure the success of a {skill} design implementation?"
            ],
            'web_app': [
                "How does {skill} improve overall web application performance?",
                "What is the primary architectural pattern used with {skill}?",
                "How do you ensure security best practices when using {skill}?",
                "Which deployment strategy works best with {skill}?",
                "How does {skill} handle session management?",
                "What is the standard approach to SEO optimization in {skill}?",
                "How do you maintain code quality in a {skill} project?",
                "What is the best way to implement real-time features in {skill}?",
                "How does {skill} address cross-browser compatibility?",
                "How do you measure the success of a {skill} implementation?"
            ],
            'fullstack': [
                "How does {skill} bridge the gap between frontend and backend?",
                "What is the primary communication protocol used with {skill}?",
                "How do you ensure end-to-end security when using {skill}?",
                "Which database type pairs best with {skill}?",
                "How does {skill} handle complex state management across the stack?",
                "What is the standard approach to deployment for a {skill} app?",
                "How do you maintain separation of concerns in a {skill} project?",
                "What is the best way to implement authentication in {skill}?",
                "How does {skill} address scalability issues?",
                "How do you write end-to-end tests for a {skill} application?"
            ]
        }

        GENERIC_TEMPLATES = [
            "What is the main purpose of using {skill}?",
            "Which of the following is a key feature of {skill}?",
            "What is a common best practice when working with {skill}?",
            "How does {skill} handle error management?",
            "What is the typical learning curve associated with {skill}?",
            "In professional environments, how does {skill} improve productivity?",
            "Which design pattern is frequently implemented using {skill}?",
            "How is state or data typically managed in {skill} applications?",
            "What is a known limitation of {skill}?",
            "Which tool is most commonly paired with {skill}?"
        ]

        # The first option in each tuple is the intended correct answer.
        # The options are shuffled per question, so we compute the final
        # correct letter after shuffling instead of choosing one randomly.
        OPTIONS = [
            ("It improves performance", "It reduces security", "It is only for beginners", "It has no real impact"),
            ("Using specific design patterns", "Ignoring best practices", "Relying purely on documentation", "Guessing the syntax"),
            ("Yes, it is highly recommended", "No, it should be avoided", "Only in rare edge cases", "It depends entirely on the OS"),
            ("Option A is generally correct", "Option B is generally correct", "Option C is generally correct", "Option D is generally correct"),
            ("By utilizing advanced caching", "By downloading more RAM", "By ignoring user input", "By slowing down the main thread"),
            ("It is extremely difficult", "It is relatively straightforward", "It is impossible to master", "It requires 10 years of experience"),
            ("It uses a centralized store", "It relies on global variables", "It does not manage state", "It uses a decentralized chaotic approach"),
            ("It is a major security risk", "It is completely safe", "It requires manual intervention", "It works automatically without setup"),
            ("It integrates seamlessly", "It requires complete rewrites", "It is incompatible", "It works only on Tuesdays"),
            ("By writing comprehensive tests", "By pushing straight to production", "By hoping for the best", "By asking users to find bugs")
        ]
        option_letters = ['A', 'B', 'C', 'D']
        correct_texts = {option_set[0] for option_set in OPTIONS}

        def get_correct_option(options):
            for index, option_text in enumerate(options):
                if option_text in correct_texts:
                    return option_letters[index]
            return None

        skills = Skill.objects.all()
        if not skills.exists():
            self.stdout.write(self.style.WARNING("No skills found in the database. Please add skills first."))
            return

        total_questions_created = 0
        total_questions_repaired = 0
        total_curated_questions_updated = 0

        with transaction.atomic():
            for skill in skills:
                sector = skill.category

                for (skill_name, set_number), curated_questions in CURATED_QUESTION_SETS.items():
                    if skill.skill_name != skill_name:
                        continue

                    for question_order, curated_question in enumerate(curated_questions, start=1):
                        question, created = Question.objects.update_or_create(
                            skill=skill,
                            set_number=set_number,
                            question_order=question_order,
                            defaults={
                                'sector': sector,
                                'question_text': curated_question['question_text'],
                                'option_a': curated_question['options']['A'],
                                'option_b': curated_question['options']['B'],
                                'option_c': curated_question['options']['C'],
                                'option_d': curated_question['options']['D'],
                                'correct_option': curated_question['correct_option'],
                                'is_active': True,
                            },
                        )
                        if created:
                            total_questions_created += 1
                        else:
                            total_curated_questions_updated += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Upserted curated set {set_number} for skill '{skill.skill_name}'"
                        )
                    )

                questions_to_update = []
                existing_questions = Question.objects.filter(skill=skill)
                for existing_question in existing_questions.iterator():
                    repaired_correct_option = get_correct_option([
                        existing_question.option_a,
                        existing_question.option_b,
                        existing_question.option_c,
                        existing_question.option_d,
                    ])
                    if repaired_correct_option and existing_question.correct_option != repaired_correct_option:
                        existing_question.correct_option = repaired_correct_option
                        questions_to_update.append(existing_question)

                if questions_to_update:
                    Question.objects.bulk_update(questions_to_update, ['correct_option'])
                    total_questions_repaired += len(questions_to_update)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Repaired {len(questions_to_update)} answer keys for skill '{skill.skill_name}'"
                        )
                    )

                # Fetch existing questions to avoid creating duplicates
                existing_questions_count = existing_questions.count()
                if existing_questions_count >= 30:
                    self.stdout.write(f"Skill '{skill.skill_name}' already has {existing_questions_count} questions. Skipping.")
                    continue

                # We need exactly 3 sets of 10 questions per skill.
                templates = SECTOR_TEMPLATES.get(sector, GENERIC_TEMPLATES)
                
                questions_to_create = []
                
                for set_number in range(1, 4):
                    # For each set, we want 10 questions
                    # We will shuffle the templates for variety but ensure 10 are used
                    shuffled_templates = list(templates)
                    random.shuffle(shuffled_templates)
                    
                    # If we don't have enough templates, cycle through them
                    while len(shuffled_templates) < 10:
                        shuffled_templates.extend(templates)
                    
                    for question_order in range(1, 11):
                        # Check if this specific question already exists
                        if Question.objects.filter(skill=skill, set_number=set_number, question_order=question_order).exists():
                            continue
                            
                        template = shuffled_templates[question_order - 1]
                        question_text = template.format(skill=skill.skill_name)
                        
                        # Pick random options while preserving the correct answer key.
                        option_set = random.choice(OPTIONS)
                        correct_option_text = option_set[0]
                        opts = list(option_set)
                        random.shuffle(opts)
                        correct_opt_letter = option_letters[opts.index(correct_option_text)]
                        
                        question = Question(
                            skill=skill,
                            sector=sector,
                            set_number=set_number,
                            question_order=question_order,
                            question_text=question_text,
                            option_a=opts[0],
                            option_b=opts[1],
                            option_c=opts[2],
                            option_d=opts[3],
                            correct_option=correct_opt_letter,
                            is_active=True
                        )
                        questions_to_create.append(question)

                if questions_to_create:
                    Question.objects.bulk_create(questions_to_create)
                    total_questions_created += len(questions_to_create)
                    self.stdout.write(self.style.SUCCESS(f"Created {len(questions_to_create)} questions for skill '{skill.skill_name}'"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded {total_questions_created} new questions, repaired {total_questions_repaired} answer keys, and updated {total_curated_questions_updated} curated questions!"
            )
        )
