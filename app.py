import datetime
from flask import Flask, render_template, redirect, url_for
from typing import List, Optional, Dict, Callable

app = Flask(__name__)


@app.route('/')
def landing_page():
    return render_template('index.html')


class BlogInfo:
    def __init__(self, route, title, date, file):
        self.route = route
        self.title = title
        self.date = date
        self.file = file


class BlogChain:
    def __init__(self, blog: BlogInfo):
        self.val = blog
        self.previous = None  # type: Optional[BlogChain]
        self.next = None  # type: Optional[BlogChain]


class BlogIndex:
    def __init__(self):
        self.files = {}
        self.titles = {}
        self.dates = {}

        self.entries = {}  # type: Dict[str, BlogInfo]
        # cached -- needs to be built
        self.chain = None # type: Optional[BlogChain]

    def register_blog(self, blog: BlogInfo):
        self.entries[blog.route] = blog

    def blog_exists(self, route):
        return route in self.entries

    def get_blog_info(self, route) -> BlogInfo:
        return self.entries[route]

    def build_chain(self):
        entries_sorted_time = sorted(list(self.entries.values()), key=lambda BI: BI.date, reverse=False)
        last_entry = None  # type: Optional[BlogChain]
        for i in range(len(entries_sorted_time)):
            if i == 0:
                self.chain = BlogChain(entries_sorted_time[0])
                last_entry = self.chain
            else:
                last_entry.next = BlogChain(entries_sorted_time[i])
                last_entry.next.previous = last_entry
                last_entry = last_entry.next

    def get_chain(self) -> Optional[BlogChain]:
        return self.chain

    def get_entry_in_chain(self, route) -> Optional[BlogChain]:
        cur = self.chain
        if cur is not None:
            while cur.val.route != route:
                cur = cur.next
        return cur

    def get_all_blogs(self) -> List[BlogInfo]:
        arr = []
        for route, blog_info in self.entries.items():
            arr.append(blog_info)
        return arr


blog = BlogIndex()
blog.register_blog(
    BlogInfo('learn-word-clusters',
             'Learn Vocabulary through Clusters',
             datetime.datetime.strptime('2021-02-05 14:32', '%Y-%m-%d %H:%M'),
             'random/learn-word-clusters.html'))
"""
blog.register_blog(
    BlogInfo('vnese-lang-advice',
             'Advice for learning Vietnamese',
             datetime.datetime.strptime('2021-02-04 15:01', '%Y-%m-%d %H:%M'),
             'random/vietnamese-lang-advice.html'))
"""
blog.register_blog(
    BlogInfo('new-platform',
             'New Platform',
             datetime.datetime.strptime('2021-02-03 20:27', '%Y-%m-%d %H:%M'),
             'random/new-platform.html'))
blog.register_blog(
    BlogInfo('test',
             'Test Blog',
             datetime.datetime.strptime('2021-02-03 19:07', '%Y-%m-%d %H:%M'),
             'test.html'))
blog.register_blog(
    BlogInfo('chau',
             'As a kid I got shamed for appropriating Italian culture',
             datetime.datetime.strptime('2018-02-01 00:01', '%Y-%m-%d %H:%M'),
             'random/chau.html'))
blog.build_chain()
# blog.register_blog('shipping-calculator', 'Shipping Calculator', datetime.datetime.strptime('2017-10-01 00:01', '%Y-%m-%d %H:%M'), 'random/shipping-calculator.html')


@app.route('/blog')
@app.route('/blog/')
def blog_home():
    return render_template('blog/blog.html', blog_index=blog, now=datetime.datetime.now())


@app.route('/blog/<route>')
def blog_handler(route: str):
    if blog.blog_exists(route):
        blog_info = blog.get_blog_info(route)
        return render_template(f"blog/{blog_info.file}", blog_chain=blog.get_entry_in_chain(route), blog_info=blog_info, now=datetime.datetime.now())
    else:
        return redirect('/blog', 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
