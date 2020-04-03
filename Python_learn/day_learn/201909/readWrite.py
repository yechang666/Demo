class readWrite():
    def __init__(self):
        self.name = "Tom"
        self.sex = "男"
        self.age = 21
    def read(self):
        fo = open("../res/data.json",mode="r")
        print(type(fo))
        print()
        # print(dir(fo))
        print("文件名字=",fo.name)
        print("是否关闭：",fo.closed)
        print("访问模式：",fo.mode)


readWrite().read()