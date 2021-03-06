import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt


def CopySubMatrix(Matrix,SubMatrix,i,j,rows,columns):
	n=rows*rows
	k=columns*columns
	for x in range(0,rows):
		for y in range(0,columns):
			Matrix[((i + x) , (j + y))] = SubMatrix[(x , y)]




def GeneratorMatrix(k):
	n=int(k + (2 * np.sqrt(k)) + 1)
	rootn = int(np.sqrt(n))
	rootk = int(np.sqrt(k))
	Generator=np.zeros((int (n),int(k)))
	Matrix =np.zeros((int(rootn),int(rootk)))
	for i in range(0,rootk):
		Matrix [i,i]=1
		Matrix [(rootn-1) , i]=1
	for i in range(0,rootk):
		CopySubMatrix   (Generator, Matrix, i*rootn, i*rootk, rootn, rootk)
		CopySubMatrix (Generator, Matrix, n - rootn, i*rootk, rootn, rootk)  
	return Generator 



def Encoder(Message):
	K = len(Message)

	Generator = GeneratorMatrix(K)
	CodedMessage = (np.dot(Generator, Message))%2

	return CodedMessage


def bec(encodedM,probability):
    ErrorM=np.zeros((len(encodedM),), dtype=int)
    NoiseM=encodedM
    
    for i in range(0,len(ErrorM)):
        P=np.around(np.random.rand(1),decimals=3)
       
        if P[0]<probability:
            ErrorM[i]=1
    for i in range(0,len(encodedM)):
        if ErrorM[i]==1:
            NoiseM[i]=-1
    return NoiseM   

def bsc(encodedM,probability):
    ErrorM=np.zeros((len(encodedM),), dtype=int)
    NoiseM=encodedM
    P=np.around(np.random.rand(1),decimals=4)
    for i in range(0,len(encodedM)):
        P=np.around(np.random.rand(1),decimals=4)
        
        if P[0]<probability:
            ErrorM[i]=1
    for i in range(0,len(encodedM)):
        if ErrorM[i]==1:
            if NoiseM[i]==1:
                NoiseM[i]=0
            else:
                  NoiseM[i]=1
    return NoiseM         

def  ParityCheckMatrix(k) :
	sqrtk = int(np.sqrt(k))
	sqrtn = int(sqrtk + 1)
	n = int(k + 2 * sqrtk + 1)
	OfSet = 0

	ParityCheckMatrix = np.zeros((n - k, n))

	for i in range(0,sqrtk):
		for j in range(OfSet,sqrtk + OfSet + 1):
			ParityCheckMatrix[i][j] = 1

		OfSet = OfSet + sqrtk + 1

	for i in range(sqrtk,2 * sqrtk):
		for j in range(i - sqrtk,n,sqrtn): 
			ParityCheckMatrix[i][j] = 1

	for i in range(0,n):
		ParityCheckMatrix[n-k-1][i] = 1

	return ParityCheckMatrix


def decoder(RecievedM,ParityCheckMatrix):
    alpha=RecievedM
    n=len(RecievedM)
    syndrome=np.dot(ParityCheckMatrix,RecievedM)

    for z in range(50):
        tempalpha=alpha
        for i in range(0,n):
            beta=np.zeros(n)
            SyndromeCount=0
            for j in range(0,np.size(ParityCheckMatrix,0)):
                beta[0]=alpha[i]

                if ParityCheckMatrix[j][i]==1:
                    SyndromeCount=SyndromeCount+1
                    sum=0
                    for k in range(0,n):
                        if ParityCheckMatrix[j][k]==1 and k!=i:
                            sum+=alpha[k]                           
                    sum=sum%2                    
                    beta[SyndromeCount]=sum

            Bincount=np.zeros(2)  
            for  t in range(0,SyndromeCount+1):
                if beta[t]==0:
                    Bincount[0]+=1
                else:
                    Bincount[1]+=1

            if (Bincount[0]==Bincount[1]):
                if (beta[0]==1):
                    tempalpha[i]=0
                else:
                    tempalpha[i]=1

            elif Bincount[0]>Bincount[1]:
               tempalpha[i]=0

            elif Bincount[0]<Bincount[1]:
                tempalpha[i]=1

        alpha=tempalpha
        syndrome=(np.dot(ParityCheckMatrix,alpha))%2
        IsSyndromZero=np.count_nonzero(syndrome)
        
        if IsSyndromZero==0:
            break                        

    return alpha          


