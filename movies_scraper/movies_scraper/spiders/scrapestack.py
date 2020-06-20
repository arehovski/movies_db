import requests

params = {
  'access_key': '2105f22f98d48cf26c40ce23db1ec3bf',
  'url': 'https://www.kinopoisk.ru/lists/top250/'
}

api_result = requests.get('http://api.scrapestack.com/scrape', params)
website_content = api_result.content

print(website_content)