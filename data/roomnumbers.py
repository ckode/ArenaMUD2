mapGrid = {}
height = 10
width = 10
depth = 10

for x in range(height):
    for y in range(width):
        for z in range(depth):
            roomid = "{0}{1}{2}".format(x, y, z)
            mapGrid[roomid] = None


print "ArenaMUD2 world has {0} foors labeled 0-{1}.".format(width, width-1)
while 1:
   z = raw_input("What floor would you like to see?: ")
   try:
      z = int(z)
      if z in range(depth):
         break
      else:
         print "Invalid selection or not in range. (0-{0})".format(width-1)
   except:
      print "Invalid selection or not in range. (0-{0})".format(width-1)

r = ""
d = "|---" * 10 + "|"
print
print
print "This is floor {0}.".format(z).center(40, " ")
for x in range(height):
     print d
     for y in range(width):
         r = r + "|{}{}{}".format(x, y, z)
         if y == (width - 1):
              r = r + "|"
     print r
     r = ""
print d