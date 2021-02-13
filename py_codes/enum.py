cars = ['kia', 'audi', 'bmw']
for car in enumerate(cars):
  print(car)



cars = ['kia', 'audi', 'bmw']
print(list(enumerate(cars, start = 1)))



cars = ['kia', 'audi', 'bmw']
listOfCars = []
n = 0
for car in cars:
    listOfCars.append((n, car))
    n += 1
print(listOfCars)