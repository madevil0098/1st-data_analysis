import pandas as pd
import numpy
import matplotlib.pyplot as mplib
#. Load the data file using pandas.

file=pd.read_csv("googleplaystore.csv")


#seperation of elements

file3=list(file.items())
head=[]
for i in file3:
    head.append(i[0])
#print(head)
elements=[]
length=len(file3[0][1])
for j in range(length):
    t=[]
    for i in range(len(head)):
        t.append(file3[i][1][j])
    elements.append(t)

#. Check for null values in the data. Get the number of null values for each column.

check_null=file.isnull().sum()
print("total null elements in row",check_null,sep="\n\n")
print()
print()

#. Drop records with nulls in any of the columns.
file2=file.notnull()


file4=list(file2.items())
elements1=[]
length=len(file4[0][1])
#print(length)
for j in range(length):
    t=[]
    for i in range(len(head)):
        t.append(file4[i][1][j])
    elements1.append(t)
#print(elements1)


#or


not_null_colum=[]
for i in range(len(elements)):
    
    if False not in elements1[i]:
        if "Varies with device" not in elements[i]:  
            not_null_colum.append(elements[i])

elements=not_null_colum
a=pd.DataFrame(not_null_colum,columns=head)
a.to_csv("not_null_colum.csv")

file2=a.isnull().sum()
print("after droping null elements ",file2,sep="\n")
print()



#. Variables seem to have incorrect type and inconsistent formatting. You need to fix them:
size_index=head.index("Size")
rating_index=head.index("Rating")
review_index=head.index("Reviews")
installs_index=head.index("Installs")
type_index=head.index("Type")
price_index=head.index("Price")
#print(size_index)
new_size=[]
for i in range(len(elements)):
    try:
        if "m" in elements[i][size_index].lower():
            sentence=elements[i][size_index].lower()
            sentence=sentence.replace("m", "")
            #print(i)
            sentence=float(sentence)
            sentence=sentence*1000
            sentence=str(sentence)+"K"
            elements[i][size_index]=sentence
            
    
        elif "k" in elements[i][size_index].lower():
            pass
        else:
            continue
        if 1<float(elements[i][rating_index]) and float(elements[i][rating_index])<5:
            new_size.append(elements[i])
    except Exception as e:
        print(i,e)


a=pd.DataFrame(new_size,columns=head)
a.to_csv("size_altered.csv")

#print(elements)



for i in range(len(new_size)):
    for j in range(len(new_size[i])):
        
        if "," in str(new_size[i][j]):
            new_size[i][j]=str((new_size[i][j]).replace(",",""))
        if "+" in str(new_size[i][j]):
            new_size[i][j]=str((new_size[i][j]).replace("+",""))
        if "$" in str(new_size[i][j]):
            new_size[i][j]=str((new_size[i][j]).replace("$",""))
        if str(new_size[i][j]).isnumeric():
            new_size[i][j]=float(new_size[i][j])


#. Reviews should not be more than installs as only those who installed can review the app. If there are any such records, drop them.
updated=[]

for i in range(len(new_size)):
    if float(new_size[i][review_index])<float(new_size[i][installs_index]):
        updated.append(new_size[i])
    if not(("Free" in new_size[i][type_index] and float(new_size[i][price_index])==0) or ("Paid" in new_size[i][type_index])):
        #print(not(("Free" in new_size[i][type_index] and float(new_size[i][price_index])==0) or ("Paid" in new_size[i][type_index])))
        continue

new_size=updated
a=pd.DataFrame(updated,columns=head)
a.to_csv("changed_altered.csv")


#. Performing univariate analysis

height=list(float(new_size[i][price_index]) for i in range(len(new_size)) if "Paid" in new_size[i][type_index] if ".99" in str(new_size[i][price_index]))
x=list(i for i in range(len(height)))
mplib.bar(x, height)
#print(len(height))
mplib.savefig("price_without_outlier.jpg")
mplib.close()

height=list(float(new_size[i][price_index]) for i in range(len(new_size)) if "Paid" in new_size[i][type_index] )
x=list(i for i in range(len(height)))
#print(len(height),len(x))
mplib.bar(x, height)
mplib.savefig("price.jpg")
mplib.close()

height=list(float(new_size[i][review_index]) for i in range(len(new_size)))
x=list(i for i in range(len(height)))
#print(len(height),len(x))
mplib.bar(x, height)
mplib.savefig("review.jpg")
mplib.close()

height=list(float(str(new_size[i][size_index]).lower().replace("k","")) for i in range(len(new_size)))
x=list(i for i in range(len(height)))
#print(len(height),len(x))
mplib.bar(x, height)
mplib.savefig("size.jpg")
mplib.close()


#. Outlier treatment:

price_treated=list(new_size[i] for i in range(len(new_size)) if ("Paid" in new_size[i][type_index] and 200 > float(new_size[i][price_index])) or ("Free" in new_size[i][type_index] ))

review_treated=list(price_treated[i] for i in range(len(price_treated)) if 2_000_000 > float(price_treated[i][review_index]))

a=pd.DataFrame(price_treated,columns=head)
a.to_csv("price_treated.csv")

a=pd.DataFrame(review_treated,columns=head)
a.to_csv("review_treat.csv")


"""
install_treated=list(review_treated[i][installs_index] for i in range(len(review_treated)))
install_treat=max(install_treated)
print((install_treat))
install_treated=list(review_treated[i][installs_index] for i in range(len(review_treated)) if review_treated[i][installs_index]<(install_treat/10))
install_treat=sum(install_treated)
print((install_treat))
install_tr=list((i/install_treat)*100 for i in (install_treated))
#print(install_tr)"""


