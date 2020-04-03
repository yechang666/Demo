# dict = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}

aa = ("name", "date", "age", "sex")
ss = ["Tom", "2019-10-11", 30, "男"]
dict1 = dict.fromkeys(aa,ss)
print(dict(zip(aa,ss)))

a = (1,1,2,3,3,4,5,6,6)
b = (2,2,3,4,4,5,6,7,8,8)
print(set(a) | set(b))

