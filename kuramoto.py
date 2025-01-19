import numpy as np

class Kuramoto:
    def __init__(self, coupling=1, dt=0.01, T=10, n_nodes, natfreqs):
        self.dt = dt
        self.T = T
        self.coupling = coupling
        self.n_nodes = n_nodes
        self.natfreqs = natfreqs

    def init_angles(self):
        return 2 * np.pi * np.random.random(size=self.n_nodes)

    def derivative(self, angles_vec, t, adj_mat, coupling):
        
        angles_i, angles_j = np.meshgrid(angles_vec, angles_vec)
        interactions = adj_mat * np.sin(angles_j - angles_i)

        dxdt = self.natfreqs + coupling * interactions.sum(axis=0)
        return dxdt

    def integrate(self, angles_vec, adj_mat):
        n_interactions = (adj_mat != 0).sum(axis=0)
        coupling = self.coupling / n_interactions

        t = np.linspace(0, self.T, int(self.T/self.dt))
        timeseries = odeint(self.derivative, angles_vec, t, args=(adj_mat, coupling))
        return timeseries.T

    def run(self, adj_mat=None, angles_vec=None):
        if angles_vec is None:
            angles_vec = self.init_angles()

        return self.integrate(angles_vec, adj_mat)

    def phase_coherence(self, angles_vec):
        suma = sum([(np.e ** (ij * i)) for i in angles_vec])
        return abs(suma / len(angles_vec))

    def mean_frequency(self, act_mat, adj_mat):
        _, n_steps = act_mat.shape

        dxdt = np.zeros_like(act_mat)
        for time in range(n_steps):
            dxdt[:, time] = self.derivative(act_mat[:, time], None, adj_mat)

        integral = np.sum(dxdt * self.dt, axis=1)
        meanfreq = integral / self.T
        return meanfreq
