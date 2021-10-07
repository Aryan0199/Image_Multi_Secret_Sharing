from operator import add

class Polynomial(object):
    field_value = 257

    def __init__(self, poly_coeff):
        self.poly = poly_coeff

    def divide_by_constant(self, c):
        """
        Divides all coefficients of a polynomial by a constant
        """
        inv = None
        p1 = self.poly
        for j in range(self.field_value):
            if (c * j) % self.field_value == 1:
                inv = j
                break
        p1 = (Polynomial(p1)).multiply(Polynomial([inv]))
        return p1

    def add(self, poly2):
        """
        Adds another polynomial to the current polynomial
        """
        p1 = self.poly
        p2 = poly2.poly
        temp1 = [0] * (abs(len(p1) - len(p2)))
        if len(temp1) != 0:
            if len(p1) > len(p2):
                p2 = temp1 + p2
            else:
                p1 = temp1 + p1
        res = list(map(add, p1, p2))
        for i in range(len(res)):
            res[i] %= self.field_value
        c = Polynomial(res)
        return c

    def multiply(self, poly2):
        """
        Multiplies another polynomial to the current polynomial
        """
        p1 = self.poly
        p2 = poly2.poly
        l = [0] * (len(p1) + len(p2) - 1)
        degree_res = len(l) - 1
        degree_p1 = len(p1) - 1
        degree_p2 = len(p2) - 1
        for i in range(len(p1)):
            for j in range(len(p2)):
                pos = degree_p1 + degree_p2 - i - j
                index_l = degree_res - pos
                l[index_l] += p1[i] * p2[j]
        for i in range(len(l)):
            l[i] %= self.field_value
        res = Polynomial(l)
        return res

    def eval(self, x):
        """
        Evaluates the polynomial at a given point x.
        """
        p1 = self.poly
        s = 0
        length = len(p1)
        for i in range(length):
            uu = 1
            for j in range(length - i - 1):
                uu = (uu * x) % (self.field_value)
            s += ((p1[i]) * (uu)) % self.field_value
        return s % self.field_value
