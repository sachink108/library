import wikipedia

#print (wikipedia.search("Killing Floor (novel)"))

page = wikipedia.page("Killing Floor (novel)")
print (page.images)

page = wikipedia.page("Master of the Game (novel)")
print (page.images)
