# tg = 6*["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
tg = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
dz =5*["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
# tgdz = []
# for i in range(60):
#     tgdz.append(tg[i] + dz[i])
# var = 0
# for m in tgdz:
#     print(m ,end="\t")
#     var+=1
#     if(var==10):
#         print()

tgdz1 = []
for i in range(60):
    num = i % len(tg)
    tgdz1.append(tg[num] + dz[i])

var = 0
# for r in range(31,36):
rr = [i for i in range(31,38)]
i = 0
for m in tgdz1:
    print("\033[1;%s;47m %s \033[0m" %(rr[i],m) ,end="\t")
    var+=1
    if(var==10):
        print()
        i +=1
        var = 0




