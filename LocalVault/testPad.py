keypat = "this is it%"
pos = keypat.find("%")
print(pos)

keypat = keypat if keypat.find("%") != -1 else keypat + "%"
print(keypat)