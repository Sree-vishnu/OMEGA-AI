from time import gmtime, strftime, sleep



ti = strftime("%M:%S", gmtime())
ti = ti.split(':')
tim = (int(ti[0])*60)+int(ti[1])
print(tim)


while True:
   ti_c = strftime("%M:%S", gmtime())
   ti_c = ti_c.split(':')
   tim_c = (int(ti_c[0])*60)+int(ti_c[1])
   print(tim_c)
   
   if tim_c>(tim+10):
      print("...")
   sleep(5)


