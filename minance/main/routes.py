import pickle
import logging

from sqlalchemy.sql.expression import func

from minance import socketio
from flask import Blueprint, render_template, request, redirect, url_for

from minance.models import Asset
from minance.main.forms import SearchForm
from minance.auth.forms import RegistrationForm, LoginForm

main = Blueprint("main", __name__)

@main.app_context_processor
def processor():
  random_assets = Asset.query.order_by(func.random()).limit(16)

  return dict(
    random_assets=random_assets,
    registrationForm=RegistrationForm(),
    searchForm=SearchForm(),
    loginForm=LoginForm()
  )

@main.route("/")
@main.route("/home")
def home():
  assets = Asset.query.order_by(Asset.margin.desc()).limit(24)
  return render_template("main/index.html", assets=assets, active_page="index", pickle=pickle, enumerate=enumerate, round=round, str=str, title="Home")

@main.route("/about")
def about():
  return render_template("main/about.html", active_page="about", title="About")

@main.route("/tos")
def tos():
  return render_template("main/tos.html", title="TOS")

@main.route("/guides")
def guides():
  return render_template("main/guides.html", title="Guides")

@main.route("/search", methods=["POST"])
def search():
  next_page = request.args.get("next")

  if request.method == "POST":
    query = request.form["query"]
    asset = Asset.query.filter(Asset.name.ilike(query.replace(" ", "_").upper())).first()
    if asset:
      return redirect(url_for("asset.specific_asset", asset_name=asset.name))
    else:
      return redirect(url_for("asset.filterAssets", search=query))