def insertionSort(arr):
    # for i in range(len(arr)):
    #     preIndex = i - 1
    #     current = arr[i]
    #     while preIndex >= 0 and arr[preIndex] > current:
    #         arr[preIndex + 1] = arr[preIndex]
    #         preIndex -= 1
    #         arr[preIndex + 1] = current
    # return arr
    dd = []
    dd.insert(0,arr[0])
    for i in range(1,len(arr)):
        if arr[i] <= dd[0]:
            dd.insert(0, arr[i])
        elif arr[i] >= dd[-1]:
            dd.insert(len(dd)+1,arr[i])
        else:
            for j in range(len(dd),0,-1):
                if arr[i] <= dd[j-1] and arr[i]>dd[j-2]:
                    dd.insert(j-1,arr[i])
    return dd


print(insertionSort([10,9,8,7,6,5,4,3,2,1]))




