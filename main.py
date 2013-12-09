#! /usr/bin/python3

# Grab Address and Info and convert to CSV File for given dates

from api import BLKAPI

test = BLKAPI()
test.initiallogic()
# print (test.blktrans)

test.writetocsv("test.csv")
