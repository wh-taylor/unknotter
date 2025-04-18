from __future__ import annotations

class Polynomial:
    def __init__(self, coefficients: dict[tuple[int, ...], int] | dict[int, int], fallback_n_vars: int = 0):
        # If `coefficients` uses integer powers instead of tuple powers,
        # we want to force it into tuple powers.
        corrected_coefficients: dict[tuple[int, ...], int] = {}
        if all(isinstance(key, int) or isinstance(key, float) for key in coefficients):
            corrected_coefficients = {(power,): coefficient for power, coefficient in coefficients.items()}
        else:
            corrected_coefficients = coefficients
        
        if len(corrected_coefficients) == 0:
            self.n_vars = fallback_n_vars
        else:
            # Set the number of variables to the length of the number of powers
            # used in defining the first term.
            self.n_vars = len(next(power for power in corrected_coefficients))

        self.coefficients = {
            powers: coefficient 
            for powers, coefficient
            in corrected_coefficients.items()
            if coefficient != 0}
        
        for powers in corrected_coefficients:
            if len(powers) != self.n_vars:
                raise TypeError(f"{len(powers)} variables counted, expected {self.n_vars}.")
    
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
    
    def __eq__(self, other: Polynomial) -> bool:
        return self.coefficients == other.coefficients and self.n_vars == other.n_vars
    
    def __add__(self, other: Polynomial):
        if self.n_vars != other.n_vars:
            raise TypeError("cannot add two polynomials with different numbers of variables.")

        power_list = list(set(list(self.coefficients.keys()) + list(other.coefficients.keys())))
        new_coefficients: dict[tuple[int, ...], int] = {}

        for powers in power_list:
            sum = self.coefficients.get(powers, 0) + other.coefficients.get(powers, 0)
            new_coefficients[powers] = sum

        return Polynomial(new_coefficients)
    
    def __mul__(self, other: Polynomial):
        if self.n_vars != other.n_vars:
            raise TypeError("cannot multiply two polynomials with different numbers of variables.")

        new_coefficients: dict[tuple[int, ...], int] = {}

        for powers1, coefficient1 in self.coefficients.items():
            for powers2, coefficient2 in other.coefficients.items():
                prod_power = tuple(power1 + power2 for power1, power2 in zip(powers1, powers2))
                if prod_power not in new_coefficients:
                    new_coefficients[prod_power] = 0
                new_coefficients[prod_power] += coefficient1 * coefficient2

        return Polynomial(new_coefficients)
    
    def __pow__(self, power: int):
        if power < 0:
            raise ValueError("cannot take a knot polynomial to a negative power.")

        p = Polynomial.one(self.n_vars)
        for i in range(power):
            p *= self
        return p
    
    def var(self, *vars: str) -> str:
        """Display a knot polynomial using a specified representation of a variable.
        
        Knot polynomials are stored without any particular variable in mind, and so
        one must be provided in order to display it.
        """
        if len(vars) != self.n_vars:
            raise ValueError(f"expected {self.n_vars} variables, received {len(vars)}: {', '.join(vars)}")
        out = ''
        for i, (powers, coefficient) in enumerate(sorted(self.coefficients.items())):
            if i == 0 and coefficient < 0:
                out += '- '
            elif i != 0 and coefficient >= 0:
                out += ' + '
            elif coefficient < 0:
                out += ' - '

            if abs(coefficient) != 1 or all(power == 0 for power in powers):
                out += str(abs(coefficient))

            for power, var in zip(powers, vars):
                if power != 0:
                    out += var
                    if power != 1:
                        out += '^'
                        if power.is_integer():
                            out += str(int(power))
                        else:
                            out += str(power)
        return out
    
    def __repr__(self) -> str:
        return self.var('_')
    
    def zero(n_vars: int = 1) -> Polynomial:
        return Polynomial({}, n_vars)
    
    def one(n_vars: int = 1) -> Polynomial:
        return Polynomial({(0,)*n_vars: 1})

