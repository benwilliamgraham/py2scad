# py2scad

## Objects
Objects are the base class for all 2D and 3D shapes in py2scad.

### Square
A square/rectangular 2D object.

Parameters:
* size:

    A single numeric value `l` for an `l`x`l` square.

    A list/tuple of two numeric values `x`, `y` for an `x`x`y` rectangle.

* centered:

    `False` to start in first quadrant. (default)

    `True` to center at the origin.

Usage:
```python
# makes a 10x10 square in the first quadrant
Square(10)
Square(size=10, centered=False)

# makes a 10x20 square centered at the origin
Square([10, 20], centered=True)
Square(size=[10, 20], centered=True)
```

### Circle
A centered, 2D object.

Parameters:
* radius: A single numeric value desribing the circle's radius.

* sides: A single integer value for the number of sides of the circle. (defualt `12`)

Usage:
```python
# makes 12-sided circle of radius 2
Circle(2)
Circle(radius=2, sides=12)
# makes 24-sided circle of radius 4
Circle(4, sides=24)
Circle(radius=4, sides=24)
```

### Polygon
A custom, multi-sided 2D object.

Parameters:

* points: A list of `x, y` lists or tuples describing a polygon

Usage:
```python
# makes a 10x10 rhombus
Polygon([(0, 0), (8, 0), (10, 10), (2, 10)])
Polygon(points=[(0, 0), (8, 0), (10, 10), (2, 10)])
```

### Text
Custom 2D text.

Parameters:
* text: A string of the text to generate.
* size: A numeric value of size of the font. (default `10`)
* font: A string of the font to be used. (default `None`)
* spacing: A numeric value describing the spacing between letters. (default `1`)

Usage:
```python
# makes the text "Hello" with size 10
Text("Hello")
Text(text="Hello", size=10)
# makes the text "Hello" with size 20 and double spacing
Text("Hello", size=20, spacing=2)
Text(text="Hello", size=20, spacing=2)
```

### Cube

## Transformations

## Combining Objects

## Using Models

## Examples

### Phone stand
A simple phone stand.

OpenSCAD:
```
difference(){
    union(){
        // side bars
        translate([0, 1, 0]) {
            cube([1, 2.5, 3]);
            translate([2, 0, 0]) cube([1, 2.5, 3]);
        };
        // front bar
        cube([3, 1, 1.25]);
    };

    // cut angle
    translate([0, 0.5, 1]) rotate([-10, 0, 0]) cube([3, 0.5, 2.5]);
    // remove slot
    translate([0, 0.5, 1]) cube([3, 0.5, 1]);
};
```

Python:
```python
from py2scad import *

frame = union([
    # side bars
    group([
        Cube([1, 2.5, 3]),
        Cube([1, 2.5, 3]).translate(x=2),
    ]).translate(y=1),
    # front bar
    Cube([3, 1, 1.25]),
])

slot = group([
    # cut angle
    Cube([3, 0.5, 2.5]).rotate(x=-10).translate(0, 0.5, 1),
    # remove slot
    Cube([3, 0.5, 1]).translate(0, 0.5, 1),
])

model = difference(frame, slot)

export_and_render(model)
```

### Exponentially-expanding blocks
10 cubes, with the distances between them spaced by twice as much each time.

OpenSCAD:
```
module spaced_cube(space, num) {
    translate([space, 0, 0]) cube();
    if (num < 10) {
        spaced_cube(space * 2, num + 1);
    }
}

spaced_cube(1, 0);
```

Python:
```python
from py2scad import *

model = group()
space = 1
for _ in range(10):
    model.add(Cube().translate(x=space))
    space *= 2

export_and_render(model)
```
