from django.core.management.base import BaseCommand
from example.management.grabbers.other.CinemaGrabber import CinemaGrabber
from example.management.grabbers.events.LookAtMeGrabber import LookAtMeGrabber
from example.management.grabbers.events.TwoDoTwoGoGrabber import TwoDoTwoGoGrabber
from example.management.grabbers.events.KudaGoGrabber import KudaGoGrabber
from example.management.grabbers.multy_start import multi_start
from datetime import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        a = datetime.now()
        multi_start(CinemaGrabber())
        print datetime.now() - a
        b = datetime.now()
        multi_start(LookAtMeGrabber())
        print datetime.now() - b
        b = datetime.now()
        multi_start(KudaGoGrabber())
        print datetime.now() - b
        b = datetime.now()
        multi_start(TwoDoTwoGoGrabber())
        print datetime.now() - b
        print datetime.now() - a