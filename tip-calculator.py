#If the bill was $150.00, split between 5 people, with 12% tip. 

#Each person should pay (150.00 / 5) * 1.12 = 33.6
#Format the result to 2 decimal places = 33.60

#Tip: There are 2 ways to round a number. You might have to do some Googling to solve this.💪

#Write your code below this line 👇

print("Welcome to the tip calculator.")
a = float(input("What was the total bill? $"))
b = int(input("What percentage tip would you like to give? 10, 12, or 15? "))
c = int(input("How many people to split the bill? "))
d = round((a/c)*(1+b/100),2)
e = "{:.2f}".format(d)
print(f"Each person should pay: ${e}")

#d = b/100
#e = a*d
#f = a + e
#g = f/c
#h = round(g, 2)