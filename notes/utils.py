
from tags.models import Tag
# from tags.models import Tag

# from .models import Tag

def get_or_create_user_tags(tags_data, user):
    tag_objs = []

    for tag_data in tags_data:
        tag_name = tag_data['name'].strip()

        tag, _ = Tag.objects.get_or_create(
            name=tag_name,
            user=user
        )
        tag_objs.append(tag)

    return tag_objs



