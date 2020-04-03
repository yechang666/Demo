# @Time     :2019/12/05 10:15
# @Author   :lzw
# @Email    :601923086@qq.com
# @File     :phone_num.py

def mobile_operator(phone_number):
    id3 = phone_number[0:3]
    id4 = phone_number[0:4]
    CMCC = [134, 135, 136, 137, 138, 139, 150, 151, 152, 157, 158, 159, 182, 183, 184, 187, 188, 147, 178, 1705]
    CUCC = [130, 131, 132, 155, 156, 185, 186, 145, 176, 1709]
    CTCC = [133, 153, 180, 181, 189, 177, 1700]
    if ((id3 in str(CMCC)) or (id4 in str(CMCC))):
        return "China CMCC"
    elif ((id3 in str(CUCC)) or (id4 in str(CUCC))):
        return "China CUCC"
    elif ((id3 in str(CTCC)) or (id4 in str(CTCC))):
        return "China CTCC"
    else:
        return 0


def verify_phone_number():
    phone_number = input("Enter your number :")
    print(end='\n')
    if not phone_number.isdigit():
        print("手机号码必须是数字,包含非法字符")
        verify_phone_number()
    elif len(phone_number) < 11:
        # print(invalid)
        print("Invalid length, your number should be in 11 digits")
        verify_phone_number()  # 函数递归调用

    else:
        operator = mobile_operator(phone_number)  # 返回的是字符串
        if operator:
            print("Operator : {}".format(operator))
            print("We're sending verification code via text to your phone: {}".format(phone_number))
        else:
            print("No such an operator")
            verify_phone_number()  # 函数递归调用


verify_phone_number()