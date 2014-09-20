from optparse import make_option
from django.core.management.base import BaseCommand
from example.management.grabbers.other.DistrictGrabber import DistrictGrabber
from example.management.grabbers.other.SubwayGrabber import SubwayGrabber
from example.management.grabbers.other.CinemaGrabber import CinemaGrabber
from example.management.grabbers.events.TwoDoTwoGoGrabber import TwoDoTwoGoGrabber
from example.management.grabbers.events.KudaGoGrabber import KudaGoGrabber
from example.management.grabbers.multi_start import multi_start


def list_of_tasks(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("--tasks",
                    dest="tasks",
                    type='string',
                    action='callback',
                    callback=list_of_tasks,
                    default=None
        ),
        make_option("--browser",
                    action="store",
                    dest="browser",
                    default="phantomjs"
        ),
        make_option("-q", "--quiet",
                    action="store_true",
                    dest="verbose",
                    default=False,
                    help="don't print status messages to stdout"
        ),
    )

    def handle(self, *args, **options):
        verbose = options["verbose"]
        browser = options["browser"]
        tasks = options["tasks"]

        grabbers = {
            "subway": u"SubwayGrabber({}, \"{}\").grab_stations_info()".format(verbose, browser),
            "district": u"DistrictGrabber({}, \"{}\").grab_districts_info()".format(verbose, browser),
            "cinema": u"multi_start(CinemaGrabber, \"{}\")".format(browser),
            "kudago": u"multi_start(KudaGoGrabber, \"{}\")".format(browser),
            "twodotwogo": u"multi_start(TwoDoTwoGoGrabber, \"{}\")".format(browser)
        }

        for task in tasks:
            if task in grabbers.keys():
                exec grabbers[task]
