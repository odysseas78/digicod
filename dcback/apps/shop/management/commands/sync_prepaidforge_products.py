from django.core.management.base import BaseCommand, CommandError

from apps.shop.prepaidforge import PrepaidForgeClient
from apps.shop.services import PrepaidForgeError


class Command(BaseCommand):
    help = "Synchronisiert Produkte aus der PrepaidForge API in den lokalen Shop-Katalog."

    def handle(self, *args, **options):
        client = PrepaidForgeClient()
        try:
            summary = client.sync_products()
        except PrepaidForgeError as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(
            self.style.SUCCESS(
                f"{summary['stocks']} Produkte synchronisiert "
                f"({summary['products']} Katalog-Produkte, {summary['skus']} SKUs)."
            )
        )
