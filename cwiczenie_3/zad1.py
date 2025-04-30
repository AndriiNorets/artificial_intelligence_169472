class CSP:
    def __init__(self, variables, Domains, constraints):
        self.variables = variables
        self.domains = Domains
        self.constraints = constraints
        self.solution = None

    def solve(self):
        assignment = {}
        self.solution = self.backtrack(assignment)
        return self.solution

    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]
        return None

    def select_unassigned_variable(self, assignment):
        unassigned_vars = [var for var in self.variables if var not in assignment]
        return min(unassigned_vars, key=lambda var: len(self.domains[var]))

    def order_domain_values(self, var, assignment):
        return self.domains[var]

    def is_consistent(self, var, value, assignment):
        for constraint in self.constraints[var]:
            if constraint[1] in assignment:
                return constraint[2](value, assignment[constraint[1]])
        return True
    

variables = ["X1", "X2", "X3"]
Domains = {"X1": {'R', 'B', 'G'}, "X2": {'R'}, "X3": {'G'}}

constraints = {}
constraints["X1"] = []
constraints["X1"].append(("X1", "X2", lambda x, y: x != y))
constraints["X1"].append(("X1", "X3", lambda x, y: x != y))
constraints["X2"] = []
constraints["X2"].append(("X2", "X1", lambda x, y: x != y))
constraints["X2"].append(("X2", "X3", lambda x, y: x != y))
constraints["X3"] = []
constraints["X3"].append(("X3", "X2", lambda x, y: x != y))
constraints["X3"].append(("X3", "X1", lambda x, y: x != y))

csp = CSP(variables, Domains, constraints)
sol = csp.solve()
print(sol)
