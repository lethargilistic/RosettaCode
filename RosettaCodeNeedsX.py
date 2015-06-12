'''Scrapes the Draft Rosetta Code Tasks for tasks without solutions in input programming language.'''
__author__ = 'Mike'
from urllib.request import *
import re

base_url = "http://rosettacode.org"
category_url = base_url + "/wiki/Category:Draft_Programming_Tasks"

request = Request(category_url, headers={"User-Agent" : "Magic Browser"}) #Spoofing as a browser
response = urlopen(request)

html = response.read().decode("utf-8") #decode bytes to a string

#Collect links to the articles
print("Collecting all drafts...")
p = re.compile('<li><a href="(/wiki/(?:\w|_)+)"')
articles = re.findall(p, html)

#Collect links that do not have solutions in lang
lang = input("What language do you want to contribute with? (exact spelling) ")

print("Eliminating drafts with", lang, "solutions...")
no_lang_sols = []
for extension in articles:
    art_url = base_url + extension
    request = Request(art_url, headers={"User-Agent" : "Magic Browser"}) #Spoofing as a browser
    response = urlopen(request)

    art_html = response.read().decode("utf-8")
    if art_html.find('title="Edit section: ' + lang + '">') == -1:
        no_lang_sols.append(extension)

print()
print("There are", len(no_lang_sols), "draft tasks without Python solutions.")
for art in no_lang_sols:
    print("    " + art.replace("_", " ")[6:] + "    (" + base_url+art + ")")

with open(lang + "Problems.txt", "w") as f:
    f.write("There are " + str(len(no_lang_sols)) + " draft tasks without Python solutions.\\n")
    for art in no_lang_sols:
        f.write("    " + art.replace("_", " ")[6:] + "    (" + base_url+art + ")\\n")
