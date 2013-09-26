import time,math
try: import numpy
except ImportError: print("Numpy is not installed on your system. Please install it and try again.")

# This number is the start depth to look through for primes to compare against very large numbers.
startprimes=100000 # Default 100000 - this means roughly searching through 10k

### Edit at your own risk
i=1
plist=[1.]
query=input("Please enter the source number.\n")
query=float(query)
input=query
#check size, if it's a number
starttime=time.time()
while query%2==0: 
    plist.append(2.)
    query=query/2.
# Remaining number is odd.
qbak=query
prange=math.floor(query/2) # This only fails if the number is 2^n*query, check it later
#if query==input: prange=math.floor(query/2) ## swapped
#else: prange=query-1 ##swapped
deep=False
try:primef=numpy.arange(prange+1)
except MemoryError:
    # This number is frakking huge. Compare against first 10k primes.
    print("This number is very large. Attempting to reduce the first few primes before calculating the rest.")
    #### Should this be a function?? ####
    primef=numpy.arange(startprimes)
    i=0
    primef_o=primef/2.%1
    indices=primef_o.nonzero()
    primef=primef[indices]
    primef=primef[1:]
    primef=primef/1.
    while i < len(primef):
        divisor=primef[i]
        primef[i]+=.1
        t=primef%divisor
        indices=t.nonzero()
        primef=primef[indices]
        primef[i]-=.1
        i+=1
        if i%1000==0: print("Calculating "+str(i)+"th prime...")
    first=query%primef
    indices=numpy.where(first==0)[0]
    ffactors=primef[indices]
    # Dump this to a file for checking later?
    #### End potential function ####
    print("Found "+str(len(ffactors))+" factors in "+str(input)+" to reduce by: "+str(ffactors))
    if len(ffactors)>0:
        query=query/ffactors.prod()
        for x in ffactors: plist.append(x)
        qbak=query
        prange=math.floor(query/2)
        try:
            print("Trying the new search space ...")
            primef=numpy.arange(startprimes,prange+1) # we've already eliminated the bottom primes
            print("Success. Searching for primes in range of "+str(prange))
            deep=True
        except MemoryError: 
            print("The new working number ("+str(query)+" is too large for the memory of this computer or the bit depth of this Python and Numpy version.")
            print("You can manually edit this function and increase the size of the variable 'startprimes'")
            exit()
    else:
        print(str(input)+" is too large for the memory of this computer or the bit depth of this Python and Numpy version, and does not have a factor smaller than "+str(startprimes))
        print("You can manually edit this function and increase the size of the variable 'startprimes'")
        exit()
# Now, primef contains all remaining possible divisors for query
# Odd only
primef_o=primef/2.%1
indices=primef_o.nonzero()
primef=primef[indices]
primef=primef[1:]
i=0
j=0
primef=primef/1. #to float
breaktrue=False
# Quick prime check
mods=query%primef
indices=numpy.where(mods==0)[0]
primef=primef[indices]
primef=numpy.append(primef,qbak)
print("Starting search ...")
while i < len(primef):
    divisor=primef[i]
    primef[i]+=.1
    t=primef%divisor
    indices=t.nonzero()
    primef=primef[indices]
    primef[i]-=.1
    i+=1
    if i%50==0: 
        j+=1
        inum=i*j
        if not deep: counter=250
        else: counter=50
        if inum%counter==0: print("Working ... "+str(inum)+" iterations... (currently checking "+str(primef[i])+")")
        #clean it up
        pslice=primef[:i]
        primer=input%pslice
        indices=numpy.where(primer==0)[0]
        pslice=pslice[indices]
        for x in pslice: plist.append(x)
        npa=numpy.array(plist)
        if npa.prod()==input: 
            breaktrue=True
            break
        else:
            # Make sure degenerecies don't already solve it
            rem=input/npa.prod()
            npa2=npa[1:]
            pv=rem%npa2
            dd=numpy.where(pv==0)[0]
            degen=npa2[dd]
            if len(degen)>0:
                for x in degen:
                    while int(rem/x)==rem/x:
                        plist.append(x)
                        rem=rem/x
                plist=sorted(plist)
                npa=numpy.array(plist)
                if npa.prod()==input: 
                    breaktrue=True
                    break
                else:
                    # Reduce the search space -- 
                    # do math on fewer elements
                    rem=input/npa.prod()
                    primef=numpy.arange(npa.max(),rem+1)
                    primef_o=primef/2.%1
                    indices=primef_o.nonzero()
                    primef=primef[indices]
                    i=0
        primef=primef[i:]
        i=0
        if inum%250==0: print("Have "+str(plist))

# Primef is now all the primes up to the reduced argument
if not breaktrue:
    primer=input%primef
    indices=numpy.where(primer==0)[0]
    primef=primef[indices]
    for x in primef: plist.append(x)
    # Expand!
    npa=numpy.array(plist)
    if npa.prod() is not input:
        rem=input/npa.prod()
        npa2=npa[1:]
        pv=rem%npa2
        dd=numpy.where(pv==0)[0]
        degen=npa2[dd]
        #print("Degenerate values:"+str(degen))
        for x in degen:
            while int(rem/x)==rem/x:
                plist.append(x)
                rem=rem/x
        plist=sorted(plist)
        # Rem is now a product of X_n^Y, where X is in plist
npa=numpy.array(plist)
nmax=npa.max()
if nmax < 3 and nmax is not qbak: plist.append(qbak)
elapsed=time.time()-starttime
if len(plist)>1: print("The prime factorization for "+str(input)+" is "+str(plist))
else: print(str(input)+" is a prime number.")
print("Total elapsed time: "+str(elapsed)+" seconds")
