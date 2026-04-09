import datetime
import sys
import os
import logging
from collections import defaultdict
import csv

from django.core.management.base import BaseCommand

import main.models
#
#
#
class Command(BaseCommand):
    help = f"Nice Help Message"


    def add_arguments(self, parser):
        pass


    def handle(self, *args, **options):
        print("hello world")
        for c in main.models.connection.objects.all():
            print(c.key)