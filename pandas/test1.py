import pandas as pd
import numpy as np

# arr1 = np.arange(10)
# print(arr1.flags)
# print(arr1)
# print(type(arr1))
#
# s1 = pd.Series(arr1)
# print(s1)
# print(type(s1))
#
# dict1 = {'a':10, 'b': 20, 'c': 30, 'd': 40 ,'e': 50}
# print(dict1)
# print(type(dict1))
#
# s2 = pd.Series(dict1)
# print(s2)
# print(type(s2))
#
# ss = pd.Series(['A', 'B', 'C', np.nan, 'cc', 'dd'])
# print(ss.str.lower())


df = pd.DataFrame({"id":[1001,1002,1003,1004,1005,1006],
 "date":pd.date_range('20130102', periods=6),
  "city":['Beijing ', 'SH', ' guangzhou ', 'Shenzhen', 'shanghai', 'BEIJING '],
 "age":[23,44,54,32,34,32],
 "category":['100-A','100-B','110-A','110-C','210-A','130-F'],
  "price":[1200,np.nan,2133,5433,np.nan,4432]},
  columns =['id','date','city','category','age','price'])

print()
