import random



# for i in range(5):
#     print(i,  end=' ')
#
# print()
# for i in range(2, 5):
#     print(i, end=' ')
#
# print()
# for i in range(4, 10, 2):

# start_range = int(input('Start :'))
# end_range = int(input('End :'))
# step_range = int(input('Step :'))
#
# for k in range(start_range, end_range, step_range):
#     print(k, end=', ')

# for j in range(1,10):
#     print()
#     for i in range(10):
#         print(f'{i}*{i}={j*i}', end='')

start_range = int(input('Start: '))
end_range= int(input('End: '))
for n in range(start_range , end_range + 1):
    is_prime = True

    for i in range(2, n):
        if n % i == 0:
           is_prime = False
    break

    if  is_prime:
        print('%d, ' % n, end=''








































