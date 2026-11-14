# API workflow

The generated reference documents the modules and signatures. This guide
connects the main objects in a Hamiltonian-simulation calculation.

| Stage            | API                                                                                                 | Role                                                                      |
| ---------------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Represent terms  | {py:class}`peropq.pauli_bitstring.PauliString`, {py:func}`peropq.pauli_bitstring.pauli_from_string` | Construct Pauli strings and attach scalar coefficients.                   |
| Define the model | {py:class}`peropq.hamiltonian.Hamiltonian`                                                          | Store the term list and its separate coefficients.                        |
| Choose an ansatz | {py:class}`peropq.unconstrained_variational_unitary.UnconstrainedVariationalUnitary`                | Set layer count, timestep and independently tunable rotation angles.      |
| Optimize         | {py:class}`peropq.optimizer.Optimizer`                                                              | Minimize a BCH objective or a small-system exact objective.               |
| Check evolution  | {py:class}`peropq.ed_module.ExactDiagonalization`                                                   | Construct matrix evolution, apply it to a state and measure exact errors. |

## Parameters and objectives

For `UnconstrainedVariationalUnitary`, `theta` has one row per layer and one
column per Hamiltonian term. `flatten_theta` and `unflatten_theta` bridge this
array and the vector used by numerical optimizers. Reinitialize the angles
when starting a separate comparison with different settings.

`Optimizer.optimize_arbitrary` constructs a
{py:class}`peropq.bch_optimized.VariationalNorm` and updates the supplied ansatz.
Its `order` argument controls the truncated BCH calculation. With `cache=True`
it also returns the constructed norm object for reuse; check that the model
and ansatz structure remain compatible before reusing it.

{py:class}`peropq.variational_unitary.VariationalUnitary` provides the constrained
ansatz interface used by `Optimizer.optimize`.
{py:class}`peropq.exact_norm.ExactUnitary` and `Optimizer.optimize_exact` provide
the matrix-based alternative for small systems. These interfaces serve
different optimization paths; use the matching optimizer method rather than
interchanging their parameter vectors.

## Reference and examples

- [Generated API reference](autoapi/index)
- [Executable two-qubit walkthrough](getting_started.md)
- [Repository examples](https://github.com/Quantinuum/PerOpQ/tree/main/examples)

The reference includes algebra and commutator helpers as well as the main
workflow. Exact diagonalization is a validation tool for tractable sizes;
it does not establish hardware performance or accuracy for larger systems.
