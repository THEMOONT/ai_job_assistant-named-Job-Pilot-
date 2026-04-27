import math


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(y * y for y in b))

    if mag_a == 0 or mag_b == 0:
        return 0

    return dot / (mag_a * mag_b)


def keyword_score(resume_skills, job_text):
    count = 0

    for skill in resume_skills:
        if skill.lower() in job_text.lower():
            count += 1

    return count / len(resume_skills) if resume_skills else 0


def experience_score(user_exp, required_exp):
    if user_exp >= required_exp:
        return 1
    elif user_exp == required_exp - 1:
        return 0.7
    else:
        return 0.4


def calculate_match_score(
    semantic,
    keyword,
    experience
):
    final_score = (
        semantic * 0.50 +
        keyword * 0.30 +
        experience * 0.20
    ) * 100

    return round(final_score)
