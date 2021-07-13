from __future__ import division
from sympy import*
import scipy.signal as sp
from pylab import *
import numpy as np
from scipy import*

s= symbols('s')# defining a symbol for s
init_printing()
#making the function giving the three matrices
def hpf(R1,C1,C2,R3,G,Vi,k):
	s= symbols('s')
	A = Matrix([ [s*C1 +1/R1 +s*C2, -s*C2,0,-1/R1], [0, -1,1, 1/G], [0 , 0, 1, -1/k], [-(R3), (1/(s*C2)+R3), 0, 0] ])
	b = Matrix( [s*C1*Vi,0,0,0])
	V = A.inv()*b # stores output matrix having V1, Vp, Vm, Vo
	return(A,b,V)
	

#OBTAINING STEP RESPONSE OF LPF
#Vi  = 1/s

#Given that: Vo = Vi/(jw*R1*C1)

R1=10e3
C1=1e-11
S_T_Num = poly1d([1])
S_T_Den= poly1d([R1*C1,0])  
#We directly multiply i/p = 1/s with the transfer function instead of convolution since u(t)*u(t) isn't actually valid



resol=500
resol1=1000000

#Time Scales
t= np.linspace(0,100,num=resol) #scale 1
t2= np.linspace(0,1000,num=resol) #second scale
t3 = np.linspace(0,10,num=resol1) #another s scale



d_t3= [0 for i in range(resol1)]
d_t3[0] = 1 #defining delta function

d_t = [0 for i in range(resol)]
d_t[0] = 1 #defining delta function


u_t= [1 for i in range(resol)]
u_t[0]=1            #Defining unit function

S_T = sp.lti(S_T_Num, S_T_Den)
t1= np.linspace(0,100,num=resol)
t1,y,svec= sp.lsim(S_T,u_t,t1) #gathering inverse laplace transform of output- step response
subplot(2,3,1)
title('Step response')
xlabel('time->(us)')
ylabel('v_step(t)(V)')
plot(t1,y) #step response


#The Second Circuit



Vi2= (2000*pi)/(s**2+(2000*pi)**2) +  s/(s**2+(2*(1e6)*pi)**2) #s domain response of input
Vi2_sin = (2000*pi)/(s**2+(2000*pi)**2) 
Vi2_cos = s/(s**2+(2*(1e6)*pi)**2) 
#defining parameters of circuit

R1=R3= 10e3
C1=C2=1e-9
G=1.586
G1=1.586
A,b,Vo2 = hpf(R1,C1,C2,R3,G,1,G1) #receiving Transfer function

# Now we have the symbolic expression for laplace transform of output 

print('Vo2[3]:',Vo2[3])
subplot(2,3,3)
ww=logspace(0,15,801)
ss=1j*ww
hf=lambdify(s,Vo2[3],'numpy')
v=hf(ss)
title('Magnitude plot of transfer func.')
loglog(ww,abs(v),lw=2)			#plotting magnitude response
grid(True)

#Finding the rational coeffiients of numerator and denominator
num,den = Vo2[3].as_numer_denom()
#expanding numerator 
num = num.expand() #Expanding numerator
den = den.expand()	#Expanding denominator



A,b,Vo2_cos = hpf(R1,C1,C2,R3,G,s/(s**2+(2e-6*(1e6)*pi)**2),G1) #receiving Transfer function from hpf
num_cos,den_cos=Vo2_cos[3].as_numer_denom() 

num_cos = num_cos.expand() #Expanding numerator
den_cos = den_cos.expand() #Expanding denominator
print('num, den _cos', num_cos,',',den_cos)
coeff_num= poly1d([float(num_cos.coeff(s,3)),0,0,0])		#finding coefficients
coeff_den= poly1d([float(den_cos.coeff(s,i)) for i in range(4,-1,-1)])
Vo2_cos = sp.lti(coeff_num, coeff_den) #transfer function cos
t,y2_cos3,svec = sp.lsim(Vo2_cos,d_t,t) #Simulating convoolution




A,b,Vo2_sin = hpf(R1,C1,C2,R3,G,(2000e-6*pi)/(s**2+(2000e-6*pi)**2),G1) #receiving Transfer function from hpf
num_sin,den_sin=Vo2_sin[3].as_numer_denom() 

num_sin = num_sin.expand() #Expanding numerator
den_sin = den_sin.expand() #Expanding denominator
print('num, den _sin', num_sin,',',den_sin)
coeff_num= poly1d([float(num_sin.coeff(s,2)),0,0])		#finding coefficients
coeff_den= poly1d([float(den_sin.coeff(s,i)) for i in range(4,-1,-1)])
Vo2_sin = sp.lti(coeff_num, coeff_den) #transfer function sine
t,y2_sin3,svec = sp.lsim(Vo2_sin,d_t,t) #finding o/p signal


print(y2_cos3)





subplot(2,3,2)

xlabel('time->(us)')
ylabel('Vo(t) -> (V)' )
title('Time domain output signal Vo(t) ')
plot(t,(y2_cos3+y2_sin3),label='net signal') #Plotting output
plot(t,y2_cos3,label='cos')
plot(t,y2_sin3,label='sin')
legend(loc='lower right')

#RESPONSE FOR A DAMPED SINUSOID
# take Vi as the following:
#circuit parameters
subplot(2,3,4)
Vi_3= exp(-0.05*t)*cos(1e5*t)
Vi_3_T = (s+0.05)/( (s+0.05)**2 + (1e5)**2 ) 

A,b,Vo_damp = hpf(R1,C1,C2,R3,G,Vi_3_T,G1) #receiving Transfer function
num_damp,den_damp=Vo_damp[3].as_numer_denom() 
num_damp = num_damp.expand()
den_damp = den_damp.expand()
print('num, den _damp', num_damp,',',den_damp)

coeff_num_damp= poly1d([float(num_damp.coeff(s,i)) for i in range(3,-1,-1)])  #finding coefficients
coeff_den_damp = poly1d([float(den_damp.coeff(s,i)) for i in range(4,-1,-1)])
Vo2_damp = sp.lti(coeff_num_damp, coeff_den_damp) #transfer function for plotting
t,y_damp,svec = sp.lsim(Vo2_damp,d_t,t) #finding o/p signal

xlabel('time->(s)')
ylabel('Vo3(t)')
title('Response for a damped sinusoid')
plot(t,y_damp)    #Plotting damped sinusoid response


#RESPONSE FOR UNIT STEP
subplot(2,3,5)

A,b,Vo_unit = hpf(R1,C1,C2,R3,G,1/s,G1) #receiving Transfer function
num_unit,den_unit=Vo_unit[3].as_numer_denom() 
num_unit = num_unit.expand()
den_unit = den_unit.expand()
print('num, den _unit', num_unit,',',den_unit)
coeff_num_unit= poly1d([float(num_unit.coeff(s,i)) for i in range(1,-1,-1)]) #finding coefficients
coeff_den_unit = poly1d([float(den_unit.coeff(s,i)) for i in range(2,-1,-1)])
Vo2_unit = sp.lti(coeff_num_unit, coeff_den_unit) #transfer function for plotting
t3,y_unit,svec = sp.lsim(Vo2_unit,d_t3,t3) #finding o/p signal

xlabel('time->(s)')
ylabel('Vo_unit(t)')
title('Response for a unit step function') 
plot(t3,(y_unit)) #Plotting response for unit step function 
#PLEASE NOTE HERE- ZOOM IN ON THE LEFT OF THE GRAPH TO SEE THE VARIATION.

show()
           
