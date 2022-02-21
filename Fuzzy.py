from turtle import speed
import numpy as np
Temperature = 0
Humidity = 97

print("The input temperature is:", Temperature)
print("The input humidity is:", Humidity)
print("\n")

#Defining Membership Functions

def leftOpen(x,a,b):
    if x<a:
        return 1
    if a<x and x<=b:
        return (b-x)/(b-a)
    else:
        return 0

def rightOpen(x,a,b):
    if x<a:
        return 0
    if a<x and x<=b:
        return(x-a)/(b-a)
    else:
        return 1

def triangular(x,a,b,c):
    return max(min((x-a)/(b-a), (c-x)/(c-b)),0)


#Creating Fuzzy Partitions

def tPartition(x):
    VC = 0; C = 0; TN = 0; H = 0; VH = 0;

    if x>=-8 and x<10:
        VC = leftOpen(x,1,10)
    if x>0 and x<20:
        C = triangular(x,0,10,20)
    if x>10 and x<30:
        TN = triangular(x,10,20,30)
    if x>20 and x<40:
        H = triangular(x,20,30,40)
    if x>30 and x<=50:
        VH = rightOpen(x,30,40)

    return VC,C,TN,H,VH;

def hPartition(x):
    D = 0; HN = 0; W = 0;

    if x>=0 and x<40:
        D = leftOpen(x,20,40)
    if x>30 and x<70:
        HN = triangular(x,30,50,70)
    if x>60 and x<=100:
        W = rightOpen(x,60,80)

    return D,HN,W;

def sPartition(x):
    VS =0; S = 0; F = 0;

    if x>0 and x<10000:
        VS = triangular(x,0,500,1000)
    if x>500 and x<1500:
        S = triangular(x,500,1000,1500)
    if x>1000 and x<2000:
        F = triangular(x,1000,1500,2000)

    return VS,S,F;

#Fuzzyfication:

VC,C,TN,H,VH = tPartition(Temperature)
D,HN,W = hPartition(Humidity)

output1= [VC,C,TN,H,VH]
output2= [D,HN,W]
print("After Fuzzification:")
print("Fuzzy values of temperature are:")
print(["VeryCold","Cold","Nornal","Hot","VeryHot"])
print(np.round(output1,2))
print("Fuzzy values of Humidity are:")
print(["Dry","Normal","Wet"])
print(np.round(output2,2))

"""Processing Section
    Consists of Rule definiton, comparison,etc"""

def cmpr(a,b):
    out=0
    if a>b and a!=0 and b!=0:
        out = b
    else:
        out = a
    
    if a==0 and b!=0:
        out = b
    
    if b==0 and a!=0:
        out = a

    return out


def rule(VC,C,TN,H,VH,D,HN,W):

    VS = []
    VS.append(min(VC,D))
    VS.append(min(VC,HN))
    VS.append(min(VC,W))
    VS.append(min(C,HN))
    VS.append(min(C,W))
    VS.append(min(TN,W))
    VS = sorted(VS,key=lambda x:float(x))

    S = []
    S.append(min(C,D))
    S.append(min(TN,D))
    S.append(min(TN,HN))
    S.append(min(H,HN))
    S.append(min(H,W))
    S.append(min(VH,W))
    S = sorted(S,key=lambda x:float(x))

    F = []
    F.append(min(H,D))
    F.append(min(VH,D))
    F.append(min(VH,HN))
    F=sorted(F,key=lambda x:float(x))

    svs=VS[len(VS)-1]
    ss=S[len(S)-1]
    sf=F[len(F)-1]
    print(svs,ss,sf)

    return svs,ss,sf

#Fuzzy outputs for Motor Speed is calculated using the given rules

verySlow,slow,fast = rule(VC,C,TN,H,VH,D,HN,W)

#Displaying Fuzzy Output

output3 = [[verySlow,slow,fast]]
print("The fuzzy outputs are:")
print(["veryslow","slow","fast"])
print(np.round(output3,2))

#Defuzzification of the fuzzy output to produce crisp result

def tArea(x,a,b,c):
    x1 = x*(b-a)+a
    x2 = c-x*(c-b)
    d1=(c-a)
    d2=(x2-x1)
    a=(1/2)*x*(d1+d2)
    return a

"""def olArea(x,a,b):
    x1=b-x*(b-a)
    return 1/2*x*(b+x1),b/2

def orArea(x,a,b):
    x1=(b-a)*x+a
    a1=(1/2)*x*"""

def defuz(verySlow,slow,fast):
    area1=0
    area2=0
    area3=0
    c1=0
    c2=0
    c3=0

    if verySlow!=0:
        area1=tArea(verySlow,0,500,1000)
        c1=500

    if slow!=0:
        area2=tArea(slow,500,1000,1500)
        c2=1000

    if fast!=0:
        area3=tArea(fast,1000,1500,2000)
        c3=1500

    divident = area1*c1 +area2*c2 +area3*c3  
    divisor = area1+area2+area3

    if divisor ==0:
        print("No rules matched")
        return 0
    else:
        crispyresult= divident/divisor
    
    return crispyresult

Result = defuz(verySlow,slow,fast)
print("\nThe speed of the motor is:",Result)