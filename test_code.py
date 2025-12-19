def calculate_average(numbers):
    sum = 0
    for i in numbers:
        sum += i
    return sum / len(numbers)  # 可能会除以零

# 测试代码
print(calculate_average([]))
