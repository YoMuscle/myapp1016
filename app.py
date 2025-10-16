from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'content': self.content
        }


@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get(post_id)
    if post:
        return render_template('post.html', post=post)
    return "文章不存在", 404

# 新增文章頁
@app.route('/new')
def new_post():
    return render_template('new_post.html')

# 編輯文章頁
@app.route('/edit/<int:post_id>')
def edit_post(post_id):
    return render_template('edit_post.html', post_id=post_id)


# RESTful API
@app.route('/api/posts', methods=['POST'])
def api_create_post():
    data = request.json
    post = Post(title=data['title'], author=data['author'], content=data['content'])
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def api_read_post(post_id):
    post = Post.query.get(post_id)
    if post:
        return jsonify(post.to_dict())
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def api_update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Not found'}), 404
    data = request.json
    post.title = data.get('title', post.title)
    post.author = data.get('author', post.author)
    post.content = data.get('content', post.content)
    db.session.commit()
    return jsonify(post.to_dict())

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def api_delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Not found'}), 404
    db.session.delete(post)
    db.session.commit()
    return jsonify({'result': 'deleted'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
