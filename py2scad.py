"""py2scad module.

Provides an interface for OpenSCAD in Python.
"""

import os
import tempfile


class _Object:
    """Object class.

    Virtual parent class for all primitive objects.
    """

    def __init__(self):
        self._tranfs = []

    def save_as(self, name):
        """Save self to file"""
        with tempfile.NamedTemporaryFile("w") as file:
            output = self._scad_with_tranfs()
            print(output)
            file.write(f"{output}\n")
            file.flush()
            os.system(f"openscad {file.name} -o {name}")
            file.close()

    def _scad(self):
        """Compiles object to OpenSCAD code."""

    def _scad_with_tranfs(self):
        """Compiles object to OpenSCAD code with included transformations."""
        tranfs_str = ""
        for tranf in self._tranfs:
            tranfs_str = f"{tranf._scad()}{tranfs_str}"
        return f"{tranfs_str}{self._scad()}"

    def scale(self, x=1, y=1, z=1):
        """Scale a object."""
        if (
            (isinstance(x, int) or isinstance(x, float))
            and (isinstance(y, int) or isinstance(y, float))
            and (isinstance(z, int) or isinstance(z, float))
        ):
            self._tranfs.append(_Transformation("scale", {"v": [x, y, z]}))
        else:
            raise TypeError("`scale` expected number arguments")
        return self

    def resize(self, x, y, z):
        """Resize a object."""
        if (
            (isinstance(x, int) or isinstance(x, float))
            and (isinstance(y, int) or isinstance(y, float))
            and (isinstance(z, int) or isinstance(z, float))
        ):
            self._tranfs.append(_Transformation("scale", {"newsize": [x, y, z]}))
        else:
            raise TypeError("`resize` expected number arguments")
        return self

    def rotate(self, x=0, y=0, z=0):
        """Rotate an object."""
        if (
            (isinstance(x, int) or isinstance(x, float))
            and (isinstance(y, int) or isinstance(y, float))
            and (isinstance(z, int) or isinstance(z, float))
        ):
            self._tranfs.append(_Transformation("rotate", {"a": [x, y, z]}))
        else:
            raise TypeError("`translate` expected number angle arguments")
        return self

    def translate(self, x=0, y=0, z=0):
        """Translate an object."""
        if (
            (isinstance(x, int) or isinstance(x, float))
            and (isinstance(y, int) or isinstance(y, float))
            and (isinstance(z, int) or isinstance(z, float))
        ):
            self._tranfs.append(_Transformation("translate", {"v": [x, y, z]}))
        else:
            raise TypeError("`translate` expected number arguments")
        return self


class Square(_Object):
    """Square class."""

    def __init__(self, size, centered=False):
        super().__init__()
        if isinstance(size, int) or isinstance(size, float):
            self.size = [size, size]
        elif (
            (isinstance(size, list) or isinstance(size, tuple))
            and len(size) == 2
            and (isinstance(size[0], int) or isinstance(size[0], float))
            and (isinstance(size[1], int) or isinstance(size[1], float))
        ):
            self.size = size
        else:
            raise TypeError(
                f"`Square` expects `size` to be either a single number or a list/tuple of two numbers, "
                f"instead found: `{type(size)}`"
            )
        if isinstance(centered, bool):
            self.centered = centered
        else:
            raise TypeError(
                f"`Square` expects `centered` to be a boolean, "
                f"instead found: `{type(centered)}`"
            )

    def _scad(self):
        return (
            f"square(size={self.size}, center={'true' if self.centered else 'false'});"
        )


class Circle(_Object):
    """Circle class."""

    def __init__(self, radius, sides=12):
        super().__init__()
        if isinstance(radius, int) or isinstance(radius, float):
            self.radius = radius
        else:
            raise TypeError(
                f"`Circle` expects `radius` to be a number, "
                f"instead found: `{type(radius)}`"
            )
        if isinstance(sides, int):
            self.sides = sides
        else:
            raise TypeError(
                f"`Circle` expects `sides` to be an integer, "
                f"instead found: `{type(sides)}`"
            )

    def _scad(self):
        return f"circle(r={self.radius}, $fn={self.sides});"


class Cube(_Object):
    """Cube class."""

    def __init__(self, size, centered=False):
        super().__init__()
        if isinstance(size, int) or isinstance(size, float):
            self.size = [size, size, size]
        elif (
            (isinstance(size, list) or isinstance(size, tuple))
            and len(size) == 3
            and (isinstance(size[0], int) or isinstance(size[0], float))
            and (isinstance(size[1], int) or isinstance(size[1], float))
            and (isinstance(size[2], int) or isinstance(size[2], float))
        ):
            self.size = size
        else:
            raise TypeError(
                f"`Cube` expects `size` to be either a single number or a list/tuple of three numbers, "
                f"instead found: `{type(size)}`"
            )
        if isinstance(centered, bool):
            self.centered = centered
        else:
            raise TypeError(
                f"`Cube` expects `centered` to be a boolean, "
                f"instead found: `{type(centered)}`"
            )

    def _scad(self):
        return f"cube(size={self.size}, center={'true' if self.centered else 'false'});"


