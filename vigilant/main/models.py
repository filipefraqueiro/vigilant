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
    trigger = models.ForeignKey("trigger", null=True, blank=True, on_delete=models.DO_NOTHING)


    def parse_regex(self):
        # print("parse_regex")
        # print(self.connection.regex_parser)
        matches = re.match(self.connection.regex_parser, self.content).groupdict()
        self.content = matches
    
    
    def check_triggers(self):
        # print("check_triggers")
        triggers = trigger.objects.filter(connection=self.connection)
        for t in triggers:
            value = self.content.get(t.field)
            if t.operation == "lt" and value < t.value:
                    self.trigger = t

            elif t.operation == "eq" and value == t.value:
                    self.trigger = t

            elif t.operation == "gt" and value > t.value:
                    self.trigger = t


    def save(self, *args, **kwargs):       
        # if key and self.validate_connection(key):
        self.parse_regex()
        self.check_triggers()

        super(log_entry, self).save(*args, **kwargs)

    
    class Meta:
        app_label = "vigilant"
        verbose_name = "Log Entry"
        verbose_name_plural = "Log Entries"
#
#
#
class trigger(models.Model):
    OPERATIONS = {
        "lt": "lt",
        "eq": "eq",
        "gt": "gt",
    }
    created = models.DateTimeField(null=False, editable=False, auto_now_add=True)
    modified = models.DateTimeField(null=False, auto_now=True)
    connection = models.ForeignKey("connection", null=True, blank=True, on_delete=models.DO_NOTHING)
    field = models.CharField(null=True, blank=False, choices=None)
    operation = models.CharField(null=True, blank=False, choices=OPERATIONS)
    value = models.CharField(null=True, blank=False)


    class Meta:
        app_label = "vigilant"
        verbose_name = "Trigger"
        verbose_name_plural = "Triggers"