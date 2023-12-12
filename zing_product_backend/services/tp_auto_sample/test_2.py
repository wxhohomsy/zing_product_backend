from .test_1 import foo


if __name__ == '__main__':
    import sys
    from pathlib import Path

    # Adjust the path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    foo()