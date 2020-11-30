from tkinter import *
from elasticsearch import Elasticsearch

master = Tk() 
master.title('Elasticsearch Interface')
master.geometry('800x600') 

def elasticsearch(query):
    result = ''
    es = Elasticsearch()
    res = es.search(
        index="novels",
        body={
            "_source": [
                "title",
                "author",
                "year",
                "origin",
                "genre",
                "keywords",
                "url"
            ],
            "query": {
                "multi_match": {
                    "query": query,
                    "fuzziness": "auto",
                    "fuzzy_transpositions": "true",
                    "slop": "5",
                    "fields": ["title", "author", "genre", "keywords", "origin", "story"]
                }
            }
        })
    result = ('Found %d Results:' % res['hits']['total']['value']) + '\n'
    for hit in res['hits']['hits']:
        hit['_source']['keywords'] = str(hit['_source']['keywords'])
        hit['_source']['keywords'] = hit['_source']['keywords'].replace('[','')
        hit['_source']['keywords'] = hit['_source']['keywords'].replace(']','')
        hit['_source']['keywords'] = hit['_source']['keywords'].replace('\'','')
        
        result += '\nScore: ' + str(hit['_score'])
        result += ("\nTitle: %(title)s\nAuthor: %(author)s\nYear: %(year)s\nOrigin: %(origin)s\nGenre: %(genre)s\nKeywords: %(keywords)s\nURL: %(url)s\n" % hit["_source"])
        # result += ("\nTitle: %(title)s\nAuthor: %(author)s\nYear: %(year)s\nOrigin: %(origin)s\nGenre: %(genre)s\nURL: %(url)s\n" % hit["_source"])
    return result

def showSearchResults():
    # message.set('')
    query = query_text.get()
    result = elasticsearch(query)
    results_label.delete('1.0', END)
    results_label.insert(END, result)
  
# label widget 
search_label = Label(master, text = "Keyword: ") 
search_label.place(relx = 0.23, y = 12, anchor = NW) 

# text widget 
query = StringVar()
query_text = Entry(master, textvariable=query, width = 50) 
query_text.place(relx = 0.5, y = 5, rely = 0.028, anchor = CENTER)

# button widget 
search_button = Button(master, text = "Search", command = showSearchResults) 
search_button.place(relx = 0.77, y = 9, anchor = NE)


results = StringVar()
results_label = Text(master, width = 80, height = 30)
results.set('Results will be shown here.')
results_label.place(relx = 0.5, rely = 0.5, anchor = CENTER)

scrollbar = Scrollbar(master)
scrollbar.pack(side=RIGHT, fill=Y)
results_label.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=results_label.yview)

master.mainloop() 