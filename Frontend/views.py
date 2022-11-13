from flask import Blueprint, render_template, request
from .models import Website, Data
from flask_login import login_required, current_user
from uuid import uuid4
from . import db
import Logic.Scrape as Scrape

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("Home.html", user=current_user)


@views.route("/scrape", methods=['GET', 'POST'])
@login_required
def scrape():
    if request.method == "POST":
        scraping_productname = request.form.get("product_name")
        scraping_suchstring = request.form.get("product_suchstring")
        scraping_url = request.form.get("product_url")

        scrape = Scrape.Scrape(scraping_url, scraping_suchstring)
        scrape.get_html()
        availability = scrape.is_available()

        website = Website(website_id=uuid4().int, productname=scraping_productname,
                          url=scraping_url, search_string=scraping_suchstring,
                          user_id=current_user.user_id)

        db.session.add(website)
        db.session.commit()

        data = Data(data_id=uuid4().int, website_id=website.website_id, availability=availability)


        db.session.add(data)
        db.session.commit()

        return render_template("Scrape.html", user=current_user, availability=availability)
    else:
        return render_template("Scrape.html", user=current_user)
