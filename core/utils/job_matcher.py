from typing import List, Dict

# Edu ranking
edu_rank =[
    "school" :1,
    "diploma" :2,
    "bachelor" :3,
    "master": 4,
    "phd": 5,
    "unknown": 0
]
def calculate_skill_score(required_skills:List[str], resume_skills:List[str]):
    """ Percentage of required skills found in resume """
    if not required_skills:
        return 100.0
    matched_skills = [s for s in required_skills if s.lower() in [r.lower() for r in resume_skills]]
    return round((len(matched_skills)/len(required_skills))*100,2)

def calculate_experience_score(required_exp:float, resume_exp:float):
    """ Percentage of required experience found in resume """

    if not required_exp:
        return 100.0
    ratio_exp = resume_exp/required_exp
    return round(ratio_exp *100 ,2)

def calculate_education_score(required_edu:str, resume_edu:str):
    """ Percantage of required education"""

    req_rank = edu_rank.get(required_edu.lower(),0)
    res_rank = edu_rank.get(resume_edu.lower(), 0)

    if req_rank ==0:
        return 100.0
    edu_ratio = res_rank/req_rank
    return round(edu_ratio * 100 ,2)

def calculate_overall_score(required_skills:List[str], resume_skills:List[str],
                            required_exp:float , resume_exp:float,
                            required_edu:str, resume_edu:str):
    """ calculate score on all 3 parameters(60 +20 +10) and then combine them """

    skill_score = calculate_skill_score(required_skills,resume_skills)
    exp_score = calculate_experience_score(required_exp, resume_exp)
    edu_score = calculate_education_score(required_edu,resume_edu)

    total_score = round(skill_score *0.6 + exp_score *0.2 + edu_rank * 0.1, 2)

    return {
        "skill_score":skill_score,
        "exp_score": exp_score,
        "edu_score": edu_score,
        "overall_score": total_score
    }
