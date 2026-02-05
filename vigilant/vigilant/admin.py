from django.contrib import admin

import vigilant.models
#
#
#
class log_entry_Admin(admin.ModelAdmin):
    list_display = ["id", "created", "modified", "connection", "trigger"]
    list_filter = []
    search_fields = []

admin.site.register(vigilant.models.log_entry, log_entry_Admin)
#
#
#
class connection_Admin(admin.ModelAdmin):
    list_display = ["id", "created", "modified", "name", "key"]
    list_filter = []
    search_fields = []

admin.site.register(vigilant.models.connection, connection_Admin)
#
#
#
class trigger_Admin(admin.ModelAdmin):
    list_display = ["id", "created", "modified", "connection", "field", "operation"]
    list_filter = []
    search_fields = []

admin.site.register(vigilant.models.trigger, trigger_Admin)
#
#
#