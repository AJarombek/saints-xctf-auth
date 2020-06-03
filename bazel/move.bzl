"""
Sample Bazel macros.
Author: Andrew Jarombek
Date: 6/3/2020
"""

def move_file(name, src, dest):
    """
    Create a macro which moves a file from the source code to the Bazel out directory.
    """
    native.genrule(
        name = name,
        srcs = [src],
        outs = [dest],
        output_to_bindir = 1,
        cmd = "mv $< $@"
    )