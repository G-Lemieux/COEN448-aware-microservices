import os

# Set the path to the source code
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
SOURCE_PATH = os.path.join(ROOT_PATH, "../src/")
os.chdir(SOURCE_PATH)

def test() -> None:
    assert(True)

