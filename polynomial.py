from __future__ import annotations

class MultivariateKnotPolynomial:
    def __init__(self, n_vars: int, coefficients: dict[tuple[int, ...], int]):
        self.n_vars = n_vars
        self.coefficients = coefficients
        
        for power in coefficients:
            if len(power) != n_vars:
                raise TypeError(f"{len(power)} variables counted, expected {n_vars}.")
    
    def __call__(self, *values: float) -> float:
        if len(values) != self.n_vars:
            raise ValueError(f"knot polynomial requires {self.n_vars} input variables.")

        sum: float = 0
        for powers, coefficient in self.coefficients.items():
            term = 1
            for power, value in zip(powers, values):
                term *= value ** power
            sum += coefficient * term
        
        return sum
    
    def __add__(self, other: MultivariateKnotPolynomial):
        if self.n_vars != other.n_vars:
            raise TypeError("cannot add two polynomials with different numbers of variables.")

        power_list = list(set(list(self.coefficients.keys()) + list(other.coefficients.keys())))
        new_coefficients: dict[tuple[int, ...], int] = {}

        for powers in power_list:
            sum = self.coefficients.get(powers, 0) + other.coefficients.get(powers, 0)
            new_coefficients[powers] = sum

        return MultivariateKnotPolynomial(self.n_vars, new_coefficients)
    
    def __mul__(self, other: MultivariateKnotPolynomial):
        if self.n_vars != other.n_vars:
            raise TypeError("cannot multiply two polynomials with different numbers of variables.")

        new_coefficients: dict[tuple[int, ...], int] = {}

        for powers1, coefficient1 in self.coefficients.items():
            for powers2, coefficient2 in other.coefficients.items():
                prod_power = tuple(power1 + power2 for power1, power2 in zip(powers1, powers2))
                if prod_power not in new_coefficients:
                    new_coefficients[prod_power] = 0
                new_coefficients[prod_power] += coefficient1 * coefficient2

        return MultivariateKnotPolynomial(self.n_vars, new_coefficients)
    
    def __pow__(self, power: int):
        if power < 0:
            raise ValueError("cannot take a knot polynomial to a negative power.")

        p = MultivariateKnotPolynomial.multiplicative_identity(self.n_vars)
        for i in range(power):
            p *= self
        return p
    
    def get_coefficient_from_power(self, power: int):
        return self.coefficients[power]
    
    def read(self, *vars: str) -> str:
        out = ''
        for i, (powers, coefficient) in enumerate(sorted(self.coefficients.items())):
            if coefficient == 0: continue

            if i == 0 and coefficient < 0:
                out += '- '
            elif i != 0 and coefficient > 0:
                out += ' + '
            elif coefficient < 0:
                out += ' - '

            if abs(coefficient) != 1 :
                out += str(abs(coefficient))

            for power, var in zip(powers, vars):
                if power != 0:
                    out += var
                    if power != 1:
                        out += '^' + str(power)
        return out
    
    def additive_identity(n_vars) -> MultivariateKnotPolynomial:
        return MultivariateKnotPolynomial(n_vars, {})
    
    def multiplicative_identity(n_vars) -> UnivariateKnotPolynomial:
        return MultivariateKnotPolynomial(n_vars, {(0,)*n_vars: 1})

class UnivariateKnotPolynomial(MultivariateKnotPolynomial):
    def __init__(self, coefficients: dict[int, int]):
        super().__init__(1, {(power,): coefficient for power, coefficient in coefficients.items()})
    
    def additive_identity() -> UnivariateKnotPolynomial:
        return UnivariateKnotPolynomial({})
    
    def multiplicative_identity() -> UnivariateKnotPolynomial:
        return UnivariateKnotPolynomial({0: 1})
