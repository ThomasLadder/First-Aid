from googleapiclient.discovery import build
import webbrowser

my_api_key = "AIzaSyACfZkvziR4L-cfgxcc2y_Hy_qJ8hjbEHw"
my_cse_id = "002135429410221340072:xdlir80yci8"

#Returns JSON for standard google search. Helper for whatQuestions().
def whatQuestions_helper(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

#Opens first google link. Call whatQuestions() for questions that start with "What".
def whatQuestions(query):
    results = whatQuestions_helper(
    query, my_api_key, my_cse_id, num=10)
    firstResult = results[0]
    search = firstResult["formattedUrl"]
    webbrowser.open(search, new=1)

#Returns JSON for standard google image search. Helper for whereQuestions().
def whereQuestions_helper(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, searchType="image", **kwargs).execute()
    return res['items']

#Opens first google image. Call whereQuestions() for questions that start with "Where".
def whereQuestions(query):
    imageResults = whereQuestions_helper(
    query, my_api_key, my_cse_id, num=10)
    firstImagesResult = imageResults[0]
    image = firstImagesResult["link"]
    webbrowser.open(image, new=1)


if __name__ == '__main__':
    whereQuestions("Where is the fibula?")

#if __name__ == '__main__':
#    whatQuestions("What is the fibula?")