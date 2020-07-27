from blog.models import Category


def get_sub_category(category: Category):
    if (subs := category.sub_categories) is None:
        yield category
    else:
        for sub in subs:
            yield sub
            yield from get_sub_category(sub)
