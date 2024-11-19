# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WorkuaAnalyticsItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    technologies = scrapy.Field()

import csv

with open("../data.csv", encoding="utf-8") as file:
    reader = csv.reader(file)
    # Пропускаємо заголовок
    num_vacancies = sum(1 for row in reader) - 1

print(f"Кількість вакансій: {num_vacancies}")