'''Draws a pentagram with different colored lines, fill, and background (http://rosettacode.org/wiki/Pentagram#Python)'''
__author__ = 'Mike'
import turtle

t = turtle.Turtle()
t.color("red", "blue")
t.begin_fill()
for i in range(0, 5):
    t.forward(200)
    t.right(144)
t.end_fill()
