"""
Compatibility launcher. The application now lives in the maromarker
package; use "python -m maromarker" or the maromarker console script.
This file keeps existing run configurations working.
"""
from maromarker.app import main

if __name__ == "__main__":
    main()
