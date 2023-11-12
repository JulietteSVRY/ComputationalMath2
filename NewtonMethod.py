import numpy as np
import matplotlib.pyplot as plt
import sympy as sp


class NewtonMethod:
    def __init__(self, f, jacobian, x0, eps=1e-6, max_iter=100):
        self.f = f
        self.jacobian = jacobian
        self.x = x0
        self.eps = eps
        self.max_iter = max_iter

    def solve(self):
        for i in range(self.max_iter):
            fx = self.f(self.x)
            if all(abs(fi) < self.eps for fi in fx):
                return tuple(self.x)
            Jx = self.jacobian(self.x)
            try:
                dx = self.solve_linear_system(Jx, fx)
            except ValueError:
                raise Exception("Linear system is singular")
            self.x = [x - d for x, d in zip(self.x, dx)]
        raise Exception("Maximum number of iterations exceeded")

    def solve_linear_system(self, A, b):
        n = len(b)
        for i in range(n):
            max_el = abs(A[i][i])
            max_row = i
            for k in range(i+1, n):
                if abs(A[k][i]) > max_el:
                    max_el = abs(A[k][i])
                    max_row = k
            if max_el == 0:
                raise ValueError("Matrix is singular")
            for k in range(i, n):
                tmp = A[max_row][k]
                A[max_row][k] = A[i][k]
                A[i][k] = tmp
            tmp = b[max_row]
            b[max_row] = b[i]
            b[i] = tmp
            for k in range(i+1, n):
                c = -A[k][i] / A[i][i]
                for j in range(i, n):
                    if i == j:
                        A[k][j] = 0
                    else:
                        A[k][j] += c * A[i][j]
                b[k] += c * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = b[i] / A[i][i]
            for k in range(i-1, -1, -1):
                b[k] -= A[k][i] * x[i]
        return x


def f(x):
    return [x[0]**2 + x[1]**2 - 1, x[0]**2 - x[1]**2]


def jacobian(x):
    return [[2*x[0], 2*x[1]], [2*x[0], -2*x[1]]]


solver = NewtonMethod(f, jacobian, [-2, -1])
x = solver.solve()
print(x)

x, y = sp.symbols('x y')
eq1 = sp.Eq(x**2 + y**2, 1)
eq2 = sp.Eq(x**2 - y**2, 0)
f1 = sp.lambdify((x, y), eq1.rhs - eq1.lhs)
f2 = sp.lambdify((x, y), eq2.rhs - eq2.lhs)
x_vals = np.linspace(-3, 3, 100)
y_vals = np.linspace(-3, 3, 100)
x_grid, y_grid = np.meshgrid(x_vals, y_vals)
z1 = f1(x_grid, y_grid)
z2 = f2(x_grid, y_grid)
plt.contour(x_grid, y_grid, z1, levels=[0], colors='red')
plt.contour(x_grid, y_grid, z2, levels=[0], colors='blue')
plt.axis('equal')
plt.show()

