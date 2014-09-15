from django.core.management.base import BaseCommand
from example.management.grabbers.other.DistrictGrabber import DistrictGrabber
from example.management.grabbers.other.SubwayGrabber import SubwayGrabber
from example.management.grabbers.other.CinemaGrabber import CinemaGrabber
# from example.management.grabbers.events.LookAtMeGrabber import LookAtMeGrabber
from example.management.grabbers.events.TwoDoTwoGoGrabber import TwoDoTwoGoGrabber
from example.management.grabbers.events.KudaGoGrabber import KudaGoGrabber
from example.management.grabbers.multi_start import multi_start


class Command(BaseCommand):
    def handle(self, *args, **options):
        SubwayGrabber(0, 'firefox').grab_stations_info()
        DistrictGrabber(1, 'firefox').grab_districts_info()

        multi_start(CinemaGrabber, "firefox")

        multi_start(KudaGoGrabber, "firefox")
        multi_start(TwoDoTwoGoGrabber, "firefox")
