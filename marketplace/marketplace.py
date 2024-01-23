# marketplace/marketplace.py
import os
import secrets
from flask import Flask, render_template, session, request

import grpc
from recommendations_pb2 import BookCategory, RecommendationRequest
from recommendations_pb2_grpc import RecommendationsStub

from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

class CategoryForm(FlaskForm):
    category = SelectField('Category', choices=[('MYSTERY', 'Mystery'), ('SCIENCE_FICTION', 'Science Fiction'), ('SELF_HELP', 'Self Help')], validators=[DataRequired()])

recommendations_host = os.environ.get("RECOMMENDATIONS_HOST", "localhost")
recommendations_channel = grpc.insecure_channel(
    f"{recommendations_host}:50051"
)
recommendations_client = RecommendationsStub(recommendations_channel)


@app.before_request
def make_csrf_secret_key():
    if 'csrf_secret_key' not in session:
        session['csrf_secret_key'] = secrets.token_hex(16)

   
@app.route('/', methods=['GET','POST'])
def get_recommendations():
    form = CategoryForm()
    if form.validate_on_submit():
        category = form.category.data
        category_enum = BookCategory.Value(category)
        recommendation_request = RecommendationRequest(user_id=1, category=category_enum, max_results=5)
        recommendations_response = recommendations_client.Recommend(recommendation_request)
        category_dict = dict(form.category.choices)
        return render_template(
            "recommendations.html",
            category=category_dict.get(category),
            recommendations=recommendations_response.recommendations,
        )
    else:
        return render_template('homepage.html', form=form)