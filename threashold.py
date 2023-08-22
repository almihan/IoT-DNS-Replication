import numpy as np
from sklearn.metrics import roc_curve

# dummy example scores and labels
positive_scores = [0.95, 0.92, 0.94, 0.91] # similarity scores for true IoT devices
negative_scores = [0.20, 0.15, 0.25] # similarity scores for non-IoT devices
scores = positive_scores + negative_scores
labels = [1] * len(positive_scores) + [0] * len(negative_scores) # 1 for IoT, 0 for non-IoT

# Generate ROC curve
fpr, tpr, thresholds = roc_curve(labels, scores)

# Finding the threshold that maximizes TPR while ensuring FPR <= 0.01
mask = fpr <= 0.01
optimal_idx = np.argmax(tpr[mask])
optimal_threshold = thresholds[mask][optimal_idx]

print(optimal_threshold)
