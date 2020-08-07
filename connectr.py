# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 20:18:14 2020

@author: ASUS
"""


import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="omr"
)
mycursor = mydb.cursor()

std_roll=11
acq_marks=40
sql = "INSERT INTO Marks (roll, mark) VALUES (%s,%s)"
val=(int(std_roll),int(acq_marks))

mycursor.execute(sql,val)

mydb.commit()