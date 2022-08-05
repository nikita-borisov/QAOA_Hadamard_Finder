# QAOA_Hadamard_Finder
Implementation of QAOA to find n-by-n Hadamard matrix. 

A Hadamard matrix, $H$,
is an n-by-n matrix with all entries populated with +1 or -1, such that any two distinct columns are orthonal (have dot product equal to zero). 
This condition is equivilant to $HH^T=nI$.

For example, a 2-by-2 Hadamard matrix can be
$$H_2=\begin{bmatrix}1&1\\1&-1\end{bmatrix},$$
since the two columns are orthogonal, which is related to the Hadamard gate in quantum computing
$$\frac{1}{\sqrt{2}}\begin{bmatrix}1&1\\1&-1\end{bmatrix}.$$

It can be shown that if $H$
is an n-by-n Hadamard matrix, then it must be the case $n=1,2$
or $n$
is a multiple of 4. The converse is not known, however. This problem is called the **Hadamard conjecture**: if $n$ is a multiple of 4 then an
n-by-n Hadamard matrix exists. We know that the conjecture is true if $n$
is power of 2 (we can the tensor product $H_2^{\otimes n}$
to get a $2^n$
-by-
$2^n$
matrix). We also know that if $n$
is product of a power of 2 and factors of the form $p^t+1$
, where $p$ is prime and $4|p^t+1$.

The smalled multiple of 4, for which we don't know whether or not a Hadamard matrix exists is $n=668$.

We apply the [Quantum Approximate Optimization Algorithm (QAOA)](https://qiskit.org/textbook/ch-applications/qaoa.html) as a proposed method for finding these matrices. This is a hybrid algorithm that itertively applies a parameterized qunatum circuit to find candidate solutions and a classic optimizer (we use COBYLA) that modifies these parameters. The algorithm produces an approximate solution, but will find an exact solution (an actual Hadamard matrix) with enough quantum circuit layers. 

In some sense, the circuit uses the optimal number of qubits: $n^2$
since this is the fewest bits of data needed to store the value of an n-by-n matrix with entries $\pm1$.
The QAOA requires a cost function to optimize. If $A$ has entries $\pm 1$,
then the diagonal entries of $HH^T$
are equal to $n$. 
Thus, we only have to check that the non-diagonal entries of $HH^T$
are zero. We define the cost function to minimize
$$C(H)=\sum_{i\neq j}\left(\sum_k H_{ik}H_{jk}\right)^2.$$
Given a bit string with $n^2$
entries of the form $b_{ik}=0,1$. 
Then the cost function in terms of the bits string is
$$C(b)=\sum_{i\neq j}\left(\sum_k (2b_{ik}-1)(2b_{jk}-1)\right)^2.$$
To turn this into a problem Hamiltonian (as seen in [earlier link](https://qiskit.org/textbook/ch-applications/qaoa.html)) we substitute $b_{ik}=\frac{1}{2}(I-Z_{ik})$,
where $Z_{ik}$ 
is a $Z$ gate applied to qubit corresponding to entry $(i,k)$.
This yields Hamiltonian (which is equivilant upon subtracting a scalar matrix to)
$$H_p=\sum_{i\neq j}\sum_{k\neq l}Z_{ik}Z_{jk}Z_{il}Z_{jl}.$$
When this Hamiltonian is converted to unitary gate: $e^{-i\gamma H_p}$,
we can apply a quantum circuit layer applying 6 CNOT gates and arbitrary rotation gate $R_z(2\gamma)$
for every term in the summation. 


