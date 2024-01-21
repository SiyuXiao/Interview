# I believe this strength check rule is closer to the real world:
# I design 2 processes: plus score and minus score
# the plus score shows the strength of the password
# the minus score shows the weakness of the password
# the least condition to get a positive score is to meet condition 1 and at least 3 conditions from condition 2 to 5:
# Conditions:
# 1. the length of the password cannot be less than 8 digits
# 2. the password includes upper letters
# 3. the password includes lower letters
# 4. the password includes numbers
# 5. the password includes symbols
def check_password_strength(x):
    item = 0
    score = 0

    #plus score
    score += len(x)*4#plus 4 times scores of the length of the password
    upper = 0
    for a in x:
        if a.isupper() == True:
            upper += 1
    score += (len(x) - upper)*2#plus about uppercase
    if upper != 0:
        item += 1
    lower = 0
    for a in x:
        if a.islower() == True:
            lower += 1
    score += (len(x) - lower)*2#plus about lowercase
    if lower != 0:
        item += 1
    num = 0
    for a in x:
        if a.isnumeric() == True:
            num += 1
    score += num*4# plus about number
    if num != 0:
        item += 1
    cha = 0
    for a in x:
        if a.isalnum() == False:
            cha += 1
    score += cha*6# plus about symbols
    if cha != 0:
        item += 1
    no_side = 0
    for i in range(1, len(x)-1):
        if ord(x[i]) not in range(65, 91) and ord(x[i]) not in range(97, 123):
            no_side += 1
    score += no_side*2# plus about number and symbol not on both sides
    if item >= 3 or len(x) >= 8:
        score += (item+1)*2 # plus if the password satisfies the least condition
    else:
        return 0# if the password does not satisfy the least condition, return 0

    #minus score
    if x.isalpha():
        score -= len(x)# minus if the password only has letters
    if x.isnumeric():
        score -= len(x)# minus if the password only has numbers
    dup = {}
    for a in x:
        if a not in dup:
            dup[a] = 1
        else:
            dup[a] += 1
    for a in dup.values():
        if a > 1:
            score -= a*(a-1)# minus about duplicate characters
    con_upper = 0
    for i in range(len(x)-1):
        if x[i].isupper() == True and x[i+1].isupper() == True:
            con_upper += 1
    score -= con_upper*2# minus about continuous uppercases
    con_lower = 0
    for i in range(len(x)-1):
        if x[i].islower() == True and x[i+1].islower() == True:
            con_lower += 1
    score -= con_lower*2# minus about continuous lowercases
    con_num = 0
    for i in range(len(x)-1):
        if x[i].isnumeric() == True and x[i+1].isnumeric() == True:
            con_num += 1
    score -= con_num*2# minus about continuous number, like the easiest password to guess: 123456
    con_order3 = 0
    for i in range(len(x)-2):
        if ord(x[i]) + 1 == ord(x[i+1]) and ord(x[i+1]) + 1== ord(x[i+2]):
            con_order3 += 1
    score -= con_order3*3# minus if continues letters or numbers like: abcd or 1234
    if score > 0:
        return score 
    else:
        return 0 # the least score of a password is 0
print(check_password_strength('111aaaFF'))# Input any password string you want here like '111aaaFF'

