"""Paid / ToPay Suite - the original browser-side tool, now inside the shared shell."""
from flask import Blueprint, render_template

from core.auth import module_required

bp = Blueprint("paid_topay", __name__, url_prefix="/paid-topay")


@bp.route("/")
@module_required("paid_topay")
def index():
    return render_template("modules/paid_topay.html")
