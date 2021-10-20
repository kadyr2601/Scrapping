from django.shortcuts import render
from .models import Example
import requests


def example(request):
    if request.method == "GET":
        return render(request, 'index.html')
    elif request.method == "POST":

        #-->  Этап 1. Найти страницу компании на сайте. Через поиск на сайте либо любым другим способом. -->
        RESEARCH_QUERY = request.POST.get('query')
        url = f'https://finance.yahoo.com/quote/{RESEARCH_QUERY}'
        response = requests.get(url)

        # <-- Этап 2. На странице компании перейти на вкладку с историческими данными. -->
        s = requests.Session()
        url2 = f'{response.url}/history?p={RESEARCH_QUERY}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response2 = s.get(url2, headers=headers)

        # <-- Этап 3. Выбрать данные за максимальный период. == Этап 4. Скачать данные по ссылке “Download Data” -->
        file = f'https://query1.finance.yahoo.com/v7/finance/download/{RESEARCH_QUERY}?period1=1425545600&period2=1634688000&interval=1d&events=history&includeAdjustedClose=true'
        res = s.get(file, headers=headers)

        # <-- Этап 5. Сохранить данные из файла в базу данных. == Важное примечание: все должно происходить в автоматическом режиме.
        # Приветствуется реализация, где во время скрапинга CSV файлы не сохраняются локально. -->
        item = Example.objects.create(
            data=res.text
        )
        item.save()
    return render(request, 'index.html', {'response': response.status_code, 'response2': response2.status_code, 'res': res.text})
