#!/usr/bin/python3
from Reddit import Reddit
import sys

def main():
	argc = len(sys.argv)

	r = Reddit()

	r.set_choise(["[up]","[dw]","[no]"])
	r.set_bot("bot4")
	r.set_sub("all")

	if ( argc > 1 and sys.argv[1] == "list"):
		r.read()
		r.list()  # to see results

	else:
		r.collect()  # endless loop


if (__name__ == '__main__'):
	main()
