from django.core.management.base import BaseCommand
from example.management.grabbers.vm_catalog.AromaButik import AromaButik
from example.management.grabbers.vm_catalog.multi_start import multi_start


class Command(BaseCommand):
    def handle(self, *args, **options):
        multi_start(AromaButik)