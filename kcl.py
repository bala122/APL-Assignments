from sys import argv, exit
CIRCUIT = '.circuit'
END = '.end'
AC = '.ac'
import numpy as np
import math
import cmath
#Assuming one source one freq
freq=float(1)
class ac_source: #ac _ sources
	def __init__(self,name):
		self.name=name
	node1 = ""
	node2= ""
	value =int(0)
	#phase = int(0)
class ac_comp:
	def __init__(self,name):
		self.name=name
	node1 = ""
	node2= ""
	value =int(0)
	
class source: #classs of sources
	def __init__(self,name):
		self.name=name
	node1 = ""
	node2= ""
	value =int(0)
class dep_source:  # class of dependent sources
	def __init__(self,name):
		self.name=name
	node1 = ""
	node2= ""
	value =int(0)
class comp:		#class of different components
	def __init__(self,name):
		self.name=name
	name=""
	node1= ""
	node2=""
	value =int(0) 

dum=source('dum')
dum.value=0
dum.node1='n0'
dum.node2='n0'


def connect(curr_node,components):	#returns list of connected components and connected nodes
	lis=[]
	
	for obj in components:
		if(curr_node==obj.node1):
			lis.append((obj,obj.node2)) 
			
		elif(curr_node==obj.node2):
			lis.append((obj,obj.node1))
			
			
			#print(curr_node+""+obj.name)
	return(lis)
if len(argv) != 2:   #if arguments accepted via terminal are not enough it prints the same
	print('\nThe number of arguments are not enough')
	exit()
#FILE HANDLING
try:
	with open(argv[1]) as f:
		lines = f.readlines() 		#each line
		start = -1; end = -2
		for line in lines:              # extracting circuit definition start and end lines
			
			if AC == line[:len(AC)]:
				freq= float( (2*math.pi)*float(line.split('#')[0].split()[2])) #storing frequency
				print("Freq:",freq,"radians")
			if CIRCUIT == line[:len(CIRCUIT)]:
				start = lines.index(line) #defining the start index
			elif END == line[:len(END)]:
				end = lines.index(line)   #defining the end index
				
		if start >= end:                # validating circuit block 
			print('Invalid circuit definition')
			exit(0)
        
		inp = []    
		for line in lines[start+1:end] :
			inp.append(' '.join((line.split('#')[0].split()))) 
		#print(inp)
        #for l in lis:
         #   print(l)
		max_node=0 #stores number of nodes
		num_ac_volt=0# num of ac volt sources
		num_volt=0 #stores no. of voltage sources         
		f.close()
		symbols=['R','L','C','V','I','E','G','H','F'] #list of symbols
		# adding objects from netlist file to list
		circuit=[] #List having all the circuit parts
		for line in inp:                #going through input file
			
			for ch in symbols:				#going through symbols list
				if ch== line[:1]:
					
					num=line.index(ch) +1 #index of next char
					#r0= ac_source('dum_ac') 
					r1= dum
					if( (ch=='V' or ch=='I')and ( (line.split('#')[0]).split()[3] == 'ac')): #if it is ac source
						num_ac_volt+=1
						r0= ac_source(""+ch+line[num])
						val= float(line.split('#')[0].split()[4])/2 # Vpp/2 = amplitude of ac source
						phase =float(line.split('#')[0].split()[5]) #phase of source
						r0.value=val*(math.cos(phase)+1j*math.sin(phase))
						r0.node1=line.split('#')[0].split()[1] #node1 
						r0.node2=line.split('#')[0].split()[2] #node2 
						#print(val,phase,r0.value)
						#print(1/(1j*freq))
					#print(r1.node2)
						if(r0.node1=='GND'): 	#condition if you encounter a GND
							r0.node1='n0'		#for computation purposes we make it n0
						if(r0.node2=='GND'):
							r0.node2='n0'
						n1=int(r0.node1[1]+"")
						n2=int(r0.node2[1]+"")
						max_node=max(max_node,n1,n2) #finding max node number
					#print(line.split('#')[0].split())
						circuit.append(r0) #adding ac source
						
					else:								# if it is dc source or any other comp.
						if(ch=='V' or ch=='I' ):
							num_volt+=1
							r1=source(""+ch+line[num])
							#print(isinstance(r1,source))
						elif (ch=='R' or ch=='C' or ch=='L'):
							r1=comp(""+ch+line[num]) #making resistor object
						else:
							r1=dep_source(""+ch+line[num])
						r1.node1=line.split('#')[0].split()[1] #node1 
						r1.node2=line.split('#')[0].split()[2] #node2 
					
						#print(r1.node2)
						if(r1.node1=='GND'): 	#condition if you encounter a GND
							r1.node1='n0'		#for computation purposes we make it n0
						if(r1.node2=='GND'):
							r1.node2='n0'
						n1=int(r1.node1[1]+"")
						n2=int(r1.node2[1]+"")
						max_node=max(max_node,n1,n2) #finding max node number
					#max_node=max(max_node,n1,n2)
				
						r1.value=float(line.split('#')[0].split()[3]) #value of component/source
						circuit.append(r1) #adding object to the circuit list
					 					
		
