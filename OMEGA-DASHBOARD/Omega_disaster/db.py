import time
def write(S):

   S= S + '.\n'
   f = open("dbase.txt","a") #opens file with name of "test.txt"
   f.write(S)
   f.close()

def read():
   w=open('dbase.txt', 'r')
   for line in w:  
       x= line
   return x
   w.close()
 
