"""
This module is a runtime hook for PyInstaller to support multiprocessing.
"""

import PyInstaller.hooks.rthooks.pyi_rth_multiprocessing  # pylint: disable=unused-import

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
