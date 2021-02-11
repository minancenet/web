from datetime import datetime
import pickle

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from trade import db
from trade.models import Asset, UserAsset
from trade.portfolio.forms import AddAssetForm

portfolio = Blueprint("portfolio", __name__)

@portfolio.route("/portfolio", methods=["GET", "POST"])
@login_required
def portfolio_dash():
  form = AddAssetForm()
  if form.validate_on_submit():
    asset = Asset.query.filter_by(name=form.asset_name.data).first()
    userAsset = UserAsset.query.filter_by(asset=asset).first()
    if not userAsset:
      userAsset = UserAsset(asset=asset, holder=current_user)
      db.session.add(userAsset)
      db.session.commit()

    specific_asset = [datetime.utcnow(), int(form.quantity.data)]
    loaded = pickle.loads(userAsset.specific_values)
    loaded.append(specific_asset)
    userAsset.specific_values = pickle.dumps(loaded)

    db.session.commit()

    flash("Asset successfully added.", "alert")
    return redirect(url_for("portfolio.portfolio_dash"))

  user_assets = UserAsset.query.filter_by(holder=current_user)

  return render_template("portfolio/portfolio.html", assets=user_assets, form=form, active_page="portfolio", title="Portfolio")

@portfolio.route("/portfolio/<string:asset_name>/edit", methods=["GET", "POST"])
@login_required
def edit_asset(asset_name):
  asset = Asset.query.filter_by(name=asset_name).first()
  if not asset:
    flash(f"Asset {asset_name} does not exists.", "alert")
    return redirect(url_for("portfolio.portfolio_dash"))

  userAsset = UserAsset.query.filter_by(asset=asset).first()
  if not userAsset:
    flash(f"Asset {asset_name} does not exists in your portfolio.", "alert")
    return redirect(url_for("portfolio.portfolio_dash"))

  return render_template("portfolio/edit_asset.html", active_page="portfolio", title="Portfolio Edit Asset")