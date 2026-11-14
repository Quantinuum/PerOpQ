# Getting started

PerOpQ optimizes a product of Pauli rotations to approximate a Hamiltonian
timestep, using a truncated Baker-Campbell-Hausdorff (BCH) error objective.
The workflow is to define the Hamiltonian, choose an ansatz and time, initialize
its parameters, optimize, and check the resulting evolution.

## Install and run

This walkthrough was checked with Python 3.12 and the project's NumPy/Numba
dependencies. To run the example from a source checkout:

```console
python -m pip install .
python examples/getting_started.py
```

For development and the documentation build, see the development instructions
on the main page. The larger plotting examples also use Matplotlib.

## A two-qubit timestep

The example uses the noncommuting Hamiltonian

```{math}
H = 0.7 Z\otimes Z + 0.3 X\otimes I + 0.2 I\otimes X
```

and approximates `exp(-1j * time * H)` at `time=0.2`. Each Pauli string has
`length=2`; the scalar multiplier supplies its Hamiltonian coefficient.

```{literalinclude} ../examples/getting_started.py
:language: python
```

`number_of_layer=3` repeats the ordered list of Pauli rotations three times.
`set_theta_to_trotter()` initializes their angles from the Hamiltonian
coefficients and timestep. `optimize_arbitrary` updates the ansatz's `theta`
in place. Here `order=3` selects the truncated BCH objective; it is distinct
from both layer count and the optimizer's stopping tolerance.

The reference is constructed independently with NumPy Pauli matrices and
SciPy's matrix exponential. The printed error is
`norm(U_approx - U_exact, "fro") / sqrt(4)`, including global phase. Both
initial and optimized errors are measured for this particular model and time;
their exact values depend on optimizer and dependency versions.

## Choosing a calculation

A smaller truncated objective does not guarantee a smaller exact error for
every timestep. Check the optimized unitary against exact evolution when the
system is small enough, and inspect the returned SciPy optimization result
when diagnosing convergence. Vary the timestep, layer count and BCH order
separately to understand their cost and accuracy effects.

Exact matrix methods store objects of size `2**n` by `2**n` and are intended
for small-system checks. The larger examples in the repository demonstrate
observable evolution and lattice models; start with this two-qubit example
before increasing system size.

Continue with the [API workflow](api.md) or the generated reference below it.