#MAKING DICTIONARY OF NODES
		dict = {'n0':0}
		#print(max_node) 
		for i in range(1,max_node+1):  #running through objects to store node names ; no. of nodes= max_node+1
			dict['n'+str(i)+""]= i #assigning node name key values
	
		#print(dict['n2'])
		nodes=max_node+1
		
		
	
		
		M= np.zeros((nodes+num_volt+1,nodes+num_volt+1)) #initializing M matrix- ie in Mx = b to zero
		x= np.zeros((nodes+num_volt+1,1))
		b= np.zeros((nodes+num_volt+1,1))  #+1 is because of GND eqn
		#print(nodes)
		
		#print(M)
		dic_ac=dict
		
		
		for obj in circuit:
			if(isinstance(obj,comp) and obj.name[0]=='L' and num_ac_volt==0):
				dict[obj.node1]=dict[obj.node2]  # shorting two ports of inductor for dc analysis
		#print(dic_ac)
		#dictionary is made

	# following is for DC analysis Inductor has to be dealt with separately
		#Algorithm to set values in M matrix
		#Making a list of current sources
		curr_sources=[]
		curr_sources.append(dum) 
		#creating list of current sources
		
		for c in range(max_node+1): # making a list of current sources
			obj = circuit[c]
			#print(isinstance(obj,source))
			if( isinstance(obj,source) and obj.name[0]=='I'): #checking if its curr source
				curr_sources.append(obj)
			
				#print('hi')
			
			c+=1 
			
			
			#DC ANALYSIS
		
		for i in range(nodes): 
			curr_node='n'+""+str(i)  #stores starting node of current source
									
			connec_curr= connect(curr_node,curr_sources) #returns list of connected current sources
			for elem in connec_curr:	
				b[  dict[curr_node] ]+= elem[0].value		#adds up all values of current sources
			if(connec_curr==[]): 	#if there are no current sources connected
				b[  dict[curr_node]] =0
				# Run a search for the same node in all components- resistors or voltage sources
			
			
			connec_comp= connect(curr_node,circuit)			#returns list of connected components to node
			
			
			for elem in connec_comp:   # setting matrix values for current node
				#print( elem[0].name)
				if(isinstance(elem[0],comp) and  elem[0].name[0]=='R'):   #checking if its a resistance
					M[  dict[curr_node], dict[curr_node] ] += 1/elem[0].value  #current is leaving that node
					
				if(isinstance(elem[0],comp) and  elem[0].name[0]=='C'):   #checking if its a capacitance
					M[ dict[curr_node], dict[curr_node]]=0 		#opening circuit for cap
				if(isinstance(elem[0],source) and  elem[0].name[0]=='V'):  	#checking if its a voltage source 
					M[ dict[curr_node], nodes+dict[curr_node] ]=1  #current is leaving node
			#FOR ALL CONNECTED COMPONENTS									
			
			for elem in connec_comp:							#iterate through connected nodes
					#elem[0] gives connected component and elem[1] gives node
				if(isinstance(elem[0],source) and  elem[0].name[0]=='V'):  	#checking if its a voltage source 
					M[ dict[curr_node], nodes+dict[elem[1]]] =-1  #current is leaving node
					
				if(isinstance(elem[0],comp) and  elem[0].name[0]=='R'):   #checking if its a resistance
					M[ dict[curr_node], dict[elem[1]]] -=1/(elem[0].value)  #current is entering node from other components				
					
				if(isinstance(elem[0],comp) and  elem[0].name[0]=='C'):   #checking if its a capacitance
					M[ dict[curr_node], dict[elem[1]]]=0 		#opening circuit for cap
					
					#if its an inductor for dc analysis its shorted as seen earlier
					
					
		
		
		volt_sources=[] #creating list of Voltage sources size num_volt
		
		i=0
		for obj in circuit: # making a list of voltage sources
			if( isinstance(obj,source) and obj.name[0]=='V' ): #checking if its dc volt source
				volt_sources.append(obj)
				i+=1
				#print(obj.value)
		
		c=0
		for obj1 in volt_sources:  #running through volt sources to form KVL eqns
  			#print(obj1.name)
			b[nodes+c]= obj1.value  #setting values in b matrix 
			M[nodes+c, dict[obj1.node1] ] = +1 # setting value in M matrix ie in eqn- V1 - V2 = EMF
			M[nodes+c, dict[obj1.node2] ] =  -1 
			c+=1
		
		M[nodes+num_volt,0]=1 # for V0 = 0 GND voltage is zero
		
			
		#print(b)
		#print(M)
					
		# AC ANALYSIS
		
		
		
		
		dict = dic_ac 		#removing any shorts in inductor now
		print(dict)
		M_ac= np.zeros((nodes+num_ac_volt+1,nodes+num_ac_volt+1),dtype=np.complex_) #initializing M matrix- ie in Mx = b to zero
		x_ac= np.zeros((nodes+num_ac_volt+1,1),dtype=np.complex_)
		b_ac= np.zeros((nodes+num_ac_volt+1,1),dtype=np.complex_)  #+1 is because of GND eqnprint(num_volt)
		print(nodes,num_ac_volt)
		for i in range(nodes): 
			curr_node='n'+""+str(i)  #stores starting node of current source
									
			connec_curr= connect(curr_node,curr_sources) #returns list of connected current sources
			for elem in connec_curr:	
				b_ac[  dic_ac[curr_node] ]+= elem[0].value /(1j*freq)	#adds up all values of current sources
			if(connec_curr==[]): 	#if there are no current sources connected
				b_ac[  dic_ac[curr_node]] =0
				# Run a search for the same node in all components- resistors or voltage sources
			
			
			connec_comp= connect(curr_node,circuit)			#returns list of connected components to node
			
			
			for elem in connec_comp:   # setting matrix values for current node
				if(isinstance(elem[0],comp) and  elem[0].name[0]=='R'):   #checking if its a resistance
					M_ac[  dict[curr_node], dict[curr_node] ] += 1/elem[0].value  #current is leaving that node
				if(isinstance(elem[0],comp) and  elem[0].name[0]=='C'):   #checking if its a capacitance
					M_ac[ dict[curr_node], dict[curr_node]]+= ( elem[0].value *(1j*freq))		#opening circuit for cap
				if(isinstance(elem[0],ac_source) and  elem[0].name[0]=='V'):  	#checking if its a voltage source 
					M_ac[ dict[curr_node], nodes+dict[curr_node] ]=1  #current is leaving node
				if(isinstance(elem[0],comp) and  elem[0].name[0]=='L'):   #checking if its a inductor
					M_ac[ dict[curr_node], dict[curr_node]]+= 1/( elem[0].value *(1j*freq))		
		
			#FOR ALL CONNECTED COMPONENTS									
			
			for elem in connec_comp:							#iterate through connected nodes
					#elem[0] gives connected component and elem[1] gives node
				if(isinstance(elem[0],ac_source) and  elem[0].name[0]=='V'):  	#checking if its a voltage source 
					M_ac[ dict[curr_node], nodes+dict[elem[1]]] =-1  #current is leaving node
					
				if(isinstance(elem[0],comp) and  elem[0].name[0]=='R'):   #checking if its a resistance
					M_ac[ dict[curr_node], dict[elem[1]]] -=1/(elem[0].value)  #current is entering node from other components				
					
				if(isinstance(elem[0],comp) and  elem[0].name[0]=='C'):   #checking if its a capacitance
					M_ac[ dict[curr_node], dict[elem[1]]]-= ( elem[0].value *(1j*freq))		
				
				if(isinstance(elem[0],comp) and  elem[0].name[0]=='L'):   #checking if its a inductance
					M_ac[ dict[curr_node], dict[elem[1]]]-= 1/( elem[0].value *(1j*freq))		
				
		
			
		ac_volt_sources=[] #creating list of Voltage sources size num_volt
		
		i=0
		for obj in circuit: # making a list of voltage sources
			if( isinstance(obj,ac_source) and obj.name[0]=='V' ): #checking if its dc volt source
				ac_volt_sources.append(obj)
				i+=1
				#print(obj.value)
			
		c=0
		for obj1 in ac_volt_sources:  #running through volt sources to form KVL eqns
  			#print(obj1.name)
			b_ac[nodes+c]= obj1.value  #setting values in b matrix 
			M_ac[nodes+c, dict[obj1.node1] ] = +1 # setting value in M matrix ie in eqn- V1 - V2 = EMF
			M_ac[nodes+c, dict[obj1.node2] ] =  -1 
			c+=1
		
		M_ac[nodes+num_ac_volt,0]=1 # for V0 = 0 GND voltage is zero
		#print(M_ac)
		#print(b_ac)
		
		if(num_volt==0 and num_ac_volt!=0):
			
			#M_ac.resize(nodes+num_ac_volt,nodes+num_ac_volt)
			#b_ac.resize(nodes+num_ac_volt,nodes+num_ac_volt)
			#print(M_ac)
			print(nodes+num_ac_volt)
		
			M_ac[nodes+num_ac_volt-2]=M_ac[nodes+num_ac_volt]
			
			M_ac=M_ac[:nodes+num_ac_volt,:nodes+num_ac_volt]
			b_ac=b_ac[:nodes+num_ac_volt]	
			print("M matrix-")
			print(M_ac)
			print("B matrix-")
			print(b_ac)
			print("FINAL ANSWER(AC ANALYSIS):-")
			x_ac=np.linalg.solve(M_ac,b_ac)
			print(x_ac)
        	
		if(num_volt!=0 and num_ac_volt==0):
			
			#M.reshape(5,5)
			#np.resize(b,(nodes+num_volt-1,1))
			#M[0][5]=0
			#M[1][5]=0
			#M=M[0:5]
			print(nodes+num_volt)
			M[nodes+num_volt-2]=M[nodes+num_volt]
			M=M[:nodes+num_volt,:nodes+num_volt]
			b=b[:nodes+num_volt]
			print("M matrix-")
			print(M)
			print("B matrix-")
			print(b)
			print("FINAL ANSWER(DC ANALYSIS):-")
			print( np.linalg.solve(M,b))
        
        
        
        
except IOError:
	print('Invalid file')
	exit()

