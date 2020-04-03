a = 3
def change():
    global a
    a = 10
    return a

print(a, change(), a)

if __name__ == "__main__":
    print(a, change(), a)
