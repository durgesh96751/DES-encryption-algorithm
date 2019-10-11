#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import textwrap
import binascii
#To compute the 56 bit key using pc-1 box 1a) computation
def key_56gen(pc_1, key_64bit):
    k56=""
    for index in pc_1:
        k56+= key_64bit[index-1]
        
    return(k56)
pc_1=[57,49,41,33,25,17,9,1,58,40,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]
key_64bit="0000000100100011010001010110011110001001101010111100110111101111"
key_56bits=key_56gen(pc_1,key_64bit)
print("The 56 bit key is as follows:-")
print(key_56bits)
#To compute the left and right halves of the key 1b.) computation of left circular shift
def splitkeys(key_56bits):
    left_L0=key_56bits[:28]
    right_R0=key_56bits[28:]
    return left_L0,right_R0
lefthalf_key, righthalf_key=splitkeys(key_56bits)
print("The left half key L0 after dividing is:-", lefthalf_key)
print("The right half key R0 after dividing is:- ", righthalf_key)

#to compute left circular shift of the lefthalf 
def leftpart_circularshift(i,newleft_28bitkey):
    left_1stpart=newleft_28bitkey[0:i]
    left_2ndpart=newleft_28bitkey[i:]
    c_1=left_2ndpart +left_1stpart
    return c_1
print("we need to compute the C1,D1 which are obtained by left circular shifts of the above keys")
c1=leftpart_circularshift(1,lefthalf_key)
print ("the left halfkey L1 after rotation is:-",c1)
#to compute right circular shift of the lefthalf 
def rightpart_circularshift(i,newright_28bitkey):
    right_1stpart=newright_28bitkey[0:i]
    right_2ndpart=newright_28bitkey[i:]
    d_1=right_2ndpart + right_1stpart
    return(d_1)
d1=rightpart_circularshift(1,righthalf_key)

print("the right half key R1 after rotation is:-",d1)
#to concatinate the new obtained left and right halves of key to compute 48bit key K1 
c1d1_concat=c1+d1
#To compute 48 bit round 1 key K1 1c) computation
def key_48bitround1(key_56bitround1):
    PC2=[14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]
    k48=""
    for index in PC2:
        k48 += key_56bitround1[index-1]
    return k48
key_48bits=key_48bitround1(c1d1_concat)
print("The 48 bit round key is:")
print(key_48bits)

#To compute the Binary value of the plaintext MESSAGES
def plaintxt_to_binary(plaintxt):
    mydict={}
    for i in (0,len(plaintxt),1):
        k=0
        k=ord(plaintxt[i])  #to convert a character to ascii integer value
        j=hex(k) #to convert an ascii integer to hexadecimal value
        l=""
        l=l+str(j)
        m=(bin(int(l, 16)))
        m=str(m)
        d=""
        
        for g in m:
            if g=='b':
                exit()
            else:
                d=d+g
        return d    
               
        
plaindata=['M','E','S','S','A','G','E','S']
m={}
for i in range(0,len(plaindata),1):
    k=plaintxt_to_binary(plaindata[i])
    m[plaindata[i]]=k
print("The binary values of the letters in the message are as follows:-")
print(m)
datab=""
for q in plaindata:
    datab=datab+m[q]
print("The combined binary value is:",datab)
Init_permutation=[58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8,57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7]    
    
#to apply initial permutation and break the plain text into left and right halves
def intpermutate():
    
    new_Init=""
    for i in Init_permutation:
        new_Init += datab[i-1]
    
        
    return(new_Init)
w=intpermutate()
print("After applying Initial permutation:-",w)
def splitplain(r):
    left_half=w[:32]
    right_half=w[32:]
    return left_half,right_half
lft_pt,rt_pt=splitplain(w)
print("The left half after applying Initial Permutation  is:-", lft_pt)
print("The right half after applying Initial Permutation is:-",rt_pt)

#To expand R0 to get E(R0) 
expansion_permut=[32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]
def expR0(rt):
    ex=""
    for i in expansion_permut:
        ex+=rt[i-1]
    return ex
