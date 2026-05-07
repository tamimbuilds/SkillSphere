from skills.models import JobSkillRequirement, CandidateSkill, CandidateSkillProgress, Score

def calculate_match_score(candidate_profile, job_post):
    """
    Calculates a match score out of 10.
    - 5 points for skill matching: (matched_skills / required_skills) * 5
    - 5 points for assessment performance: average of best scores for matched skills, scaled to 5
    
    Returns 0.0 if the job has no skill requirements defined yet.
    """
    required_skills = JobSkillRequirement.objects.filter(job=job_post).select_related('skill')
    total_required = required_skills.count()

    # If the recruiter hasn't set any required skills, score is 0 (not calculable)
    if total_required == 0:
        return 0.0

    candidate_skills = CandidateSkill.objects.filter(candidate=candidate_profile).select_related('skill')
    candidate_skill_map = {cs.skill_id: cs for cs in candidate_skills}

    matched_count = 0
    assessment_percentages = []

    total_penalty = 0.0

    for req in required_skills:
        cand_skill = candidate_skill_map.get(req.skill_id)
        if cand_skill:
            matched_count += 1
            progress = CandidateSkillProgress.objects.filter(
                candidate=candidate_profile,
                skill=cand_skill.skill,
            ).first()
            if progress and progress.penalty_points > 0:
                total_penalty += progress.penalty_points

            # Get best (highest) assessment score for this matched skill
            best_score = Score.objects.filter(
                user=candidate_profile.user,
                candidate_skill=cand_skill
            ).order_by('-score').values_list('score', flat=True).first()

            if best_score is not None:
                assessment_percentages.append(best_score)
            else:
                # Skill matched but no assessment taken — counts as 0% assessment
                assessment_percentages.append(0.0)

    # 5 points: proportion of required skills the candidate has
    skill_score = (matched_count / total_required) * 5.0

    # 5 points: average assessment % across ALL required skills (unmatched = 0)
    # We have scores only for matched; unmatched skills count as 0
    all_percentages = assessment_percentages + [0.0] * (total_required - matched_count)
    avg_percentage = sum(all_percentages) / total_required if total_required > 0 else 0.0
    assessment_score = (avg_percentage / 100.0) * 5.0

    total_score = skill_score + assessment_score - total_penalty
    return round(max(1.0, min(10.0, total_score)), 2)

def update_candidate_match_scores(candidate_profile):
    """
    Recalculates and updates match scores for all job applications of a candidate.
    """
    from jobs.models import Application
    applications = Application.objects.filter(candidate=candidate_profile)
    for app in applications:
        app.match_score = calculate_match_score(candidate_profile, app.job)
        app.save(update_fields=['match_score'])

