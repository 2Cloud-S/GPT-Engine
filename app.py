import os
from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai

# Set OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # Get user input
    query = request.form['query']
    num_results = int(request.form.get('num_results', 10))
    results_per_page = int(request.form.get('results_per_page', 5))

    # Perform search
    urls = []
    start = 0
    while len(urls) < num_results:
        url = 'https://www.google.com/search?q=' + query + '&start=' + str(start)
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            for result in soup.find_all('div', class_='r'):
                link = result.find('a')['href'][7:]
                if link.startswith('http') or link.startswith('https'):
                    urls.append(link)
                if len(urls) == num_results:
                    break
            start += 10
        except requests.exceptions.RequestException as e:
            return jsonify({'error': 'Error: Unable to retrieve search results.'})

    # Paginate results
    num_pages = (num_results + results_per_page - 1) // results_per_page
    results = []
    for i in range(num_pages):
        start_index = i * results_per_page
        end_index = min((i + 1) * results_per_page, num_results)
        page_urls = urls[start_index:end_index]

        # Generate response for each URL on the current page
        for url in page_urls:
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()
                summary = summarize(text)
                chat_response = chat(summary)
                result = {
                    'url': url,
                    'summary': summary,
                    'chat_response': chat_response
                }
                results.append(result)
            except:
                pass

    return jsonify({'results': results})

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

if __name__ == '__main__':
    app.run(debug=True)
