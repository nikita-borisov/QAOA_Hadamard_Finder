
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute
from qiskit.circuit import Parameter
import numpy as np
import random as rd

#Finds n-by-n Hadamard matrix (matrix with entries 1,-1 such that any two columns are orthogonal)
#via QAOA
n=4
p=1 # number of layers

#We need a qubit for every entry of the matrix 
#  if the qubit is 1 this represents a -1 in the matrix. If the qubit is 0 it represents a +1 in the matrix
#matrix entry (i,j) will correspond to qubit with index n*i+j
numqubits = n**2

def create_qaoa_circ(n, theta):
    
    numqubits = n**2
    p = len(theta)//2  # number of alternating unitary iterations
    qc = QuantumCircuit(numqubits)
    
    #QAOA parameters to optimize for
    beta = theta[:p]
    gamma = theta[p:]
    
    # initial_state
    for i in range(0, numqubits):
        qc.h(i)
    
    for iteration in range(0, p):
        
        # problem unitary
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for l in range(n):
                        if (k!=l) and (j!=i):
                            qc.cnot(n*i+k,n*j+k)
                            qc.cnot(n*j+k,n*i+l)
                            qc.cnot(n*i+l,n*j+l)
                            qc.rz(2*gamma[iteration],n*j+l)
                            qc.cnot(n*i+l,n*j+l)
                            qc.cnot(n*j+k,n*i+l)
                            qc.cnot(n*i+k,n*j+k)

        # mixer unitary
        for i in range(0, numqubits):
            qc.rx(2 * beta[iteration], i)
            
    qc.measure_all()
        
    return qc

#returns execute_circ( ) for COBYLA to classically optimize
def get_expectation(n, shots=512):
    
    
    backend = Aer.get_backend('qasm_simulator')
    backend.shots = shots
    
    def execute_circ(theta):
        
        qc = create_qaoa_circ(n, theta)
        counts = backend.run(qc, seed_simulator=10, 
                             nshots=512).result().get_counts()
        
        return compute_expectation(counts, n)
    
    return execute_circ

#measures how good the current state is (COBYLA tries to minimize this value)
def compute_expectation(counts, n):
    
    avg = 0
    sum_count = 0
    for bitstring, count in counts.items():
        
        obj = hadamard_obj(bitstring, n)
        avg += obj * count
        sum_count += count
    
    #returns the expected cost from those measurement results
    return avg/sum_count

#measures how for the solution is from optimum (ideally AA^T=nI)
#it does so by summing squares of non-diagonal entries of AA^T (if these entries are zero than AA^T=nI)
def hadamard_obj(x, n):  
    obj = 0
    for i in range(n):
        for j in range(n):
            if i!=j:
                temp=0
                for k in range(n):
                    temp+=(2*int(x[n*i+k])-1)*(2*int(x[n*j+k])-1)
                obj+=temp**2
    return obj

from scipy.optimize import minimize

#change p to increase number of layers (chance of finding Hadamard matrix)
expectation = get_expectation(n)

res = minimize(expectation, np.ones(2*p), method='COBYLA')
print(res)



backend = Aer.get_backend('aer_simulator')
backend.shots = 512

qc_res = create_qaoa_circ(n, res.x)

counts = backend.run(qc_res, seed_simulator=10).result().get_counts()
#print(counts)


#find best matrix candidate in counts
minVal=n**4
minMatrix="-1"
matrixCount=0
succCount=0
for key in counts:
    keyCost=hadamard_obj(key,n)
    if keyCost<minVal:
        minMatrix=key
        minVal=keyCost
        matrixCount=counts[key]
    if keyCost==0:
        succCount+=counts[key]

#find best matrix candidate as most likely measurement outcome
#minMatrix=max(counts, key=counts.get)
#minVal=hadamard_obj(minMatrix,n)
    
A = np.zeros([n,n])
for i in range(n):
    for j in range(n):
        1
        A[i,j]=(-1)**int(minMatrix[n*i+j]) 
print(f"{A} with non-Hadamardness {minVal} (found a Hadamard matrix if 0) measured {counts[minMatrix]} time(s)")
totMeasurements=sum(counts.values())
print(f"{succCount}/{totMeasurements} good measurement rate")
