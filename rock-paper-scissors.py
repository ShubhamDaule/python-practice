rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

#Write your code below this line 👇

import random

list = [rock, paper, scissors]
a = input("What do you choose? type 0 for Rock, 1 for Paper 2 for Scissors: ")
b = int(a)

if b >= 3 or b < 0:
    print("Wrong Choice, try again")
else:
    print("You chose:" + list[b])
    c = random.randint(0, 2)
    print("Computer chose:" + list[c])
    if b == c:
        print("It's a tie")
    elif b == 0 and c == 2:
        print("you win!")
    elif b == 2 and c == 0:
        print("you lose!")
    elif b > c:
        print("you win!")
    else:
        print("You lose!")
