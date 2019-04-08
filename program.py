import requests
import bs4
import collections


WeatherReport = collections.namedtuple('WeatherReport', 'cond, temp, scale, loc')

def main():
    print_the_header()

    city = input('Which Polish city do you want the weather for (eg. Warsaw)? ')

    html = get_html_from_web(city)
    report = get_weather_from_html(html)

    print('The temp in {} is {} and {}{}'.format(
        report.loc,
        report.cond,
        report.temp,
        report.scale
    ))

    get_weather_from_html(html)

    # display for the forecast


def print_the_header():
    print('--------------------------------------')
    print('            WEATHER APP')
    print('--------------------------------------')
    print()


def get_html_from_web(city):
    url = f'https://www.wunderground.com/weather/pl/{city}'
    response = requests.get(url)
    # print(response.status_code)
    # print(response.text[0:250])

    return response.text


def get_weather_from_html(html):

    # cityCss = '.region-content-header h1'
    # weatherConditionCss = 'div.condition p'
    # weatherTempCss = '.wu-value-to'
    # weatherScaleCss = '.wu-label'

    soup = bs4.BeautifulSoup(html, 'html.parser')
    loc = soup.find(class_='region-content-header').find('h1').get_text()
    condition = soup.find(class_='condition-icon').get_text()
    temp = soup.find(class_='wu-value-to').get_text()
    scale = soup.find(class_='wu-label').get_text()

    loc = cleanup_text(loc)
    loc = find_city_from_location(loc)
    condition = cleanup_text(condition)
    condition = condition.lower()
    temp = cleanup_text(temp)
    scale = cleanup_text(scale)

    # print(loc, condition, temp, scale)
    # return loc, condition, temp, scale
    report = WeatherReport(cond=condition, temp=temp, scale=scale, loc=loc)
    return report

def find_city_from_location(loc : str):
    parts = loc.split(',')
    return  parts[0].strip()


def cleanup_text(text : str):
    if not text:
        return text

    text = text.strip()
    return text

if __name__ == '__main__':
    main()
