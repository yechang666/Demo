def selectionSort(arr):
    for i in range(len(arr)-1):
        # 记录最小数的索引
        minIndex = i
        for j in range(i + 1,len(arr)):
            if arr[j] < arr[minIndex]:
                minIndex = j
        if i != minIndex:
            arr[i],arr[minIndex] = arr[minIndex],arr[i]
    return arr

print(selectionSort([2,1,8,5,3]))