'''Scrapes the Draft Rosetta Code Tasks for tasks without solutions in input programming language.'''
__author__ = 'Mike'
from urllib.request import *
import re


BASE_URL = "http://rosettacode.org"
ARTICLE_PATTERN = re.compile('<li><a href="(/wiki/(?:\w|_|/)+)"')


def readPageHTML(url_extension):
    url = BASE_URL + url_extension
    request = Request(url, headers={"User-Agent" : "Magic Browser"}) #Spoofing as a browser
    response = urlopen(request)
    html = response.read().decode("utf-8") #decode bytes to a string
    return html


def collectLinks(arts, extension):
    html = readPageHTML(extension)

    #Collect links to the articles
    arts.extend(re.findall(ARTICLE_PATTERN, html))


def filterProblems(arts, lang):
    print("Eliminating tasks with", lang, "solutions...")

    lang_html = readPageHTML("/wiki/Category:" + lang)

    #Find index in string where the link section starts
    start = lang_html.find("Pages in category")

    #Collect the links
    yes_lang_sols = set(re.findall(ARTICLE_PATTERN, lang_html[start:]))

    #Get all links that are in arts, but not in yes_lang_sols
    #These are the problems for which there is no solution in the language
    no_lang_sols = list(arts.difference(yes_lang_sols))

    #Sort list in alphabetical order
    no_lang_sols.sort()

    return no_lang_sols


def outputResults(results, lang):
    with open(lang + "Problems.txt", "w") as f:
        print("\nThere are", len(results), "tasks without Python solutions.")
        f.write("There are " + str(len(results)) + " tasks without Python solutions.\n")

        for art in results:
            art_cleaned = art.replace("_", " ")[6:] #Cuts of /wiki/ and replaces any _ in the link with space
            print("    " + art_cleaned + "    (" + BASE_URL+art + ")")
            f.write("    " + art_cleaned + "    (" + BASE_URL+art + ")\n")


def main():
    #Extend a list with all tasks on RosettaCode
    articles = []
    print("Collecting all official tasks...")
    collectLinks(articles, "/wiki/Category:Programming_Tasks")
    print("Collecting all draft tasks...")
    collectLinks(articles, "/wiki/Category:Draft_Programming_Tasks")

    #Convert that list into a set. (Can't extend a set, so a list was used for initial populating)
    articles = set(articles)

    #Do the filtering for a language
    lang = input("What language do you want to contribute with? (exact spelling) ")
    results = filterProblems(articles, lang)

    #Output the results
    outputResults(results, lang)


main()
