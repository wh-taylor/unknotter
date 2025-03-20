# knot-diagram

Manipulate and analyze knot and link diagrams.

This library is written in python version 3.12.3. It is currently unstable.

## Usage

### Making Diagrams

We can construct our own diagrams via the `Diagram` class like so:

```py
trefoil_diagram = Diagram([(1, 5, 2, 4), (3, 1, 4, 6), (5, 3, 6, 2)])
```

The input of the `Diagram` constructor accepts a list of 4-tuples. This notation is known as [planar diagram notation](https://knotinfo.math.indiana.edu/descriptions/pd_notation.html). Our purpose for using this notation is that it is highly efficient in knot diagram manipulation algorithms.

We can also access reduced knot diagrams of tabulated prime knots via the `knot` function. As of now, you can access all knots up to and including 13 crossings. For knots of crossing number less than or equal to 10, we can access them like so:

```py
figure_eight_diagram = knot(4, 1)
```

When we want to get knots of crossing number, we need to specify whether or not the knot is alternating:

```py
big_knot_diagram = knot(12, 45, 'a')
```

There are also a few special unknot diagrams provided: the `THISTLETHWAITE_UNKNOT`, the `OCHIAI_UNKNOT`, and the `INFINITY_UNKNOT`.

### Manipulating and Analyzing Diagrams

Let `d` and `p` be knot diagrams, `e`, `f` and `g` edge labelings (unsigned integer), and `n` a signed integer. Note that all methods below are pure and thus do not mutate any values.

- `d.reverse()` reverses the orientation of `d`.
- `d.reflect()` switches all crossings of `d`, or reflects the knot of `d` in space.
- `d.copy()` gives a new diagram object identical to `d`.
- `d.shift(n)` shifts the edge labelings of `d` by `n`, giving an equivalent diagram.
- `d == p` checks whether two knot diagrams are equivalent up to an overpass.
- `d.is_congruent(p)` checks whether two knot diagrams are equivalent ignoring orientation.
- `d.twist(e)` twists the edge `e`, applying a positive Reidemeister I move.
- `d.twist(e, is_positive=False)` applies a negative Reidemeister I move.
- `d.poke(e, f)` pokes the edge `e` underneath the edge `f`, applying a Reidemeister II move.
- `d.slide(e, f, g)` applies a Reidemeister III move over the triangular face formed by `e`, `f` and `g`.

The following methods are intended to be implemented later:

- `d.disjoint_union(p)` forms the disjoint union link of `d` and `p`.
- `d.join(p, e, f)` joins the edge `e` of `d` with the edge `f` of `p`.
- `d.get_gauss_code()` returns the Gauss code notation of `d`.
- `d.get_dt_notation()` returns the Dowker-Thistlethwaite notation of `d`.
- `d.get_jones_polynomial()` returns the Jones polynomial of `d`.
- `d.get_alexander_polynomial()` returns the Alexander polynomial of `d`.
- `d.get_p_colorability(n)` checks whether or not `d` is `n`-colorable where `n` is prime.
