with open("results.txt") as file:
    i = 0
    contents = file.read().split("\n")
    print(len(contents))