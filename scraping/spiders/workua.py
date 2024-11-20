import scrapy
import csv
from scraping.config import technologies


class WorkuaSpider(scrapy.Spider):
    name = "workua"
    allowed_domains = ["work.ua"]
    start_urls = ["https://www.work.ua/jobs-python/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Open the CSV file in append mode and initialize writer
        self.file = open("data.csv", mode="w", newline="", encoding="utf-8")
        self.writer = csv.DictWriter(self.file, fieldnames=["title", "description", "technologies"])
        self.writer.writeheader()  # Write the CSV header

    def parse(self, response):
        job_links = response.css("div.card-hover h2 a::attr(href)").getall()
        for link in job_links:
            yield response.follow(link, callback=self.parse_job)

        next_page = response.css("ul.pagination li a:contains('Наступна')::attr(href)").get()
        if next_page:
            self.logger.info(f"Moving to the next page: {next_page}")
            yield response.follow(next_page, callback=self.parse)
        else:
            self.logger.info("No more pages to process.")

    def parse_job(self, response):
        title = response.css("h1::text").get()
        description = response.css("div#job-description *::text").getall()
        if description:
            description = " ".join(description).replace('"', '').strip()
        else:
            description = "No description available"

        tech_mentions = [tech for tech in technologies if tech.lower() in description.lower()]

        self.logger.info(f"Title: {title}")
        self.logger.info(f"Technologies: {tech_mentions}")

        if tech_mentions:
            self.writer.writerow({
                "title": title.strip() if title else "No title found",
                "description": description,
                "technologies": ", ".join(tech_mentions),
            })

    def close_spider(self, spider):
        self.file.close()
        self.logger.info("CSV file has been saved and closed.")
# scrapy crawl workua
