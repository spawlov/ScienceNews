from time import sleep

from bs4 import BeautifulSoup as Bs

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from loguru import logger

import requests

from transliterate import slugify

from ...models import Category, Post, Tag


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

            if Post.objects.filter(
                slug=slugify(post["title"], language_code="ru")
            ).exists():
                logger.info(
                    f'Post "{post["title"]}" already exists from db, skipped',
                )
                return False

            post["author"] = (
                soup.find(
                    name="div",
                    class_="title",
                )
                .find(
                    name="div",
                    class_="meta-item meta-item_author",
                )
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

            logger.info(f'Post "{post["title"]}" successfully parsed.')
            return post

    def adding_post_to_db(self):
        image_name = self.recent_post["image"].split("/")[-1]
        try:
            with requests.get(
                url=self.recent_post["image"],
                headers=self._headers,
                stream=True,
            ) as response:
                image_content = ContentFile(
                    response.content,
                    name=image_name,
                )
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
        ) as error:
            logger.error(error)
            return error

        try:
            qs_category, created_category = Category.objects.get_or_create(
                title=self.recent_post["category"],
                slug=slugify(self.recent_post["category"], language_code="ru"),
            )
        except IntegrityError as error:
            logger.error(error)
            return error

        message = "successfully created."
        if not created_category:
            message = "already exists"
        logger.info(f'Category "{qs_category.title}" {message}')

        try:
            qs_post, created_post = Post.objects.get_or_create(
                slug=slugify(self.recent_post["title"], language_code="ru"),
                title=self.recent_post["title"],
                category=qs_category,
                author=self.recent_post["author"],
                content=self.recent_post["content"],
                photo_caption=self.recent_post["image_caption"],
                defaults={"photo": image_content},
            )
        except IntegrityError as error:
            logger.error(error)
            return error

        if created_post:
            for tag in self.recent_post["tags"]:
                try:
                    qs_tag, created_tag = Tag.objects.get_or_create(
                        title=tag, slug=slugify(tag, language_code="ru")
                    )
                except IntegrityError as error:
                    logger.error(error)
                    return error

                message = "successfully created."
                if not created_tag:
                    message = "already exists"
                logger.info(f'Tag "{qs_tag.title}" {message}')
                qs_post.tag.add(qs_tag)
                logger.info(f'Created post "{self.recent_post["title"]}"')
            return True
        logger.info(f'Post "{self.recent_post["title"]}" already exists')

    def handle(self, *args, **options):
        with open("./.urls", "r") as urls_to_parsing:
            for url in urls_to_parsing:
                logger.info(f'Parsing "{url.strip()}"')
                link = self.get_recent_post_link(url.strip())
                self.recent_post = self.get_recent_post(link)
                if self.recent_post:
                    self.adding_post_to_db()
                sleep(1)
        logger.info("Finished parsing!")
