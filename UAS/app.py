from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def Home():
    return render_template("index.html")

@app.route("/beautynesia")
def beautynesia():
    html_doc = requests.get("https://www.beautynesia.id/beauty/skincare")
    soup = BeautifulSoup(html_doc.text, "html.parser")
    populer_area = soup.find(attrs={'class': 'gap-3 d-flex flex-column mt-48px'})

    # Debug jika populer_area tidak ditemukan
    if not populer_area:
        print("Error: Element dengan class 'gap-3 d-flex flex-column mt-48px' tidak ditemukan.")
        return render_template("beautynesia.html", articles=[], error="Element tidak ditemukan.")

    articles = []
    items = populer_area.find_all("article")
    for item in items:
        image = item.find("img")
        link = item.find("a")
        title = item.find("h3")
        category = item.find("div", {"class": "beaut__info"})

        if image and link and title and category:
            articles.append({
                "img_src": image.get("src", ""),
                "img_alt": image.get("alt", ""),
                "link": link.get("href", ""),
                "title": title.text.strip(),
                "category": category.text.strip(),
            })

    return render_template("beautynesia.html", articles=articles)


@app.route("/womenpedia")
def womenpedia():
    html_doc = requests.get("https://womenpedia.id/category/beauty/")
    soup = BeautifulSoup(html_doc.text, "html.parser")
    populer_area = soup.find(attrs={'id': 'gmr-main-load'})
    
    if not populer_area:
        print("Error: Element dengan id 'gmr-main-load' tidak ditemukan.")
        return render_template("womenpedia.html", articles=[], error="Element tidak ditemukan.")
    
    articles = []
    items = populer_area.find_all("article")
    for item in items:
        image = item.find("img")
        link = item.find("a")
        title = item.find("h2", {"class": "entry-title"})
        time = item.find("time")  # Menggunakan elemen <time> jika ada

        if image and link and title and time:
            articles.append({
                "img_src": image.get("src", ""),
                "img_alt": image.get("alt", ""),
                "link": link.get("href", ""),
                "title": title.text.strip(),
                "time": time.text.strip(),
            })

    return render_template("womenpedia.html", articles=articles)


@app.route("/liputan6")
def liputan6():
    html_doc = requests.get("https://www.liputan6.com/tag/kecantikan")
    soup = BeautifulSoup(html_doc.text, "html.parser")
    populer_area = soup.find(attrs={'class': 'articles--iridescent-list'})
    
    if not populer_area:
        print("Error: Element dengan class 'articles--iridescent-list' tidak ditemukan.")
        return render_template("liputan6.html", articles=[], error="Element tidak ditemukan.")
    
    articles = []
    items = populer_area.find_all("article")
    for item in items:
        image = item.find("img")
        link = item.find("a")
        title = item.find("span", {"class": "articles--iridescent-list--text-item__title-link-text"})
        time = item.find("span", {"class": "articles--iridescent-list--text-item__datetime"})

        if image and link and title and time:
            articles.append({
                "img_src": image.get("src", ""),
                "img_alt": image.get("alt", ""),
                "link": link.get("href", ""),
                "title": title.text.strip(),
                "time": time.text.strip(),
            })

    return render_template("liputan6.html", articles=articles)


if __name__ == "__main__":
    app.run(debug=True)
