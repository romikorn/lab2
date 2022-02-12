import csv
import re

read_genre = input('Какой жанр игры вас интересует?\n')
read_category = input('Какая категория игры вас интересует?\n')
read_developer = input('Игры какого разработчика вас интересуют?\n')
read_platform = input('На какой операционной системе вы хотите играть?\n')
read_year = input('Игры какого года выхода вас интересуют? (можете ввести промежуток, например 1999-2005)\n')
read_cost = input('Какая цена игры вам предпочтительна (можете использовать <, например <100)\n')
read_rating = input('Положительных оценок игр обязательно должно быть больше отрицательных? (Введите ~+да+~ или ~+нет+~) \n').lower()

norm_genre = list([genre.lstrip().capitalize() for genre in read_genre.split(',')])
norm_category = list([category.lstrip().title() for category in read_category.split(',')])
norm_developer = list([developer.lstrip().title() for developer in read_developer.split(',')])
norm_platform = list([platform.lstrip().lower() for platform in read_platform.split(',')])


def genre_correct(steam_data):
    return (norm_genre == ['']) or any(genre in steam_data for genre in norm_genre)


def category_correct(steam_data):
    return (norm_category == ['']) or any(category in steam_data for category in norm_category)


def developer_correct(steam_data):
    return (norm_developer == ['']) or any(developer in steam_data for developer in norm_developer)


def platform_correct(steam_data):
    return (norm_platform == ['']) or any(platform in steam_data for platform in norm_platform)


def year_correct(steam_data, year=read_year):
    if '-' in year:
        year_in = year.split('-')
        return year_in[0] <= steam_data <= year_in[1]
    else:
        return (steam_data == year) or (year == '')


def cost_correct(steam_data, cost=read_cost):
    if cost == '':
        return 1
    elif cost[0] == '<':
        c = float(re.findall(r'[\d.]+', cost)[0])
        return 0.0 <= steam_data <= c
    else:
        return cost == steam_data


def rating_correct(steam_data):
    return ((read_rating == 'да') and (steam_data[0] > steam_data[1])) or (read_rating == '') or (read_rating == 'нет')


with open('steam.csv', encoding='utf-8') as file, \
        open('result.txt', 'w', encoding='utf-8') as file1:
    data = csv.reader(file)
    for str in data:
        if str[0] == 'appid':
            continue
        genre_steam = str[9].split(';') and str[10].split(';')
        category_steam = str[8].split(';')
        developer_steam = str[4].split(';')
        platform_steam = str[6].split(';')
        year_steam = str[2].split('-')[0]
        cost_steam = float(str[17])
        rating_steam = [int(str[12]), int(str[13])]

        if (genre_correct(genre_steam) and
            category_correct(category_steam) and
            developer_correct(developer_steam) and
            platform_correct(platform_steam) and
            year_correct(year_steam) and
            cost_correct(cost_steam) and
            rating_correct(rating_steam)):
            file1.write(str[1] + '\n')
