#!/usr/bin/python
from PayLoader import PayLoader

def main():
	pay = PayLoader()

	pay.read()
	pay.print()
	pay.vote()


if (__name__ == '__main__'):
	main()