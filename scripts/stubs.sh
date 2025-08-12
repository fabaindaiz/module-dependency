#! /bin/bash
stubgen src/dependency -o stubs/dependency --include-docstrings
stubgen src/library -o stubs/library --include-docstrings