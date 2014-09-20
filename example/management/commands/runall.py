from django.core.management.base import BaseCommand
from optparse import make_option
from example.management.grabbers.other.DistrictGrabber import DistrictGrabber
from example.management.grabbers.other.SubwayGrabber import SubwayGrabber
from example.management.grabbers.other.CinemaGrabber import CinemaGrabber
# from example.management.grabbers.events.LookAtMeGrabber import LookAtMeGrabber
from example.management.grabbers.events.TwoDoTwoGoGrabber import TwoDoTwoGoGrabber
from example.management.grabbers.events.KudaGoGrabber import KudaGoGrabber
from example.management.grabbers.multi_start import multi_start


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("--browser",
                    action="store",
                    dest="browser",
                    default="phantomjs"
        ),
        make_option("-q", "--quiet",
                    action="store_true",
                    dest="verbose",
                    default=False,
                    help="print status messages to stdout"
        ),
    )

    def handle(self, *args, **options):
        verbose = options["verbose"]
        browser = options["browser"]

        SubwayGrabber(verbose, browser).grab_stations_info()
        DistrictGrabber(verbose, browser).grab_districts_info()

        multi_start(CinemaGrabber, browser)
        multi_start(KudaGoGrabber, browser)
        multi_start(TwoDoTwoGoGrabber, browser)
