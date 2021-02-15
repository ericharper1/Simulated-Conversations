from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore


class Command(BaseCommand):
    help = "Runs scheduler for SimCon."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
