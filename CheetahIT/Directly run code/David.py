#I think this is a very easy classification problem, the label is Risk
#So we can understand it as to predict whether a company is risk or not
from sklearn import tree
import csv
import scipy
from scipy.stats import pearsonr
filename = open('audit_risk.csv')
reader = csv.reader(filename)
audit_risk = [row for row in reader]
name = audit_risk[0]
data = audit_risk[1:]
label = [int(a[len(data[0])-1]) for a in data]
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
cnt = 0
for a in data:
	for b in a[:len(name)-1]:
		if is_number(b) == False:
			cnt += 1
#print(cnt)
#I find that the count of not number is only 4, so I use 0 to replace this 
data_only = []
for a in data:
	data_only_element = []
	for b in a[:len(data[0])-1]:
		if is_number(b) == False:
			b =0
		data_only_element.append(float(b))
	data_only.append(data_only_element)
#Check the threshold to distinguish whether a company is risk based on Audit_Risk
Audit_Risk = [a[-1] for a in data_only]
threshold = 1.7148
for i in range(len(Audit_Risk)):
    if label[i] == 1:
        temp = Audit_Risk[i]
        if temp < threshold:
            threshold = temp
#print(threshold)
outlier = 0.5108
for i in range(len(Audit_Risk)):
    if label[i] == 0:
        temp = Audit_Risk[i]
        if temp > threshold:
            outlier = temp
#print(outlier)
#Calculate the correlation coeffience of each variarible 
#to see which variable has more weight
correlation_list = []
y = scipy.array(Audit_Risk)
for i in range(2, len(name)-3):
    Inherent_Risk = [a[i] for a in data_only]
    x = scipy.array(Inherent_Risk)
    correlation, p_value = pearsonr(x, y)
    correlation_list.append({name[i]:correlation})
#print(correlation_list)
#Use Decision Tree model to classify and predict whether a company is risk
dtc = tree.DecisionTreeClassifier(criterion="entropy")
clf = dtc.fit(data_only[:676], label[:676])
result = clf.predict(data_only[676:])
correct = 0
for i in range(len(result)):
    if result[i] == label[676:][i]:
        correct += 1
print('Accuracy: {:.2%}'.format(correct/100))
