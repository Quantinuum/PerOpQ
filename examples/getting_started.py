"""Optimize a two-qubit timestep and compare it with an exact matrix reference."""

import numpy as np
from peropq.ed_module import ExactDiagonalization
from peropq.hamiltonian import Hamiltonian
from peropq.optimizer import Optimizer
from peropq.pauli_bitstring import pauli_from_string
from peropq.unconstrained_variational_unitary import UnconstrainedVariationalUnitary
from rich.console import Console
from scipy.linalg import expm


def optimize_two_qubits() -> tuple[float, float]:
    """Return the initial and optimized normalized Frobenius errors."""
    hamiltonian = Hamiltonian(
        [
            0.7 * pauli_from_string("ZZ", length=2),
            0.3 * pauli_from_string("XI", length=2),
            0.2 * pauli_from_string("IX", length=2),
        ],
    )
    time = 0.2
    ansatz = UnconstrainedVariationalUnitary(
        hamiltonian,
        number_of_layer=3,
        time=time,
    )
    ansatz.set_theta_to_trotter()
    exact = ExactDiagonalization(number_of_qubits=2)

    # Build an independent dense reference for exp(-i * time * H).
    identity = np.eye(2)
    x_matrix = np.array([[0, 1], [1, 0]])
    z_matrix = np.diag([1, -1])
    dense_hamiltonian = (
        0.7 * np.kron(z_matrix, z_matrix)
        + 0.3 * np.kron(x_matrix, identity)
        + 0.2 * np.kron(identity, x_matrix)
    )
    target = expm(-1j * time * dense_hamiltonian)
    initial = exact.get_variational_evolution(ansatz).toarray()
    before = float(np.linalg.norm(initial - target, ord="fro") / 2)

    Optimizer().optimize_arbitrary(
        ansatz,
        order=3,
        unconstrained=True,
        tol=1e-9,
    )
    optimized = exact.get_variational_evolution(ansatz).toarray()
    after = float(np.linalg.norm(optimized - target, ord="fro") / 2)
    return before, after


if __name__ == "__main__":
    initial_error, optimized_error = optimize_two_qubits()
    Console().print(f"Trotter error: {initial_error:.6g}")
    Console().print(f"Optimized error: {optimized_error:.6g}")
