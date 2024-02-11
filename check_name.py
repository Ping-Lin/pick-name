#!/usr/bin/env python3

'''
check_name.py is an easy tool for checking good name.

'''

from goodname import GoodName


def main():
    name = GoodName("林大明")

    # example
    print(name)
    print(f"is good name: {name.is_good_name()}")


if __name__ == "__main__":
    main()
