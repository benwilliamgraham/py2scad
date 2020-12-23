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
Coming soon.

### Text
Coming soon.

### Cube
A cube/rectangular prism 3D object.

Parameters:
* size:

    A single numeric value `l` for an `l`x`l`x`l` cube.

    A list/tuple of three numeric values `x`, `y`, `z` for an `x`x`y`x`z` rectangular prism.

* centered:

    `False` to start in first quadrant. (default)

    `True` to center at the origin.

Usage:
```python
# makes a 10x10x10 cube in the first quadrant
Cube(10)
Cube(size=[10, 10, 10], centered=False)
# makes a 10x20x30 rectangular prism centered at the origin
Cube([10, 20, 30], centered=True)
Cube(size=[10, 20, 30], centered=True)
```

### Sphere
A centered, 3D object.

Parameters:
* radius: A single numeric value desribing the sphere's radius.

* sides: A single integer value for the number of sides of the sphere. (defualt `12`)

Usage:
```python
# makes 12-sided sphere of radius 2
Sphere(2)
Sphere(radius=2, sides=12)
# makes 24-sided sphere of radius 4
Sphere(4, sides=24)
Sphere(radius=4, sides=24)
```

### Cylinder
A centered 3D object.

Parameters:
* radius:

    A single numeric value desribing the cylinder's radius.

    Two numeric values desribing the cylinder's top and bottom radii.

* height: A single numeric value desribing the cylinder's height.
* sides: A single numeric value for the number of sides of the cylinder. (default `12`)
* centered: If the cylinder is centered in the z axis or not. (default `False`)

Usage:
```python
# makes a 12-sided cylinder with radius 2 and height 4
Cylinder(2, 4)
Cylinder(radius=2, height=4, sides=12, centered=False)
# makes a centered 24-sided cylinder with bottom radius 3, top radius 5, and height 8
Cylinder([3, 5], 8, sides=24, centered=True)
Cylinder(radius=[3, 5], height=8, sides=24, centered=True)
```

### Polyhedron
Coming soon.

## Transformations

Transformations modify an existing object, returning the updated value.
The following transformations apply to all Objects in the format `<object>.<transformation>(<arguments>)`.

### scale
Scale Object by given vector.

Parameters:
* x (default: `1`)
* y (default: `1`)
* z (default: `1`)

Usage (given Object `obj`):
```python
# scales x by 10
obj.scale(x=10)
obj.scale(10, 1, 1)
```

### 
Resize Object to given vector.

Parameters:
* x
* y
* z

Usage (given Object `obj`):
```python
# resizes object to 10x20x30
obj.resize(10, 20, 30)
```

### rotate
Rotate an object a given number of degrees around the origin.

Parameters:
* x (default: `0`)
* y (default: `0`)
* z (default: `0`)

Usage (given Object `obj`):
```python
# rotate 10 degrees in the z direction
obj.rotate(z=10)
obj.rotate(10, 0, 0)
```

### translate
Translate an object by a given vector.

Parameters:
* x (default: `0`)
* y (default: `0`)
* z (default: `0`)

Usage (given Object `obj`):
```python
# translate 10 in the z direction
obj.translate(0, 0, 10)
obj.translate(z=10)
# translate by `[1, 2, 3]`
obj.translate(1, 2, 3)
```

## Combining Objects

Given a list of objects, combine them together to form a new object.

### group
Create a grouping of a list of objects, leaving the inner objects separate.

Usage (given Objects `obj1, obj2, obj3`)
```python
group(obj1, obj2, obj3)
```

### union
Create a union of a list of objects.

Usage (given Objects `obj1, obj2, obj3`)
```python
union(obj1, obj2, obj3)
```

### intersection
Create an intersection of a list of objects.

Usage (given Objects `obj1, obj2, obj3`)
```python
intersection(obj1, obj2, obj3)
```

### difference
Take the difference between two objects.

Usage (given Objects `obj1, obj2`)
```python
difference(obj1, obj2)
```

### minkowski
Take the minkowski sum of a list of objects.

Usage (given Objects `obj1, obj2, obj3`)
```python
minkowski(obj1, obj2, obj3)
```

### hull
Take the convex hull of a list of objects.

Usage (given Objects `obj1, obj2, obj3`)
```python
hull(obj1, obj2, obj3)
```

## Using Models

Once a model is created, it can be exported using the following:

### save_as
Save a model under a given filename.

Usage (given Object `obj`):
```python
# save model to `model.scad`
obj.save_as("model.stl")
```

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

frame = union(
    # side bars
    group(
        Cube([1, 2.5, 3]),
        Cube([1, 2.5, 3]).translate(x=2)
    ).translate(y=1),
    # front bar
    Cube([3, 1, 1.25]),
)

slot = group(
    # cut angle
    Cube([3, 0.5, 2.5]).rotate(x=-10),
    # remove slot
    Cube([3, 0.5, 1]),
).translate(0, 0.5, 1)

difference(frame, slot).save_as("model.stl")
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
    model = group(model, (Cube().translate(x=space)))
    space *= 2

model.save_as("model.stl")
```
