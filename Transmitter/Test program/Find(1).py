string = "My Name Is Josh"
substring = "name"
flag = False
for word in string.lower().split():
    if substring == word:
        flag = True
        print(f"Found:", {substring}, " in:", {string})
if (flag == False):
    print("No match found!")