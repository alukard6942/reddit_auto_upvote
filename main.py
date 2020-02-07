#!/usr/bin/python
from PayLoader import PayLoader
from PayCheck import PayCheck

def main():
	load = PayLoader()
	check = PayCheck()

	load.config["choises"] = ["[up]","[dw]", "[dw]"]
	load.config["bot"] = "bot3"
	load.config["subreddit"] = "memes"

	load.vote()  # endless loop

	check.read()
	check.list()  # to see results


if (__name__ == '__main__'):
	main()