import os
import sys

print()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'../game')))

print(sys.path)
