from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize page_views in session if not set
    session['page_views'] = session.get('page_views', 0)

    # Increment page_views
    session['page_views'] += 1

    # Check page_views limit
    if session['page_views'] <= 3:
        # Fetch and return article data
        article = Article.query.get_or_404(id)
        article_data = {
            'id': article.id,
            'author': article.author,
            'title': article.title,
            'content': article.content,
            'preview': article.preview,
            'minutes_to_read': article.minutes_to_read,
            'date': article.date,
            'user_id': article.user_id,
        }
        return jsonify(article_data)
    else:
        # Return error message and 401 status code
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

if __name__ == '__main__':
    app.run(port=5555)
