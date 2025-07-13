
from tags.models import Tag
from uuid import UUID


# def get_or_create_user_tags(tag_data_list, user):
#     tag_objs = []

#     for tag_data in tag_data_list:
#         try:
#             tag_id = UUID(str(tag_data['id']))
#         except (ValueError, TypeError):
#             continue  # Skip if invalid UUID

#         tag = Tag.objects.filter(id=tag_id, user=user).first()
#         if tag:
#             tag_objs.append(tag)
#         else:
#             tag = Tag.objects.create(id=tag_id, name=tag_data['name'], user=user)
#             tag_objs.append(tag)

#     return tag_objs


from tags.models import Tag

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


# def get_or_create_user_tags(tags_data, user):
#     tag_objs = []

#     for tag in tags_data:
#         tag_id = tag.get('id')
#         tag_name = tag.get('name')

#         obj, _ = Tag.objects.get_or_create(
#             id=tag_id,  # You can optionally use this, but not required unless you're managing IDs manually
#             defaults={
#                 'name': tag_name,
#                 'user': user,
#             }
#         )

#         # Ensure tag belongs to this user (or skip if it doesn’t)
#         if obj.user != user:
#             continue  # or raise a PermissionError

#         tag_objs.append(obj)

#     return tag_objs
