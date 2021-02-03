import datetime
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
def landing_page():
    return render_template('index.html')


@app.route('/blog')
def blog_home():
    return render_template('blog/blog.html')


class BlogInfo:
    def __init__(self, route, title, date, file):
        self.route = route
        self.title = title
        self.date = date
        self.file = file


class BlogIndex:
    def __init__(self):
        self.files = {}
        self.titles = {}
        self.dates = {}

    def register_blog(self, route, title, date, file):
        self.files[route] = file
        self.titles[route] = title
        self.dates[route] = date

    def blog_exists(self, route):
        return route in self.files

    def get_blog_info(self, route) -> BlogInfo:
        return BlogInfo(route, self.titles[route], self.dates[route], self.files[route])


blog = BlogIndex()
blog.register_blog('test', 'Test Blog', datetime.datetime.strptime('2021-02-03 19:07', '%Y-%m-%d %H:%M'), 'test.html')
blog.register_blog('new-platform', 'New Platform', datetime.datetime.strptime('2021-02-03 20:27', '%Y-%m-%d %H:%M'), 'random/new-platform.html')
blog.register_blog('chau', 'As a kid I got shamed for appropriating Italian culture', datetime.datetime.strptime('2018-02-01 00:01', '%Y-%m-%d %H:%M'), 'random/chau.html')


@app.route('/blog/<route>')
def blog_handler(route: str):
    if blog.blog_exists(route):
        blog_info = blog.get_blog_info(route)
        return render_template(f"blog/{blog_info.file}", blog_info=blog_info)
    else:
        return redirect('/blog', 404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
