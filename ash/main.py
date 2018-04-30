#!/usr/bin/env python

"""
Main loop for the application
"""

from ash import Ash

def main():
    ash = Ash()

    while True:
        ash.run()

if __name__ == '__main__':
    main()
