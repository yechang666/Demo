import random
poker_num = [str(i) for i in range(2,11)]
poker_str = ['A','J','Q','K']
poker_king = ['大王','小王']
poker_color = ['红桃','黑桃','方块','梅花']
pokers = ['%s%s'%(i,j) for i in poker_color for j in poker_num+poker_str]+poker_king
# print(pokers)
random.shuffle(pokers)
person_a = pokers[::3]
person_b = pokers[1::3]
person_c = pokers[2::3]
landowner = pokers[-3:]
print(person_a)
print(person_b)
print(person_c)