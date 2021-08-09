"""
This file contains description of 8 test_mappings described by Hubbers in his master's thesis. See [5] in README.md file
"""
from mapping import Mapping
from algorithms import algorithms, methods

test_mappings = {}

h = Mapping([
    "X1",
    "X2",
    "X3",
    "X4 - a4*X1^3 - b4*X1^2*X2 - c4*X1^2*X3 - e4*X1*X2^2 - f4*X1*X2*X3" +
    "- h4*X1*X3^2 - k4*X2^3 - l4*X2^2*X3 - n4*X2*X3^2 - q4*X3^3"
],
    name="H1",
    params={"a4": "1", "b4": "1", "c4": "1", "e4": "1", "f4": "1",
            "h4": "1", "k4": "1", "l4": "1", "n4": "1", "q4": "1"})
test_mappings[h.name] = h

h = Mapping([
    "X1",
    "X2 - 1/3*X1^3 - h2*X1*X3**2 - q2*X3**3",
    "X3",
    "X4 - X1**2 - h4*X1*X3**2 - q4*X3**3"
],
    name="H2",
    params={"h2": "1", "q2": "1", "h4": "1", "q4": "1"},
    r=3)
test_mappings[h.name] = h

h = Mapping([
    "X1",
    "X2 - 1/3*X1^3 - c1*X1^2*X4 + 3*c1*X1*X2*X3 - (16*q4*c1^2-r4^2)/48/c1^2*X1*X3^2" +
    "- 1/2*r4*X1*X3*X4 + 3/4*r4*X2*X3^2 - r4*q4/12/c1*X3^3 - r4^2/16/c1*X3^2*X4",
    "X3",
    "X4 -X1^2*X3 + r4/4/c1*X1*X3^2 - 3*c1*X1*X3*X4 + 9*c1*X2*X3^2 - q4*X3^3 - 3/4*r4*X3^2*X4"
],
    name="H3",
    params={"c1": "1", "q4": "1", "r4": "1"},
    r=48,
    primes=[3, 5, 7, 11, 13, 17])
test_mappings[h.name] = h

h = Mapping([
    "X1",
    "X2 - 1/3*X1^3",
    "X3 - X1^2*X2 - e3*X1*X2^2 -k3*X2^3",
    "X4 - e4*X1*X2^2 - k4*X2^3"
],
    name="H4",
    params={"e3": "1", "k3": "1", "e4": "1", "k4": "1"},
    r=3,
    primes=[3, 5, 7, 11, 13])
test_mappings[h.name] = h

h = Mapping([
    "X1",
    "X2 - 1/3*X1^3 + i3*X1*X2*X4 - j2*X1*X4^2 + s3*X2*X4^2 + i3^2*X3*X4^2 - t2*X4^3",
    "X3 - X1^2*X2 - 2*s3/i3*X1*X2*X4 - i3*X1*X3*X4 - j3*X1*X4^2 - s3^2/i3^2*X2*X4^2 - s3*X3*X4^2 - t3*X4^3",
    "X4"
],
    name="H5",
    params={"i3": "1", "j2": "1", "s3": "1", "t2": "1", "t3": "1", "j3": "1"},
    r=3,
    primes=[3, 5, 7, 11, 13])
test_mappings[h.name] = h

h = Mapping([
    "X1",
    "X2 - 1/3*X1^3 - j2*X1*X4^2 - t2*X4^3",
    "X3 - X1^2*X2 - e3*X1*X2^2 - g3*X1*X2*X4 - j3*X1*X4^2 - k3*X2^3 - m3*X2^2*X4",
    "X4"
],
    name="H6",
    params={"j2": "1", "t2": "1", "e3": "1", "g3": "1", "j3": "1", "k3": "1", "m3": "1"},
    r=3,
    primes=[5, 7, 11, 13, 17])
test_mappings[h.name] = h

h = Mapping([
    "X1",
    "X2-(1/3)*X1^3",
    "-X1*X2^2*e3-X2^3*k3-X1^2*X2+X3",
    "-X1*X2^2*e4-X1*X2*X3*f4-X1*X3^2*h4-X2^3*k4-X2^2*X3*l4-X2*X3^2*n4-X3^3*q4-X1^2*X3+X4"
],
    name="H7",
    params={"e3": "1", "k3": "1", "e4": "1", "f4": "1", "h4": "1", "k4": "1", "l4": "1", "n4": "1", "q4": "1"},
    r=3,
    primes=[5, 7, 11, 13, 17, 23, 29, 31, 37])
test_mappings[h.name] = h

h = Mapping([
    "X1",
    "X2-(1/3)*X1^3",
    "X2^2*X4*g4^2-X1*X2^2*e3+X1*X2*X3*g4-X2^3*k3+X2^2*X3*m4-X1^2*X2+X3",
    "X4-X1^2*X3-e4*X1*X2^2-2*m4*X1*X2*X3/g4-g4*X1*X2*X4-k4*X2^3-m4^2*X2^2*X3/g4^2-m4*X2^2*X4"
],
    name="H8",
    params={"g4": "1", "e3": "1", "k3": "1", "m4": "1", "e4": "1", "k4": "1"},
    r=3,
    primes=[5, 7, 11, 13, 17, 19, 23])
test_mappings[h.name] = h

def verify(debug=False):
    for al in algorithms:
        for method in methods[al]:
            if debug:
                print(f"{al}({method})")
            for mapping in test_mappings:
                t = algorithms[al](test_mappings[mapping], False, True, method)
                if debug:
                    print(f"{mapping}: {t}")


if __name__ == '__main__':
    verify(True)
