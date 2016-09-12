

def main(**kw):
    """
    Application main entry points
    :param kw:
    :return:
    """


    """
    A plugin to attach the the publisher front-end to your views

    It extends your view  read, list content from the CMS

    kwargs:
        - query: {}
        - menu: {}
        - template_dir
        - endpoint
        - slug
        - title
    """

    # Totally required
    PublisherModel = kwargs.get("model")
    Post = PublisherModel.Post

    view_name = view.__name__
    templates_dir = kwargs.get("template_dir", "Mambo/Plugin/Publisher/Page")
    template_page = templates_dir + "/%s.html"
    slug = kwargs.get("slug", "slug")
    endpoint = kwargs.get("endpoint", "pages")
    endpoint_path = "/%s/" % endpoint
    endpoint_namespace = view_name + ":" + endpoint + ":" + "%s"
    title = kwargs.get("title", "")
    description = kwargs.get("description", "")

    query = kwargs.get("query", {})
    query.setdefault("types", [])
    query.setdefault("categories", [])
    query.setdefault("tags", [])
    query.setdefault("order_by", "published_at desc")
    query.setdefault("per_page", 20)

    _menu = kwargs.get("menu", {})
    _menu.setdefault("title", "Pages")
    _menu.setdefault("order", 100)
    _menu.setdefault("visible", True)
    _menu.setdefault("extends", view)
    _menu.pop("endpoint", None)

    #  Options for page_single to customize the slug format
    # It will be used to access the proper endpoint and format the
    slug_format = {
        "id": {
            "url": "{id}",
            "accept": ["id"],
            "route": "%s/<int:id>" % endpoint_path,
            "endpoint": "%s:%s" % (view_name, "id")
        },
        "slug": {
            "url": "{slug}",
            "accept": ["slug"],
            "route": "%s/<slug>" % endpoint_path,
            "endpoint": "%s:%s" % (view_name, "slug")
        },
        "id-slug": {
            "url": "{id}/{slug}",
            "accept": ["id", "slug"],
            "route": "%s/<int:id>/<slug>" % endpoint_path,
            "endpoint": "%s:%s" % (view_name, "id-slug")
        },
        "month-slug": {
            "url": "{month}/{slug}",
            "accept": ["month", "slug"],
            "route": '%s/<regex("[0-9]{4}/[0-9]{2}"):month>/<slug>' % endpoint_path,
            "endpoint": "%s:%s" % (view_name, "month-slug")
        },
        "date-slug": {
            "url": "{date}/{slug}",
            "accept": ["date", "slug"],
            "route": '%s/<regex("[0-9]{4}/[0-9]{2}/[0-9]{2}"):date>/<slug>' % endpoint_path,
            "endpoint": "%s:%s" % (view_name, "id")
        }
    }

    class PublisherPage(Mambo):
        @classmethod
        def prepare_post(cls, post):
            """
            Prepare the post data,
            """
            url_kwargs = {
                "id": post.id,
                "slug": post.slug,
                "date": post.published_at.strftime("%Y/%m/%d"),
                "month": post.published_at.strftime("%Y/%m")
            }
            # Filter items not in the 'accept'
            url_kwargs = {_: None if _ not in slug_format.get(slug)["accept"]
            else __
                          for _, __ in url_kwargs.items()}

            url = url_for(slug_format.get(slug)["endpoint"],
                          _external=True,
                          **url_kwargs)
            post.url = url
            return post

        @classmethod
        def prepare_author(cls, author):
            """
            Prepare the author data
            """
            name = utils.slugify(author.name or "no-name")
            # url = url_for("%s:post_author" % view_name, id=author.id, name=name, _external=True)
            # author.url = url
            return author

        @classmethod
        def get_prev_next_post(cls, post, position):
            """
            Return previous or next post based on the current post
            :params post: post object
            :params position:
            """
            position = position.lower()
            if position not in ["prev", "next"]:
                raise ValueError("Invalid position key. Must be 'prev' or 'next'")

            posts = Post.get_published(types=post_types)

            if position == "prev":
                posts = posts.filter(Post.id < post.id)
            elif position == "next":
                posts = posts.filter(Post.id > post.id)
            post = posts.first()
            return cls.prepare_post(post) if post else None

        @menu(endpoint=endpoint_namespace % "page_index", **_menu)
        @template(template_page % "page_index")
        @route(endpoint_path, endpoint=endpoint_namespace % "page_index")
        def page_index(self, endpoint=None):

            page = request.args.get("page", 1)
            app_per_page = get_config("APPLICATION_PAGINATION_PER_PAGE", 10)
            per_page = query.get("limit", app_per_page)

            set_meta(title=title, description=description)

            _query = {"types": query.get("types"),
                      "categories": query.get("categories"),
                      "tags": query.get("tags")}

            posts = Post \
                .get_published(**_query) \
                .order_by(query.get("order_by"))

            posts = posts.paginate(page=page,
                                   per_page=per_page,
                                   callback=self.prepare_post)
            _kwargs = {
                """
                "post_header": opt_endpoints.get("index.post_header", None),
                "post_subheader": opt_endpoints.get("index.post_subheader", None),
                "post_show_byline": opt_endpoints.get("index.post_show_byline", True)
                visible_with_
                """
            }
            _kwargs = dict()
            return dict(posts=posts, **_kwargs)

        @menu("%s Page" % _menu["name"],
              visible=False,
              endpoint=slug_format.get(slug).get("endpoint"),
              extends=view)  # No need to show the read in the menu
        @template(template_page % "page_single")
        @route(slug_format.get(slug).get("route"),
               endpoint=slug_format.get(slug).get("endpoint"))
        def page_single(self, id=None, slug=None, month=None, date=None):
            """
            Endpoints options
                single
                    - post_show_byline
            """
            post = None
            _q = {}
            if id:
                _q = {"id": id}
            elif slug:
                _q = {"slug": slug}

            post = Post.get_published(types=query.get("types"), **_q)
            if not post:
                abort("PublisherPageNotFound")

            set_meta(title=post.title,
                     image=post.top_image,
                     description=post.excerpt)

            _kwargs = {
                # "post_show_byline": opt_endpoints.get("single.post_show_byline", True)
            }
            _kwargs = dict()
            return dict(post=self.prepare_post(post), **_kwargs)

        @menu("%s Archive" % _menu["name"],
              visible=False,
              endpoint=endpoint_namespace % "page_archive",
              extends=view)
        @template(template_page % "page_archive")
        @route(endpoint_path + "archive/",
               endpoint=endpoint_namespace % "page_archive")
        def page_archive(self):

            set_meta(title="Archive")

            _query = {"types": query.get("types"),
                      "categories": query.get("categories"),
                      "tags": query.get("tags")}

            posts = Post.get_published(**_query) \
                .order_by(Post.published_at.desc()) \
                .group_by(Post.db.func.year(Post.published_at),
                          Post.db.func.month(Post.published_at))

            return dict(posts=posts)

        '''
        @menu(opt_endpoints.get("authors.menu", "Authors"),
              visible=opt_endpoints.get("authors.show_menu", False),
              #order=opt_endpoints.get("authors.menu_order", 91),
              endpoint=endpoint_namespace % "post_authors",
              extends=view)
        @template(template_page % "post_authors")
        @route(opt_endpoints.get("authors.endpoint", "authors"),
               endpoint=endpoint_namespace % "post_authors")
        def post_authors(self):
            """
            Endpoints options
                - authors
                    menu
                    show_menu
                    menu_order
                    endpoint
                    title
            """

            set_meta(title=opt_endpoints.get("authors.title", "Authors"))

            authors = []
            return dict(authors=authors)

        @menu(opt_endpoints.get("author.menu", "Author"),
              visible=False,
              endpoint=endpoint_namespace % "post_author",
              extends=view)
        @template(template_page % "post_author")
        @route("%s/<id>/<name>" % opt_endpoints.get("author.endpoint", "author"),
               endpoint=endpoint_namespace % "post_author")
        def post_author(self, id, name=None):
            """
            Endpoints options
                - author
                    endpoint
            """

            set_meta(title=opt_endpoints.get("author.title", "Author"))

            author = []
            return dict(author=author)
        '''


    return PublisherPage


from mambo.contrib.publisher import posts, get_post

@posts
def index(self):

    return {
        "post": get_post("hello-world")
    }



import db, model

class Hello(db.Model):
    pass

