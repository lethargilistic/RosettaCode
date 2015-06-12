'''Scrapes the Draft Rosetta Code Tasks for tasks without solutions in input programming language.'''
__author__ = 'Mike'
from urllib.request import *
import re

BASE_URL = "http://rosettacode.org"

def collectLinks(arts, extension):
    category_url = BASE_URL + extension
    request = Request(category_url, headers={"User-Agent" : "Magic Browser"}) #Spoofing as a browser
    response = urlopen(request)
    html = response.read().decode("utf-8") #decode bytes to a string

    #Collect links to the articles
    p = re.compile('<li><a href="(/wiki/(?:\w|_)+)"')
    arts.extend(re.findall(p, html))

def filterProblems(arts, lang):

    print("Eliminating tasks with", lang, "solutions...")
    t = len(arts)
    no_lang_sols = []
    for extension in arts:
        print(t)
        t -= 1
        art_url = BASE_URL + extension
        request = Request(art_url, headers={"User-Agent" : "Magic Browser"}) #Spoofing as a browser
        response = urlopen(request)

        art_html = response.read().decode("utf-8")
        if art_html.find('title="Edit section: ' + lang + '">') == -1:
            no_lang_sols.append(extension)

    return no_lang_sols


def outputResults(results, lang):
    print()
    print("There are", len(results), "tasks without Python solutions.")
    for art in results:
        print("    " + art.replace("_", " ")[6:] + "    (" + BASE_URL+art + ")")

    with open(lang + "Problems.txt", "w") as f:
        f.write("There are " + str(len(results)) + " tasks without Python solutions.\\n")
        for art in results:
            f.write("    " + art.replace("_", " ")[6:] + "    (" + BASE_URL+art + ")\\n")


def main():
    articles = []
    print("Collecting all official tasks...")
    collectLinks(articles, "/wiki/Category:Programming_Tasks")
    print("Collecting all draft tasks...")
    collectLinks(articles, "/wiki/Category:Draft_Programming_Tasks")

    #Collect links that do not have solutions in lang
    lang = input("What language do you want to contribute with? (exact spelling) ")

    results = filterProblems(articles, lang)

    outputResults(results, lang)

main()
