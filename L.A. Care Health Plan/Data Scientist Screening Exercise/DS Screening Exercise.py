#Before you run this code, you have to use pip3 to install matplotlib and sklearn firstly

#Question1: Manually calculate the sensitivity and specificity of the model, 
#using a predicted_prob threshold of greater than or equal to .5.
import csv
filename = open('model_outcome.csv')
reader = csv.reader(filename)
outcome = [row for row in reader]
outcome1 = outcome[1:]
outcome_class = []
for a in outcome1:
    outcome_class.append(int(a[1]))
predicted_prob = []
for a in outcome1:
    predicted_prob.append(float(a[2]))
#We set threshold = 0.5
predicted_class = []
for a in predicted_prob:
    if a >= 0.5:
        predicted_class.append(1)
    else:
        predicted_class.append(0)
true_positive = 0
condition_positive = 0
for i in range(len(outcome_class)):
    if outcome_class[i] == 1:
        condition_positive += 1
    if outcome_class[i] == 1 and predicted_class[i] == 1:
        true_positive += 1
Sensitivity = true_positive / condition_positive
print('Sensitivity:' , Sensitivity)
true_negative = 0
condition_negative = 0
for i in range(len(outcome_class)):
    if outcome_class[i] == 0:
        condition_negative += 1
    if outcome_class[i] == 0 and predicted_class[i] == 0:
        true_negative += 1
specificity = true_negative / condition_negative
print('specificity:', specificity)

#Question2: Manually calculate the Area Under the Receiver Operating Characteristic Curve.
AUC_denominator = condition_positive*condition_negative
condition_positive_data = []
condition_negative_data = []
for i in range(len(predicted_prob)):
    if outcome_class[i] == 0:
        condition_negative_data.append(predicted_prob[i])
    else:
        condition_positive_data.append(predicted_prob[i])
count = 0
for a in condition_positive_data:
    for b in condition_negative_data:
        if a > b:
            count += 1
        elif a < b:
            count += 0
        else:
            count += 0.5
AUC = count/AUC_denominator
print('AUC:', AUC)

#Question3: Visualize the Receiver Operating Characterstic Curve.
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
fpr, tpr, threshold = roc_curve(outcome_class, predicted_prob)
roc_auc = auc(fpr, tpr)
plt.figure(figsize=(10,10))
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.3f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characterstic Curve')
plt.legend(loc="lower right")
plt.show()