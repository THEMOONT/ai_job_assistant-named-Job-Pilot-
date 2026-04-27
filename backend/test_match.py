from app.services.match_engine import calculate_match_score

semantic = 0.90
keyword = 0.80
experience = 1.00

score = calculate_match_score(
    semantic,
    keyword,
    experience
)

print("Match Score:", score)
