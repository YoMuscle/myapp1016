from flask import Flask, render_template

app = Flask(__name__)

# 假資料
posts = [
    {
        "id": 1,
        "title": "第一篇文章",
        "author": "小明",
        "content": "這是第一篇部落格文章內容。"
    },
    {
        "id": 2,
        "title": "第二篇文章",
        "author": "小華",
        "content": "這是第二篇部落格文章內容。"
    }
]

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    if post:
        return render_template('post.html', post=post)
    return "文章不存在", 404

if __name__ == '__main__':
    app.run(debug=True)
