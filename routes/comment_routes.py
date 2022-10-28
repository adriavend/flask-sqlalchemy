from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db.db import db
import formulario
from models.comment import Comment

comments_bp = Blueprint("comments", __name__)

@comments_bp.route('/comment', methods=['GET', 'POST'])
def comment():
    comment_form = formulario.CommentForm(request.form)

    if request.method == 'POST' and comment_form.validate():
        user_id = session['user_id']
        comment = Comment(user_id = user_id, text = comment_form.comment.data)

        db.session.add(comment)
        db.session.commit()

        success_message = "Nuevo comentario creado"
        flash(success_message)
        return redirect(url_for('comments.comment')) # comment = name function

    title = "Comentarios"
    return render_template('comment.html', title=title, form=comment_form)