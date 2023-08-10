#!/usr/bin/env python3

# SPDX-License-Identifier: Unlicense

import requests
from bs4 import BeautifulSoup
import csv
import re
import sys


def generate_filename(base_url, article_id):
    sanitized_url = re.sub(
        r"[^\w]", "_", base_url
    )  # Replace non-word characters with underscores
    return f"{sanitized_url}_article_{article_id}"


def fetch_comments_for_article(base_url, article_id, max_forums):
    step = 20
    all_comments = []

    for i in range(0, max_forums + 1, step):
        params = {"page": "article", "id_article": article_id, "debut_forums": i}

        print(
            f"Fetching {requests.compat.urljoin(base_url, '?')}page={params['page']}&id_article={params['id_article']}&debut_forums={params['debut_forums']}"
        )

        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.text, "html.parser")
        doc_title = soup.find("h1", class_="titre-article").get_text(strip=True)
        doc_text = soup.find("div", class_="texte-article").find("p")

        comments_section = soup.find("ul", class_="forum-total")

        if comments_section:
            for li in comments_section.find_all("li"):
                title = li.find("div", class_="titresujet").text.strip()
                content = li.find("div", class_="textesujet").find("p").text.strip()
                all_comments.append((title, content))

    return doc_title, doc_text, all_comments


def export_to_csv(data, filename="comments.csv"):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Title", "Content"])
        writer.writerows(data)


def export_to_html(
    doc_title, doc_text, data, filename="comments.html", comments_per_page=60
):
    pages = [
        data[i : i + comments_per_page] for i in range(0, len(data), comments_per_page)
    ]

    with open(filename, "w") as htmlfile:
        htmlfile.write(
            f"<!-- Data extracted from {base_url}?page=article&id_article={article_id} -->\n"
        )
        # Basic CSS for styling
        htmlfile.write(
            """
        <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background-color: #f4f4f4;
                }
                .container {
                    max-width: 60em; /* Limiting the width based on font size */
                    margin: 40px auto; /* Centering the container */
                    padding: 20px;
                    background-color: #fff;
                    box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                }
                li {
                    background-color: #fff;
                    padding: 20px;
                    margin-bottom: 20px;
                    border-radius: 5px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                }
                .doc-title {
                    font-size: 28px;
                    font-weight: bold;
                    margin-bottom: 20px;
                }
                .doc-text {
                    font-size: 18px;
                    margin-bottom: 40px;
                }
                .comment-title {
                    font-size: 20px;
                    color: #2C3E50;
                    margin-bottom: 10px;
                    border-bottom: 2px solid #3498DB;
                    padding-bottom: 5px;
                }
                .comment-content {
                    font-size: 16px;
                    color: #7F8C8D;
                }
                .pagination {
                    display: flex;
                    justify-content: center;
                    margin-top: 20px;
                    flex-wrap: wrap;
                }
                .pagination a {
                    margin: 5px 10px;
                    padding: 5px 10px;
                    background-color: #007BFF;
                    color: white;
                    border-radius: 5px;
                    text-decoration: none;
                }
                .pagination a:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="container">
        """
        )

        # Writing the extracted document title and text
        htmlfile.write(f'<div class="doc-title">{doc_title}</div>\n')
        htmlfile.write(f'<div class="doc-text">{doc_text}</div>\n')

        def write_pagination():
            htmlfile.write('<div class="pagination">\n')
            for i in range(len(pages)):
                htmlfile.write(
                    f'<a href="javascript:void(0)" onclick="switchPage({i})">{i + 1}</a>\n'
                )
            htmlfile.write("</div>\n")

        write_pagination()  # Write pagination at the top of the page

        for index, page in enumerate(pages):
            htmlfile.write(
                f'<div id="page-{index}" class="page" style="display: {(lambda x: "block" if x == 0 else "none")(index)}">\n'
            )
            htmlfile.write("<ul>\n")
            for title, content in page:
                htmlfile.write("<li>\n")
                htmlfile.write(f'<div class="comment-title">{title}</div>\n')
                htmlfile.write(f'<div class="comment-content">{content}</div>\n')
                htmlfile.write("</li>\n")
            htmlfile.write("</ul>\n")
            htmlfile.write("</div>\n")

        write_pagination()  # Write pagination at the bottom of the page

        # JavaScript for pagination
        htmlfile.write(
            """
        <script>
            function switchPage(index) {
                const pages = document.querySelectorAll('.page');
                for (let page of pages) {
                    page.style.display = 'none';
                }
                document.querySelector(`#page-${index}`).style.display = 'block';
            }
        </script>
        """
        )

        htmlfile.write("</div>\n")
        htmlfile.write("</body>\n</html>")


if __name__ == "__main__":
    print("Enter article ID (e.g., 2877):")
    article_id = int(input().strip())

    print("Enter max forums value (e.g., 14840):")
    max_forums = int(input().strip())

    base_url = (
        "https://www.consultations-publiques.developpement-durable.gouv.fr/spip.php"
    )

    doc_title, doc_text, comments = fetch_comments_for_article(
        base_url, article_id, max_forums
    )

    base_filename = generate_filename(base_url, article_id)
    csv_filename = f"{base_filename}.csv"
    html_filename = f"{base_filename}.html"

    export_to_csv(comments, csv_filename)
    export_to_html(doc_title, doc_text, comments, html_filename)

    print(f"Comments extracted and saved to {base_filename}.csv!")
    print(f"Comments extracted and saved to {base_filename}.html!")
