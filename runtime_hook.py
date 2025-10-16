import PyInstaller.hooks.rthooks.pyi_rth_multiprocessing

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
