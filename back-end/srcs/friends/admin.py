from django.contrib import admin
from .models import Friendship, muted_User, blocked_User, messages

admin.site.register(Friendship)
admin.site.register(muted_User)
admin.site.register(blocked_User)

admin.site.register(messages)

