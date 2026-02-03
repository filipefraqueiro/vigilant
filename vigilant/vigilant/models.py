from django.db import models
import random
import string
import secrets
import re
#
#
#
def random_key():
    length = 25
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))
#
#
#
class connection(models.Model):
    created = models.DateTimeField(null=False, editable=False, auto_now_add=True)
    modified = models.DateTimeField(null=False, auto_now=True)
    name = models.CharField(max_length=255, blank=False, null=True)
    regex_parser = models.TextField(null=False, blank=False, help_text="Received Data Regex Parser")
    key = models.CharField(max_length=255, blank=True, null=True, default=random_key())
    fields = models.TextField(null=False, blank=True, help_text="Fields")


    def __str__(self):
        return self.name


    class Meta:
        app_label = "vigilant"
        verbose_name = "connection"
        verbose_name_plural = "connections"
#
#
#
class log_entry(models.Model):
    created = models.DateTimeField(null=False, editable=False, auto_now_add=True)
    modified = models.DateTimeField(null=False, auto_now=True)
    content = models.JSONField(null=False, blank=False, help_text="Received Data")
    connection = models.ForeignKey("connection", null=True, blank=True, on_delete=models.DO_NOTHING)


    def parse_regex(self):
        # print(self.connection.regex_parser)
        matches = re.match(self.connection.regex_parser, self.content).groupdict()
        self.content = matches


    def save(self, *args, **kwargs):       
        # if key and self.validate_connection(key):
        self.parse_regex()

        super(log_entry, self).save(*args, **kwargs)

    
    class Meta:
        app_label = "vigilant"
        verbose_name = "Log Entry"
        verbose_name_plural = "Log Entries"
#
#
#
class trigger(models.Model):
    created = models.DateTimeField(null=False, editable=False, auto_now_add=True)
    modified = models.DateTimeField(null=False, auto_now=True)
    connection = models.ForeignKey("connection", null=True, blank=True, on_delete=models.DO_NOTHING)
    
    
    class Meta:
        app_label = "vigilant"
        verbose_name = "Trigger"
        verbose_name_plural = "Triggers"