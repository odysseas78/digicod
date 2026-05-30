import asyncio
from django.conf import settings
from django.core.management.base import BaseCommand
from temporalio.client import Client
from workflows.catalog_sync import CatalogSyncWorkflow

class Command(BaseCommand):
    help = "Start one catalog sync workflow"

    def handle(self, *args, **options):
        workflow_id = asyncio.run(self._run())
        self.stdout.write(self.style.SUCCESS(f"Catalog sync started: {workflow_id}"))

    async def _run(self) -> str:
        client = await Client.connect(settings.TEMPORAL_ADDRESS)
        handle = await client.start_workflow(
            CatalogSyncWorkflow.run,
            id="prepaidforge-catalog-sync-manual",
            task_queue=settings.TEMPORAL_TASK_QUEUE_ORDER,
        )
        return handle.id