y=expR0(rt_pt)
print("R0 after expansion is:-",y)

#To perform the operation A= E(R0) XOR K1
def a1():
    a_res=""
    for i in range(0,len(y),1):
        
        if y[i]==key_48bits[i]:
            a_res+="0"
        else:
            a_res+="1"
    return a_res
a_out=a1()
print("After performing the operation A= E(R0) XOR K1 the answer is:-", a_out)

#to group the 48-bit result A into sets of 6 bits and evaluate the corresponding S-box substitutions.

s_box=[
        #sbox 1
        [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
         [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
         [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
         [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
       ],
    #sbox 2
        [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
         [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
         [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
         [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
       ],
    #sbox 3
        [ [10,0,9,14,6,3,15,5,1,13,12,5,11,4,2,8],
          [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
          [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
          [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]
       ],
  #sbox 4
        [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
         [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
         [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
         [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
       ],
   #sbox 5
        [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
         [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
         [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
         [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
       ],
    #sbox 6
        [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
         [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
         [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
         [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]
      ],
    #sbox 7
        [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
         [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
         [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
         [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
      ],
  #sbox 8
        [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
         [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
         [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
         [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
      ]
  ]
def split_6(a_output_48):
    newlist_6bits=textwrap.wrap(a_output_48,6)
    return newlist_6bits
splitlist=split_6(a_out)
print("The new list of 6 bit pairs of the new 48 bits computed in function  A is:-")
print(splitlist)

def extrt_last_first_bits(bits_6):
    new_first_last_bit=""
    new_first_last_bit= bits_6[0]+bits_6[-1]
    return new_first_last_bit

def extract_middlefourbits(bits6):
    newfourbits=""
    newfourbits+=bits6[1:5]
    return newfourbits

def bin_to_decimal(binary_bits):
    dec=0
    dec=int(binary_bits,2)
    return dec

def dec_to_binary(decimal_bits):
    binary_bits=bin(decimal_bits)[2:].zfill(4)
    return binary_bits

def sbox_search(sbox_count,firstlast_bits,middle4_bits):
    searchrow=bin_to_decimal(firstlast_bits)
    searchcolumn=bin_to_decimal(middle4_bits)
    sbox_val=s_box[sbox_count][searchrow][searchcolumn]
    return sbox_val
sbox_res=""
sbox_ct=[0,1,2,3,4,5,6,7]
#for i in (0,len(splitlist),1):
print("The values of the individual computations of sboxes are:-")
for i in sbox_ct:
    data_split_list=splitlist[i]
    binary_last_firstbits=extrt_last_first_bits(data_split_list)
    binary_middle4bits=extract_middlefourbits(data_split_list)
    finalres=sbox_search(sbox_ct[i],binary_last_firstbits,binary_middle4bits)
    finalres=bin(finalres)
    finalres=str(finalres)
    #print(finalres)
    z=""
    for t in finalres:
        if t=='b':
            exit()
        else:
            z+=t
            
    z=str(z)
    print(z)
    for h in z:
        if z=="01011":
            z="1011"
        elif z=="011":
            z="0"+z
        else:
            exit()
    
    sbox_res+=z
    
print("The combined result after combining the sbox results is:-",sbox_res)

#to compute P(B)
P_list=[16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]

def P_B_compute(Inp_list):
    P_B_res=""
    for i in Inp_list:
        P_B_res+=sbox_res[i-1]
    return P_B_res
comp_pb=P_B_compute(P_list)
print("The value of P(B) is :-",comp_pb)

#to compute R1
def R1_compute(pb):
    z=""
    lft=lft_pt
    #print(lft)
    pb_new=pb
    #print(pb_new)
    for i in range(0,32,1):
        if lft[i]==pb[i]:
            z+="0"
        else:
            z+="1"
    return z
compute_R1=R1_compute(comp_pb)
print("The value of R1 is :-",compute_R1)
        
    
    
    
    

        
        
    
    
    



    
  

    
    





    
    

    
    
    


# In[ ]:






















# In[ ]:





# In[ ]:





# In[ ]:




