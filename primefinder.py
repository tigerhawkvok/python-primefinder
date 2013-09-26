#Python 2.6 as numpy is not 3.0 yet. Watch print statements!
import time,numpy
def listPrimes(endval):
    primelist = numpy.array([2]) #will need to be a numpy list
    i=1
    j=3
    while (endval > j):
        # math!
        test=numpy.fmod(j,primelist)
        tl=len(test)
        test2=sum(test/test)
        if test2 == tl: 
            primelist=numpy.append(primelist,j)
            if (tl+1)%100 == 0: print("Working ... found ", tl+1, " primes so far ...")
        i+=1
        j=2*i+1
    return primelist

def main:
    endval = input("Please enter the maximum number you'd like to test.  \n")
    if endval > 1000:
        cconf = raw_input("This is a large number. Do you want the entire list printed? (Y/N)  \n")
        if cconf.lower() == "y": print("This option not yet enabled") #set_printoptions(threshold=nan) #throwing namererror?
    starttime=time.time()
    j=2*i+1
    primelist=listPrimes(endval)
    elapsed = time.time()-starttime
    print("The primes in the range (0,",endval,") are ",primelist)
    print("Total elapsed time to find ", len(primelist), "primes: ", elapsed, " seconds")

if __name__ == '__main__':
  main()
