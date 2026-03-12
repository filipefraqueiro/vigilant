import datetime
import sys
import os
import logging
from collections import defaultdict
import csv

from django.core.management.base import BaseCommand
#
#
#
class Command(BaseCommand):
    help = f"Nice Help Message"


    def add_arguments(self, parser):
        pass


    def handle(self, *args, **options):
        print("hello world")