class Sphere(_Object):
    """Sphere class."""

    def __init__(self, radius, sides=12):
        super().__init__()
        if isinstance(radius, int) or isinstance(radius, float):
            self.radius = radius
        else:
            raise TypeError(
                f"`Sphere` expects `radius` to be a number, "
                f"instead found: `{type(radius)}`"
            )
        if isinstance(sides, int):
            self.sides = sides
        else:
            raise TypeError(
                f"`Sphere` expects `sides` to be an integer, "
                f"instead found: `{type(sides)}`"
            )

    def _scad(self):
        return f"sphere(r={self.radius}, $fn={self.sides});"


class Cylinder(_Object):
    """Cylinder class."""

    def __init__(self, radius, height, sides=12, centered=False):
        super().__init__()
        if isinstance(radius, int) or isinstance(radius, float):
            self.radius = [radius, radius]
        elif (
            (isinstance(radius, list) or isinstance(radius, tuple))
            and len(radius) == 2
            and (isinstance(radius[0], int) or isinstance(radius[0], float))
            and (isinstance(radius[1], int) or isinstance(radius[1], float))
        ):
            self.radius = radius
        else:
            raise TypeError(
                f"`Cylinder` expects `radius` to be a number or list/tuple of two numbers, "
                f"instead found: `{type(radius)}`"
            )
        if isinstance(height, int) or isinstance(height, float):
            self.height = height
        else:
            raise TypeError(
                f"`Cylinder` expects `height` to be a number, "
                f"instead found: `{type(height)}`"
            )
        if isinstance(sides, int):
            self.sides = sides
        else:
            raise TypeError(
                f"`Cylinder` expects `sides` to be an integer, "
                f"instead found: `{type(sides)}`"
            )
        if isinstance(centered, bool):
            self.centered = centered
        else:
            raise TypeError(
                f"`Cylinder` expects `centered` to be a boolean, "
                f"instead found: `{type(centered)}`"
            )

    def _scad(self):
        return f"cylinder(r1={self.radius[0]}, r2={self.radius[1]}, h={self.height}, center={'true' if self.centered else 'false'}, $fn={self.sides});"


class _Group(_Object):
    """Group class."""

    def __init__(self, objs):
        super().__init__()
        self.objs = objs

    def _scad(self):
        return f"{{ {' '.join([obj._scad_with_tranfs() for obj in self.objs])}}};"


class _Union(_Object):
    def __init__(self, objs):
        super().__init__()
        self.objs = objs

    def _scad(self):
        return (
            f"union() {{ {' '.join([obj._scad_with_tranfs() for obj in self.objs])}}};"
        )


class _Intersection(_Object):
    def __init__(self, objs):
        super().__init__()
        self.objs = objs

    def _scad(self):
        return f"intersection() {{ {' '.join([obj._scad_with_tranfs() for obj in self.objs])}}};"


class _Difference(_Object):
    def __init__(self, obj1, obj2):
        super().__init__()
        self.obj1 = obj1
        self.obj2 = obj2

    def _scad(self):
        return f"difference() {{ {self.obj1._scad_with_tranfs()} {self.obj2._scad_with_tranfs()} }};"


class _Transformation:
    """Transformation class.

    Describes a transformation.
    """

    def __init__(self, name, args):
        self.name = name
        self.args = args

    def _scad(self):
        """Transforms transformation to scad code."""
        return f"{self.name}({', '.join([f'{arg_name}={arg_value}' for arg_name, arg_value in self.args.items()])})"


def _all_objs(objs):
    """Insure that all objects in a list of Objects are Objects."""
    for obj in objs:
        if not isinstance(obj, _Object):
            return False
    return True


def group(*argv):
    """Group a list of objects."""
    args = list(argv)
    if not _all_objs(args):
        raise TypeError("`group` expected a list of objects")
    return _Group(args)


def union(*argv):
    """Union a list of objects."""
    args = list(argv)
    if not _all_objs(args):
        raise TypeError("`union` expected a list of objects")
    return _Union(args)


def intersection(*argv):
    """Intersect a list of objects."""
    args = list(argv)
    if not _all_objs(args):
        raise TypeError("`intersection` expected a list of objects")
    return _Intersection(args)


def difference(arg1, arg2):
    """Difference a list of objects."""
    args = [arg1, arg2]
    if not _all_objs(args):
        raise TypeError("`difference` expected two objects")
    return _Difference(arg1, arg2)
