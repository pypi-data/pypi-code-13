import argparse

description="""
    Toy program to search inverted index and print out each line the term appears

"""
parser = argparse.ArgumentParser(description=description)
mainfile = parser.add_argument("mainfile",
type=argparse.FileType(),help="""Text file to be indexed""",)
term = parser.add_argument("term",
type=str,help="""Term for search""",)
args = parser.parse_args()