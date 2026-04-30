from django.core.management.base import BaseCommand

from skills.models import Question, Skill


QUESTION_SETS = [
    [
        {
            'question_text': "Which statement best describes the primary role of {skill} in {sector} work?",
            'option_a': "It helps solve domain-specific tasks in {sector}.",
            'option_b': "It is only used for payroll accounting.",
            'option_c': "It replaces the need for all testing.",
            'option_d': "It can only be used without source control.",
            'correct_option': 'A',
        },
        {
            'question_text': "When starting a project with {skill}, what is the best first step?",
            'option_a': "Delete the default configuration before reading it.",
            'option_b': "Understand the requirements and setup for {skill}.",
            'option_c': "Deploy to production before local testing.",
            'option_d': "Skip documentation and copy random code snippets.",
            'correct_option': 'B',
        },
        {
            'question_text': "Which habit most improves maintainability when using {skill}?",
            'option_a': "Writing clear, modular code and naming things well.",
            'option_b': "Putting all logic in one very long file.",
            'option_c': "Avoiding comments, tests, and structure.",
            'option_d': "Changing libraries every day.",
            'correct_option': 'A',
        },
        {
            'question_text': "What is the safest way to validate a change built with {skill}?",
            'option_a': "Assume it works because the code compiles.",
            'option_b': "Ask users to find bugs in production first.",
            'option_c': "Test the change in a controlled environment.",
            'option_d': "Only check the UI color.",
            'correct_option': 'C',
        },
        {
            'question_text': "Why is version control important in {sector} projects using {skill}?",
            'option_a': "It makes collaboration and rollback easier.",
            'option_b': "It permanently prevents all bugs.",
            'option_c': "It removes the need for reviews.",
            'option_d': "It is only useful for design files.",
            'correct_option': 'A',
        },
        {
            'question_text': "Which action is most helpful when debugging an issue in {skill}?",
            'option_a': "Changing several unrelated files at once.",
            'option_b': "Reproducing the problem and isolating the cause.",
            'option_c': "Ignoring logs and error messages.",
            'option_d': "Restarting the machine repeatedly without checking anything.",
            'correct_option': 'B',
        },
        {
            'question_text': "What is a good performance mindset when working with {skill}?",
            'option_a': "Measure first, then optimize the real bottleneck.",
            'option_b': "Optimize everything before the feature works.",
            'option_c': "Avoid profiling and benchmarking.",
            'option_d': "Always choose the most complex solution.",
            'correct_option': 'A',
        },
        {
            'question_text': "Which practice improves team collaboration on {skill}-based features?",
            'option_a': "Keeping changes secret until launch day.",
            'option_b': "Using small pull requests and clear communication.",
            'option_c': "Skipping code reviews for speed.",
            'option_d': "Using different naming styles in every file.",
            'correct_option': 'B',
        },
        {
            'question_text': "What should happen before releasing a {skill} feature to users?",
            'option_a': "Nothing, release immediately.",
            'option_b': "Delete the previous working version.",
            'option_c': "Verify functionality, stability, and expected behavior.",
            'option_d': "Rename variables and ship.",
            'correct_option': 'C',
        },
        {
            'question_text': "Which statement about learning {skill} is most accurate?",
            'option_a': "Strong fundamentals matter more than memorizing tricks.",
            'option_b': "Only shortcuts matter.",
            'option_c': "Best practices never change.",
            'option_d': "Documentation is never useful.",
            'correct_option': 'A',
        },
    ],
    [
        {
            'question_text': "In a real {sector} project, why would a team choose {skill}?",
            'option_a': "Because it can support relevant project needs.",
            'option_b': "Because it automatically removes all deadlines.",
            'option_c': "Because it guarantees zero maintenance forever.",
            'option_d': "Because it works without any project planning.",
            'correct_option': 'A',
        },
        {
            'question_text': "What is the most reliable way to grow proficiency in {skill}?",
            'option_a': "Avoid building anything practical.",
            'option_b': "Practice with real tasks and review feedback.",
            'option_c': "Memorize terms without using them.",
            'option_d': "Change tools every hour.",
            'correct_option': 'B',
        },
        {
            'question_text': "What is a common sign of healthy architecture when using {skill}?",
            'option_a': "Clear separation of concerns.",
            'option_b': "Every module depends on every other module.",
            'option_c': "No one can explain the structure.",
            'option_d': "Business logic is duplicated everywhere.",
            'correct_option': 'A',
        },
        {
            'question_text': "How should developers handle risky changes involving {skill}?",
            'option_a': "Ship them silently.",
            'option_b': "Document assumptions and test carefully.",
            'option_c': "Remove monitoring first.",
            'option_d': "Skip backups and rollback plans.",
            'correct_option': 'B',
        },
        {
            'question_text': "What is the main purpose of code review for {skill}-related work?",
            'option_a': "To improve quality and share context.",
            'option_b': "To delay projects without reason.",
            'option_c': "To replace testing entirely.",
            'option_d': "To avoid collaboration.",
            'correct_option': 'A',
        },
        {
            'question_text': "If a {skill} feature fails in testing, what is the best response?",
            'option_a': "Hide the failure and merge anyway.",
            'option_b': "Investigate the root cause and fix it.",
            'option_c': "Delete the test permanently.",
            'option_d': "Blame the framework immediately.",
            'correct_option': 'B',
        },
        {
            'question_text': "What is the value of documentation around {skill} implementations?",
            'option_a': "It helps onboarding and future maintenance.",
            'option_b': "It makes the code stop running.",
            'option_c': "It only matters for marketing teams.",
            'option_d': "It should replace source code.",
            'correct_option': 'A',
        },
        {
            'question_text': "What is a strong security mindset while working with {skill}?",
            'option_a': "Trust all inputs by default.",
            'option_b': "Validate inputs and follow secure defaults.",
            'option_c': "Expose secrets in repositories for convenience.",
            'option_d': "Disable authentication during release.",
            'correct_option': 'B',
        },
        {
            'question_text': "Which outcome shows that a {skill} solution is production-ready?",
            'option_a': "It works only on one developer laptop.",
            'option_b': "It passes validation, testing, and deployment checks.",
            'option_c': "It has the longest file length.",
            'option_d': "It avoids all feedback from teammates.",
            'correct_option': 'B',
        },
        {
            'question_text': "Which attitude helps someone become truly strong in {skill}?",
            'option_a': "Curiosity, iteration, and disciplined practice.",
            'option_b': "Refusing feedback.",
            'option_c': "Avoiding debugging.",
            'option_d': "Ignoring project goals.",
            'correct_option': 'A',
        },
    ],
    [
        {
            'question_text': "What is the best reason to use standards and conventions with {skill}?",
            'option_a': "They make teamwork more predictable.",
            'option_b': "They prevent all future redesigns.",
            'option_c': "They remove the need for requirements.",
            'option_d': "They only matter in classroom exercises.",
            'correct_option': 'A',
        },
        {
            'question_text': "When scaling a {skill}-based solution, what matters most first?",
            'option_a': "Guessing at problems.",
            'option_b': "Understanding usage patterns and bottlenecks.",
            'option_c': "Adding random infrastructure.",
            'option_d': "Ignoring monitoring data.",
            'correct_option': 'B',
        },
        {
            'question_text': "Why is incremental delivery valuable in {sector} work using {skill}?",
            'option_a': "It reduces risk and supports faster feedback.",
            'option_b': "It guarantees no rewrites are ever needed.",
            'option_c': "It removes the need for design.",
            'option_d': "It only works for toy projects.",
            'correct_option': 'A',
        },
        {
            'question_text': "What should a developer do before adopting a new pattern in {skill}?",
            'option_a': "Apply it everywhere immediately.",
            'option_b': "Evaluate whether it fits the problem.",
            'option_c': "Use it only because it is popular.",
            'option_d': "Skip team discussion.",
            'correct_option': 'B',
        },
        {
            'question_text': "What is a useful indicator of quality in {skill}-based development?",
            'option_a': "Readable code with reliable behavior.",
            'option_b': "The highest number of files changed.",
            'option_c': "The most complex syntax possible.",
            'option_d': "The absence of comments, tests, or structure.",
            'correct_option': 'A',
        },
        {
            'question_text': "When requirements change for a {skill} feature, what is the best approach?",
            'option_a': "Ignore the new requirement.",
            'option_b': "Reassess the implementation and adapt safely.",
            'option_c': "Keep old assumptions hidden.",
            'option_d': "Refuse to update tests.",
            'correct_option': 'B',
        },
        {
            'question_text': "Why do teams monitor systems built with {skill} after release?",
            'option_a': "To detect issues and improve reliability.",
            'option_b': "Because monitoring replaces maintenance.",
            'option_c': "To avoid debugging forever.",
            'option_d': "Because local testing is impossible.",
            'correct_option': 'A',
        },
        {
            'question_text': "How should reusable logic be handled in a healthy {skill} codebase?",
            'option_a': "Duplicate it in as many places as possible.",
            'option_b': "Abstract it carefully when repetition appears.",
            'option_c': "Hide it in unrelated modules.",
            'option_d': "Rewrite it differently every time.",
            'correct_option': 'B',
        },
        {
            'question_text': "What is the best way to gain confidence in a {skill} release?",
            'option_a': "Use validation, review, and staged rollout habits.",
            'option_b': "Deploy first and inspect later.",
            'option_c': "Depend only on luck.",
            'option_d': "Skip team communication.",
            'correct_option': 'A',
        },
        {
            'question_text': "What separates a beginner from a strong practitioner of {skill}?",
            'option_a': "Consistent problem-solving and sound judgment.",
            'option_b': "Memorizing one tutorial forever.",
            'option_c': "Avoiding collaboration.",
            'option_d': "Never revisiting fundamentals.",
            'correct_option': 'A',
        },
    ],
]


class Command(BaseCommand):
    help = "Create or refresh 3 linked assessment question sets for every skill."

    def handle(self, *args, **options):
        created_or_updated = 0
        skills = Skill.objects.all().order_by('category', 'skill_name')

        for skill in skills:
            sector_label = skill.get_category_display()
            for set_index, question_set in enumerate(QUESTION_SETS, start=1):
                for order, template in enumerate(question_set, start=1):
                    defaults = {
                        'sector': skill.category,
                        'question_text': template['question_text'].format(skill=skill.skill_name, sector=sector_label),
                        'option_a': template['option_a'].format(skill=skill.skill_name, sector=sector_label),
                        'option_b': template['option_b'].format(skill=skill.skill_name, sector=sector_label),
                        'option_c': template['option_c'].format(skill=skill.skill_name, sector=sector_label),
                        'option_d': template['option_d'].format(skill=skill.skill_name, sector=sector_label),
                        'correct_option': template['correct_option'],
                        'is_active': True,
                    }
                    Question.objects.update_or_create(
                        skill=skill,
                        set_number=set_index,
                        question_order=order,
                        defaults=defaults,
                    )
                    created_or_updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Seeded {created_or_updated} question records across {skills.count()} skills.'
            )
        )