def decoder(RecievedM,ParityCheckMatrix):
    alpha=RecievedM
    n=len(RecievedM)
    rootn=np.sqrt(n)
    k=(rootn-1)*(rootn-1)

    syndrome=(np.dot(ParityCheckMatrix,alpha))%2
    IsSyndromZero=np.count_nonzero(syndrome)
        
    if IsSyndromZero==0:
        return alpha

    for z in range(500):
        tempalpha=alpha
        for i in range(0,n):
            beta=np.zeros(n)
            SyndromeCount=0

            #if (i==n-1):
               #beta[0]=alpha[i]
                #for j in range(0,n-1):
                    #if (j%rootn==0):
                        #beta[1]+=alpha[j]
                    #if (j>k*rootn):
                        #beta[2]+=alpha[j]
                #SyndromeCount+=2

            for j in range(0,np.size(ParityCheckMatrix,0)):
                beta[0]=alpha[i]

                if ParityCheckMatrix[j][i]==1:
                    SyndromeCount=SyndromeCount+1
                    sum=0
                    for k in range(0,n):
                        if ParityCheckMatrix[j][k]==1 and k!=i:
                            sum+=alpha[k]                                              
                    beta[SyndromeCount]=sum

            beta=beta%2
            Bincount=np.zeros(2)  
            for  t in range(0,SyndromeCount+1):
                if beta[t]==0:
                    Bincount[0]+=1
                else:
                    Bincount[1]+=1

            if Bincount[0]>Bincount[1]:
               tempalpha[i]=0

            else:
                tempalpha[i]=1

        if (np.array_equal(tempalpha,alpha)):
            break
        alpha=tempalpha
        syndrome=(np.dot(ParityCheckMatrix,alpha))%2
        IsSyndromZero=np.count_nonzero(syndrome)
        
        if IsSyndromZero==0:
            break                        

    return alpha 


def DecoderBEC(RecievedMessage,RelationMatrix):
    n=len(RecievedMessage)
    k=int((np.sqrt(n)-1)*(np.sqrt(n)-1))
    alpha=np.array(RecievedMessage)

    check=0
    for i in range(n):
        if (alpha[i]==-1):
            check+=1   
    if check==0:
        return alpha

    for Cycle in range(30):
        tempalpha=np.array(alpha)

        for i in range(n-k):
            indexMatrix=np.zeros(n)
            z=0
            for j in range(0,n):
                if (RelationMatrix[i][j]==1):
                    if (tempalpha[j]==-1):
                        indexMatrix[z]=j
                        z+=1
            if (z!=1):
                continue
            sum=0
            for j in range(0,n):
                if RelationMatrix[i][j]==1 and j!=indexMatrix[0]:
                    sum+=tempalpha[j]                    
            tempalpha[int(indexMatrix[0])]=sum%2

        CheckEqual=tempalpha-alpha
        if (np.count_nonzero(CheckEqual)==0):
            break

        alpha=tempalpha

        check=0
        for i in range(n):
            if (alpha[i]==-1):
                check+=1   
        if check==0:
            break 

    return alpha



def ProductCodeBsc():
    k=int(input("Enter the length of message signal:\n"))
    x=np.sqrt(k)
    y=np.floor(x)
    while x!=y:
        print("Invalid lenth,length  must be a perfect square\n")
        k=int(input("Enter the length of message signal:\n"))
        x=np.sqrt(k)
        y=np.floor(x)    


    Message=np.zeros(k)
    print("Enter the message bits:\n")  
    for i in range(k):
        Message[i]=int(input())
    
    a=Encoder(Message)
    print("Entered Message is : ",Message)
    print("Encoded Message is: ",a)
    p=float(input("Enter the probability of error:  "))
    while p>1 or p<0 :
        print("Enter a number between 0 and 1")
        p=float(input("Enter the probability of error:  "))
    
   
    NoiseMBsc=bsc(a,p)
    print(" Message with noise i.e Recievd message through BSC is: ",NoiseMBsc)
    
    
    DecodedBsc=decoder(NoiseMBsc,ParityCheckMatrix(k))
    print("Decoded Message BSC is: ",DecodedBsc)
    

def ProductCodeBec():
    k=int(input("Enter the length of message signal:\n"))
    x=np.sqrt(k)
    y=np.floor(x)
    while x!=y:
        print("Invalid lenth,length  must be a perfect square\n")
        k=int(input("Enter the length of message signal:\n"))
        x=np.sqrt(k)
        y=np.floor(x)    


    Message=np.zeros(k)
    print("Enter the message bits:\n")  
    for i in range(k):
        Message[i]=int(input())
    
    a=Encoder(Message)
    print("Entered Message is : ",Message)
    print("Encoded Message is: ",a)
    p=float(input("Enter the probability of error:  "))
    while p>1 or p<0 :
        print("Enter a number between 0 and 1")
        p=float(input("Enter the probability of error:  "))
    
    NoiseMBec=bec(a,p)

    
    
    print(" Message with noise i.e Recievd message through BEC is: ",NoiseMBec)
    DecodedBEC=DecoderBEC(NoiseMBec,ParityCheckMatrix(k))
    
    print("Decoded Message BEC is: ",DecodedBEC)

    

ProductCodeBsc()


















