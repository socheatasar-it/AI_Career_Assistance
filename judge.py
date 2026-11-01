from evaluation_utils import basic_answer_checks

def judge_answer(answer):
    checks = basic_answer_checks(answer)
    checks["passes_basic_checks"] = checks["non_empty"] and checks["length_chars"] >= 20
    return checks

if __name__ == "__main__":
    print(judge_answer("Start by listing your skills and exploring related job roles."))
