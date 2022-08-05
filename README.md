# QAOA_Hadamard_Finder
Implementation of QAOA to find n-by-n Hadamard matrix. 

A Hadamard matrix is an n-by-n matrix with all entries populated with +1 or -1, such that any two distinct columns are orthonal (have dot product equal to zero).

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

We apply the [Quantum Approximate Optimization Algorithm (QAOA)](https://qiskit.org/textbook/ch-applications/qaoa.html) as a proposed method for finding these matrices. 
