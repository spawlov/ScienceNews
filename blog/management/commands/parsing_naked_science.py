from bs4 import BeautifulSoup as Bs

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from loguru import logger

import requests

from transliterate import slugify

from ...models import Category, Post, Tag


# from icecream import ic


class Command(BaseCommand):
    _headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/39.0.2171.95 Safari/537.36"
    }

    def __init__(self):
        super().__init__()
        self.recent_post = {}

    def get_recent_post_link(self, url):
        try:
            with requests.get(url=url, headers=self._headers) as response:
                soup = Bs(response.text, features="lxml")
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
        ) as error:
            logger.error(error)
            return {"error": error}
        else:
            href = (
                soup.find(
                    name="div",
                    class_="news-item-title",
                )
                .find(
                    name="a",
                    class_="animate-custom",
                )
                .get("href")
            )

            return href

    def get_recent_post(self, url):
        try:
            with requests.get(url=url, headers=self._headers) as response:
                soup = Bs(response.text, features="lxml")
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
        ) as error:
            logger.error(error)
            return error
        else:
            post = {}
            content = []

            post["title"] = (
                soup.find(
                    name="div",
                    class_="post-title",
                )
                .find(name="h1")
                .text.strip()
            )

            post["category"] = (
                soup.find(
                    name="div",
                    class_="terms-item terms-item--cat",
                )
                .find("a")
                .text.strip()
            )

            paragraph = (
                soup.find(
                    name="div",
                    class_="post-lead",
                )
                .find("p")
                .text.strip()
            )
            content.append(f"<p>{paragraph}</p>")
            post_body = soup.find(name="div", class_="body").find_all("p")
            for paragraph in post_body:
                content.append(f"<p>{paragraph.text.strip()}</p>")
            post["content"] = "".join(content)

            post["image"] = "https:" + soup.find(
                name="div",
                class_="post-image-inner",
            ).find("img").get("src")

            post["image_caption"] = (
                soup.find(
                    name="div",
                    class_="post-image-inner",
                )
                .find("figcaption")
                .text.strip()
            )

            tags_raw = soup.find(
                name="div",
                class_="terms-items grid",
            ).find_all(
                name="a",
                class_="animate-custom",
            )
            post["tags"] = []
            for _ in range(1, len(tags_raw)):
                post["tags"].append(" ".join(tags_raw[_].text.split()[1:]))

            return post

    def adding_post_to_db(self):
        image_name = self.recent_post["image"].split("/")[-1]
        image_content = ContentFile(
            requests.get(
                url=self.recent_post["image"],
                headers=self._headers,
                stream=True,
            ).content,
            name=image_name,
        )

        qs_category, created_category = Category.objects.get_or_create(
            title=self.recent_post["category"],
            slug=slugify(self.recent_post["category"], language_code="ru"),
        )

        qs_post, created_post = Post.objects.get_or_create(
            slug=slugify(self.recent_post["title"], language_code="ru"),
            title=self.recent_post["title"],
            category=qs_category,
            author="Parser",
            content=self.recent_post["content"],
            photo_caption=self.recent_post["image_caption"],
            defaults={"photo": image_content},
        )

        if created_post:
            for tag in self.recent_post["tags"]:
                qs_tag, created_tag = Tag.objects.get_or_create(
                    title=tag, slug=slugify(tag, language_code="ru")
                )
                qs_post.tag.add(qs_tag)
            logger.info(f'Created post "{self.recent_post["title"]}"')
            return
        logger.error(f'Post "{self.recent_post["title"]}" already exists')

    def add_arguments(self, parser):
        parser.add_argument("url", action="store")

    def handle(self, *args, **options):
        link = self.get_recent_post_link(options.get("url"))
        self.recent_post = self.get_recent_post(link)
        logger.info(f'Post "{self.recent_post["title"]}" successfully parsed.')
        self.adding_post_to_db()
