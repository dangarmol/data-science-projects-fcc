import numpy as np

def calculate(list):
    if len(list) != 9:
        raise ValueError("List must contain nine numbers.")

    result = dict()
    
    matrix = np.array(list).reshape(3,3)
    
    result["mean"] = [matrix.mean(0).tolist(), matrix.mean(1).tolist(), matrix.mean()]
    result["variance"] = [matrix.var(0).tolist(), matrix.var(1).tolist(), matrix.var()]
    result["standard deviation"] = [matrix.std(0).tolist(), matrix.std(1).tolist(), matrix.std()]
    result["max"] = [matrix.max(0).tolist(), matrix.max(1).tolist(), matrix.max()]
    result["min"] = [matrix.min(0).tolist(), matrix.min(1).tolist(), matrix.min()]
    result["sum"] = [matrix.sum(0).tolist(), matrix.sum(1).tolist(), matrix.sum()]
    
    return result