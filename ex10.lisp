# ex10.py
# Simple expert system rule in Python

temperature = int(input("Enter temperature: "))

if temperature > 30:
    print("Rule Fired: Weather is Hot")
elif temperature < 20:
    print("Rule Fired: Weather is Cold")
else:
    print("Rule Fired: Weather is Normal")
