import random

for i in range(1,1000000):
    x=str(random.randint(1,10))
    with open("random_number.txt","a") as f:
        f.write(f"{x}\n")