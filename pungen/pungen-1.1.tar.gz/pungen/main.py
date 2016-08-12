import argparse
import os




def main():
	args = argparse.ArgumentParser(description="Generates a Punnet Square using given arguments")

	args.add_argument("-f", "--female", nargs=2, help="Females Genes", action="store", required=True)
	args.add_argument("-m", "--male", nargs=2, help="Males Genes", action="store", required=True)


	ootput = args.parse_args()
	f_g = ootput.female
	m_g = ootput.male


	punnet = """
	       |
	{0: <6} | {m[0]: ^5} | {m[1]: ^5} |
	{1: <3} | {f[0]: ^5} | {f[1]: ^5} |
	--------------------------------------------
	{2: <6} | {m[0]: >2}{f[0]: <4}| {m[1]: >2}{f[0]: <4}|
	{2: <6} | {m[0]: >2}{f[1]: <4}| {m[1]: >2}{f[1]: <4}|


	""".format("Male >", "Female", "    ", f=f_g, m=m_g)
	print(punnet)

