from flask import Blueprint, render_template
from sqlalchemy import desc
from db.db import db
from helpers import date_format
from models.comment import Comment
from models.user import User
import json

reviews_bp = Blueprint("reviews", __name__)

@reviews_bp.route('/reviews/', methods=['GET'])
@reviews_bp.route('/reviews/<int:page>', methods=['GET'])
def reviews(page = 1):
    per_page = 3
    comments = Comment.query.join(User).add_columns(
        User.username, 
        Comment.text,
        Comment.create_date,
        Comment.id).order_by(desc(Comment.id))
        #.all()
        #.paginate(page,per_page,False) # page-> pagina inicial, per_page-> cant paginas
    # print(comments)

    return render_template('reviews.html', comments = comments, date_format = date_format)

@reviews_bp.route('/review/<int:id>', methods=['DELETE'])
def review_delete_ajax(id):
    Comment.query.filter_by(id=id).delete()
    db.session.commit()
    return json.dumps({ 'ok': True, 'id': id})