#!/usr/bin/python3
from Reddit import Reddit

def main():
	r = Reddit()
	
	r.set_choise(["[up]","[dw]", "[dw]"])
	r.set_bot("bot3")
	r.set_sub("memes")

	# r.collect()  # endless loop

	r.read()
	r.list()  # to see results


if (__name__ == '__main__'):
	main()