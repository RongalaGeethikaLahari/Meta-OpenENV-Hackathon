def grade_classification(pred, gt):
    return 1.0 if pred == gt else 0.0

def grade_priority(pred, gt):
    mapping = {"low":0.3, "important":0.6, "urgent":1.0}
    return 1.0 - abs(mapping.get(pred,0) - mapping.get(gt,0))

def grade_reply(pred, gt):
    return 1.0 if gt.lower() in pred.lower() else 0.5