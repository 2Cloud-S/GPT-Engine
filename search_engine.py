import requests
from bs4 import BeautifulSoup
import openai

openai.api_key = 'YOUR_API_KEY_HERE'

def search(query, num_results=10):
    urls = []
    start = 0

    while len(urls) < num_results:
        url = 'https://www.google.com/search?q=' + query + '&start=' + str(start)
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        for result in soup.find_all('div', class_='r'):
            link = result.find('a')['href'][7:]
            urls.append(link)

            if len(urls) == num_results:
                break

        start += 10

    return urls

def generate_response(url):
    try:
        response = requests.get(url)
    except:
        return {'summary': 'Error: Unable to retrieve webpage content', 'chat_response': ''}

    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()

    summary = summarize(text)
    chat_response = chat(summary)

    return {'summary': summary, 'chat_response': chat_response}

def summarize(text):
    try:
        response = openai.Completion.create(
          engine="text-davinci-002",
          prompt="Summarize the following text:\n" + text,
          max_tokens=50,
          n=1,
          stop=None,
          temperature=0.5,
        )

        summary = response.choices[0].text.strip()
    except:
        summary = 'Error: Unable to summarize webpage content'

    return summary

def chat(prompt):
    try:
        response = openai.Completion.create(
          engine="davinci",
          prompt="Q: " + prompt + "\nA:",
          max_tokens=50,
          n=1,
          stop=None,
          temperature=0.5,
        )

        chat_response = response.choices[0].text.strip()
    except:
        chat_response = ''

    return chat_response

# User input
query = input("Enter a search query: ")
num_results = int(input("Enter the number of search results to return (default is 10): ") or 10)
results_per_page = int(input("Enter the number of results to display per page (default is 5): ") or 5)

# Perform search
urls = search(query, num_results)

# Paginate results
num_pages = (num_results + results_per_page - 1) // results_per_page
for i in range(num_pages):
    start_index = i * results_per_page
    end_index = min((i + 1) * results_per_page, num_results)
    page_urls = urls[start_index:end_index]

    # Generate response for each URL on the current page
    for url in page_urls:
        response = generate_response(url)
        print("Link:", url)
        print("Summary:", response['summary'])
        print("Chat Response:", response['chat_response'])

    print("Press Enter to view the next page...")
    input()
