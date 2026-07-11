import sys
import os

# Source code uses bare `from utilities.X import ...` imports designed to run
# with venmo_scheduler/ as the working directory. Add it to sys.path so tests
# resolve those imports without changing the source.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "venmo_scheduler"))
