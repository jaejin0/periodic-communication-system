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

 
