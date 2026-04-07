def compute_reward(task, action, gt):
    if task == "easy":
        return 1.0 if action == gt else 0.0

    if task == "medium":
        return 0.7 if action == gt else 0.3

    if task == "hard":
        if gt.lower() in action.lower():
            return 1.0
        return 0.2

    return 0.0