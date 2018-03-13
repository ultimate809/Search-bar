import nltk
from nltk.corpus import wordnet	
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def list_comp(inputc,l,tempinp):

	list_2=l.split()
	count=0
	for i in inputc:
		index_2=0
		for ele in list_2:
			if(i==ele):
				count=count+1
				list_2.pop(index_2)
				index_2=index_2-1
				break
			index_2=index_2+1
	return count	

def comp_base_words(inputc,line,tempinp):
	templ=list(inputc)
	index_1=0
	#print(templ)
	list_2=line.split()
	#print(list_2)
	for i in templ:
		index_2=0
		for ele in list_2:
			if(i==ele):
				templ.pop(index_1)
				index_1=index_1-1
				list_2.pop(index_2)
				index_2=index_2-1
				break
			index_2=index_2+1
		index_1=index_1+1
	
	#print(templ)
	#print(list_2)	
	
	stop_words=set(stopwords.words("english"))						
	
	sen1=[]
	sen2=[]	
											#removing stop words
	for w in templ:
		if w not in stop_words:
			sen1.append(w)
	for w in list_2:
		if w not in stop_words:
			sen2.append(w)		
	
	#print(sen1)
	#print(sen2)
	try:
		tsen1=[]
		tsen2=[]
		ps=PorterStemmer()									# converting both the list to base words
		for w in sen1:
			tsen1.append(ps.stem(w))
		for w in sen2:
			tsen2.append(ps.stem(w))
		
		#print(tsen1)
		#print(tsen2)
	
		lpop1=[]
		lpop2=[]
		base_count=0										#counting the base no of same base words
		ind1=0											#and deleting them from the oiginal list
		for i in tsen1:
			ind2=0
			for j in tsen2:
				if(i==j):#and (ind2 not in lpop2) :
					sen2.pop(ind2)
					lpop1.append(ind1)
					base_count+=1
					break
				ind2=ind2+1
			ind1=ind1+1
		#print("\n",sen1)
		#print(sen2)
		#print(lpop1)
		#print(lpop2)
		for i in reversed(lpop1):
			sen1.pop(i)
		#print(base_count)
		#print(sen1)
		#print(sen2)
	except:
		base_count=0
	
	return (sen1,sen2,base_count)
	
def comp_similarity(sen1,sen2):
	sim=0
	#print("yo")
	#print(sen1,sen2)
	#return 0
	(maxs1,maxs2,maxs3)=(0,0,0)
	try:
		for w1 in sen1:
			for w2 in sen2:
				#print(w1,w2)
				s2=wordnet.synsets(w2)[0]
				s1=wordnet.synsets(w1)[0]
				sim=(s1.wup_similarity(s2))
				#print(w2,sim)
				
				if(sim>0.4):
					if sim<maxs3:
						continue
					if sim>maxs3 and sim <maxs2:
						maxs3=sim
					if sim<maxs1:
						maxs3=maxs2
						maxs2=sim
					if sim>maxs1:
						maxs3=maxs2
						maxs2=maxs1
						maxs1=sim
		#print	(maxs1,maxs2,maxs3)
	except:
		sim=0					
	return (maxs1,maxs2,maxs3)
	

def str_res(inputc,tempinp):
	f1=open("sk.txt","r")
	listw=[]
	match=[]
	for i in range(0,30):
		match.append(-1)
		listw.append("none")
	#print(match)
	for line in f1.readlines():
		rep_ind=29
		m=list_comp(inputc,line,tempinp)
		#print(line)
		if(negation(inputc,line)):
			m=-1
			#print(line)
		if(m>match[rep_ind]):
			while(m>match[rep_ind]):
				listw[rep_ind]=listw[rep_ind-1]
				match[rep_ind]=match[rep_ind-1]
				rep_ind=rep_ind-1		
				if(rep_ind==-1):
					break
			listw[rep_ind+1]=line
			match[rep_ind+1]=m
	#print(listw)
	f1.close()
	return (listw,match)
			
def negation(inputc,line):
	tl2=list(inputc)
	tl=line.split()
	no=['not','no','negate']
	flag=0
	for w in tl:
		for w2 in no:
			if w==w2:
				flag=1
				break
		if flag==1:
			break
	d=0
	for w in tl2:
		for w2 in no:
			if w==w2:
				if flag==1:
					flag=0
					d=1
					break
				else:
					flag=1
					d=1
					break
		if d==1:
			break			
	return flag
			
	

	
def comp_word_power(inputc,line,tempinp):
	try:
		(sen1,sen2,base_count)=comp_base_words(inputc,line,tempinp)
		similarity=comp_similarity(sen1,sen2)
		word_power=2*base_count+0.4*(similarity[0]+similarity[1]+similarity[2])
	except:
		return 0;
	return word_power

def arrange_all(listw,match,inputc,tempinp):
	order=[]
	power=[]
	tempinp=list(inputc)
	for i in range(0,30):
		power.append(0)
	ind=0
	try:
		for i in listw:
			tempinp=list(inputc)
			power[ind]=4*match[ind]+comp_word_power(inputc,i,tempinp)			#total powerof the top 30 sentences 
			ind+=1
	except:
		power[ind]=0
	for j in range(0,len(listw)):
		for i in range(0,len(listw)-1):
			if(power[i]<power[i+1]):
				temp=listw[i]
				listw[i]=listw[i+1]
				listw[i+1]=temp
				tem=power[i]
				power[i]=power[i+1]
				power[i+1]=tem
	return (listw,power)		
	
def no_output(power):
	if(power[0]==0.0):
		return 0
	return 1

def time_save():
	sen1=['ride']
	sen2=['me']
	test=comp_similarity(sen1,sen2)
	
def final_order():
	time_save()
	ch='y'
	while ch=='y' or ch=='Y':
		print("****************Search Bar Application***************************")
		inp=input("\nEnter the Sentence to search\n")
		inputc=inp.split()
		tempinp=list(inputc)
		(listw,match)=str_res(inputc,tempinp)
		(listw,power)=arrange_all(listw,match,inputc,tempinp)
		flag=no_output(power)
		if(flag==1):
			for i in range(0,3):
				print(listw[i])
		else:
			print("No Match Found")
		print("******************************************")
		ch=input("do you want to continue (y/n) :  ")
	return 0
	
final_order()	
	
		
	
