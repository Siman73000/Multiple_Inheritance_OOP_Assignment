# This code calculates the optimal dimensions of a cylinder (radius and height) that minimize the surface area for a given volume.
import math # This line imports the math Python package for mathematical operations.
import sympy as sp # This line imports the sympy Python package for symbolic mathematics such as differentiation and solving equations.
class FunctionOps: # This defines a new class called FunctionOps.
    @staticmethod # This decorator indicates that the method can be called on the class itself, not just on instances of the class.
    def derivative(expr, var): # A new method defined as "derivative" that takes an expression and a variable.
        return sp.diff(expr, var) # This line returns the derivative of the expression with respect to the variable.
    @staticmethod # This decorator indicates that the method can be called on the class itself, not just on instances of the class.
    def solve_zero(expr, var): # A new method defined as "solve_zero" that takes an expression and a variable.
        return sp.solve(sp.Eq(expr, 0), var) # This line returns the solutions to the equation where the expression equals zero.
    @staticmethod # This decorator indicates that the method can be called on the class itself, not just on instances of the class.
    def to_numeric(expr, var): # A new method defined as "to_numeric" that takes an expression and a variable.
        return sp.lambdify(var, expr, 'math') # This line converts the expression into a numerical function that can be evaluated.
class Cylinder: # This defines a new class called Cylinder.
    def __init__(self): # This is the constructor method that initializes the class.
        self.r, self.V = sp.symbols('r V', positive=True, real=True) # This line creates symbolic variables r and V, which are positive and real.
        self.S = 2 * sp.pi * self.r**2 + 2 * self.V / self.r # This line defines the surface area S of the cylinder in terms of its radius r and volume V.
    def surface_area_expr(self): # This method returns the symbolic expression for the surface area.
        return self.S # This line returns the surface area expression.
    def height_expr(self, radius): # This method calculates the height of the cylinder given its radius.
        return self.V / (sp.pi * radius**2) # This line returns the height of the cylinder in terms of its volume and radius.
class CylinderOptimizer(FunctionOps, Cylinder): # This defines a new class called CylinderOptimizer that inherits from FunctionOps and Cylinder, demonstrating multiple inheritance.
    def __init__(self): # This is the constructor method that initializes the class.
        Cylinder.__init__(self) # This line initializes the Cylinder class.
    def optimal_dimensions(self, volume_value): # This method calculates the optimal dimensions of the cylinder for a given volume.
        dS_dr = self.derivative(self.S, self.r) # This line calculates the derivative of the surface area with respect to the radius.
        r_solutions = self.solve_zero(dS_dr, self.r) # This line finds the radius that minimizes the surface area by solving the equation where the derivative equals zero.
        r_opt = r_solutions[0] # This line selects the first solution as the optimal radius.
        h_opt_expr = self.height_expr(r_opt) # This line calculates the optimal height using the optimal radius.
        S_min_expr  = self.S.subs(self.r, r_opt) # This line calculates the minimum surface area by substituting the optimal radius into the surface area expression.
        r_fn = self.to_numeric(r_opt, self.V) # This line converts the optimal radius expression into a numerical function.
        h_fn = self.to_numeric(h_opt_expr, self.V) # This line converts the optimal height expression into a numerical function.
        S_fn = self.to_numeric(S_min_expr, self.V) # This line converts the minimum surface area expression into a numerical function.
        return r_fn(volume_value), h_fn(volume_value), S_fn(volume_value) # This line returns the optimal radius, height, and minimum surface area as numerical values for the given volume.
if __name__ == "__main__": # This line checks if the script is being run directly (not imported as a module).
    V = float(input("Enter a constant volume: ")) # This line prompts the user to enter a volume and converts it to a float.
    optimizer = CylinderOptimizer() # This line creates an instance of the CylinderOptimizer class.
    r_opt, h_opt, S_min = optimizer.optimal_dimensions(V) # This line calls the optimal_dimensions method to calculate the optimal dimensions for the given volume.
    print(f"For V = {V:.3f}:") # This line prints the volume.
    print(f"  - optimal radius = {r_opt:.4f}") # This line prints the optimal radius.
    print(f"  - optimal height = {h_opt:.4f}") # This line prints the optimal height.
    print(f"  - minimal surface area = {S_min:.4f}") # This line prints the minimum surface area.