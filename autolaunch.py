"""
Auto-launch script — runs every test inside the regression suite directory.

Usage:
    python autolaunch.py
"""

import subprocess
import sys

SUITE_DIR = "regression_suite"

if __name__ == "__main__":
    cmd = [
        sys.executable, "-m", "pytest",
        SUITE_DIR,
        "-v",
    ]
    print(f"Running: {' '.join(cmd)}\n")
    sys.exit(subprocess.call(cmd))
