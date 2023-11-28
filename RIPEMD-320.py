# RIPEMD-320

import chilkat2
import random
import string
import numpy
from scipy import stats
import matplotlib.pyplot as plt

crypt = chilkat2.Crypt2()

content = "KobetsDenisSergiyovich"
crypt.HashAlgorithm = "ripemd320"
crypt.EncodingMode = "hex"

def hashMessage(content):
    return crypt.HashStringENC(content)

def getUniqueValue():
    return content + str(random.randint(10**5, 10**6))

def searchPrototype1():
    original = getUniqueValue()
    originalHash = hashMessage(original)
    # print(originalHash)
    i = 1
    while 1:
        newMessage = f"{original}{i}"
        newHash = hashMessage(newMessage)
        # if i < 30:
        #     print(newMessage)
        #     print(newHash)
        if newHash[-4:] == originalHash[-4:]:
            return [i, original, originalHash, newMessage, newHash]
        i = i + 1

def modifyRandomCharacter(input):
    # Випадковий індекс для вибору символу
    index_to_modify = random.randint(0, len(input) - 1)

    # Випадковий символ з ASCII таблиці (букви, цифри, спеціальні символи)
    new_character = random.choice(string.ascii_letters + string.digits + string.punctuation)

    # Змінюємо символ у вибраному індексі
    modifiedString = input[:index_to_modify] + new_character + input[index_to_modify + 1:]

    return modifiedString

def searchPrototype2():
    original = getUniqueValue()
    originalHash = hashMessage(original)
    newMessage = original
    i = 1
    while 1:
        newMessage = modifyRandomCharacter(newMessage)
        newHash = hashMessage(newMessage)
        # if i < 30:
        #     print(newMessage)
        #     print(newHash)
        if newHash[-4:] == originalHash[-4:]:
            return [i, original, originalHash, newMessage, newHash]
        i = i + 1

def birthday1():
    original = getUniqueValue()
    originalHash = hashMessage(original)
    shortKeysMessages = {originalHash[-8:]: original}
    i = 1
    # print("original = " + original)
    # print(originalHash)

    while 1:
        newMessage = f"{original}{i}"
        newHash = hashMessage(newMessage)
        # if i < 30:
        #     print(newMessage)
        #     print(newHash)
        if newHash[-8:] in shortKeysMessages:
            return [shortKeysMessages[newHash[-8:]], newMessage, hashMessage(shortKeysMessages[newHash[-8:]]), newHash, i]
        shortKeysMessages[newHash[-8:]] = newMessage
        i = i + 1

def birthday2():
    message = getUniqueValue()
    messageHash = hashMessage(message)
    shortKeysMessages = {messageHash[-8:]: message}
    i = 1
    # print('original = ' + message)
    # print(messageHash)
    while 1:
        message = modifyRandomCharacter(message)
        messageHash = hashMessage(message)
        # if i < 30:
        #     print(message)
        #     print(messageHash)
        if messageHash[-8:] in shortKeysMessages:
            if message == shortKeysMessages[messageHash[-8:]]:
                continue
        if messageHash[-8:] in shortKeysMessages:
            # print('number = ' + str(list(shortKeysMessages.keys()).index(messageHash[-8:])))
            return [shortKeysMessages[messageHash[-8:]], message, hashMessage(shortKeysMessages[messageHash[-8:]]), messageHash, i]
        shortKeysMessages[messageHash[-8:]] = message
        i = i + 1


# result1 = searchPrototype1()
# print(f"за {result1[0]} ітерацій")
# print("Прообрази 1:")
# print(result1[1])
# print(result1[3])
# print("Значення гешів:")
# print(result1[2])
# print(result1[4])
# print()
# print()

res = []
for i in range (101):
    res.append(birthday2()[4])

print('array' + str(res))
print(numpy.mean(res))
print(numpy.var(res))
print()

print('interval ' + str(stats.t.interval(0.95, len(res) - 1, loc=numpy.mean(res), scale=stats.sem(res))))
print('table')

for i in range(len(res)):
    print(str(res[i]))

plt.hist(res, bins='auto', alpha=0.7, rwidth=0.85)
plt.title('Гістограма')
plt.xlabel('Значення')
plt.ylabel('Частота')
plt.grid(axis='y', alpha=0.75)
plt.show()


# result2 = searchPrototype2()
# print(f"за {result2[0]} ітерацій")
# print("Прообрази 2:")
# print(result2[1])
# print(result2[3])
# print("Значення гешів:")
# print(result2[2])
# print(result2[4])
# print()
# print()
#
# result3 = birthday1()
# print(f"за {result3[4]} ітерацій")
# print("Дні народження варіант 1:")
# print(result3[2])
# print(result3[3])
# print("Повідомлення, які дали колізію, варіант 1:")
# print(result3[0])
# print(result3[1])
# print()
# print()
#
# result4 = birthday2()
# print(f"За {result4[4]} ітерацій")
# print("Дні народження варіант 2:")
# print(result4[2])
# print(result4[3])
# print("Повідомлення, які дали колізію, варіант 2:")
# print(result4[0])
# print(result4[1])
# print()
# print()