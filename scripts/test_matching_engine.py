from core.utils.job_matcher import calculate_overall_score

required_skills = ["Python","Django","SQL","AWS"]
resume_skills = ["SQL", "Django","HTML"]
required_exp = 5
resume_exp = 7
required_edu = "Bachelor"
resume_edu = "Master"

score = calculate_overall_score(required_skills,resume_skills,
                                required_exp,resume_exp,
                                required_edu,resume_edu)
print(score)