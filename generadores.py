def my_gen():
    a = 1
    yield a

    a = 2
    yield a

    a = 3
    yield a


my_first_gen = my_gen()

print(next(my_first_gen))
print(next(my_first_gen))
print(next(my_first_gen))
print("*" * 50)


# desafio, generar los 200 primeros numeros pares, guardando el estado anterior
def my_gen():
    for i in range(1, 201):
        if i % 2 == 0:
            yield i

my_first_gen = my_gen()

for i in range(100):
    print(next(my_first_gen))