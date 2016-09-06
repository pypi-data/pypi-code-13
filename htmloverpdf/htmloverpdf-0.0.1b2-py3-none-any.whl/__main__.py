import sys
from . import render

sys.stdout.buffer.write(render(sys.stdin.read()))
