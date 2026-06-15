import asyncio
from django.conf import settings
from django.core.management.base import BaseCommand
from temporalio.client import Client
from temporalio.worker import Worker
from workflows.order_fulfillment import OrderFulfillmentWorkflow
from workflows.catalog_sync import CatalogSyncWorkflow
from workflows.activities import (
    act_load_order_snapshot, act_verify_payment, act_final_availability_check,
    act_purchase_and_store_supplier_codes, act_send_order_codes_email,
    act_mark_order_completed, act_mark_order_needs_review, act_sync_prepaidforge_catalog,
)

class Command(BaseCommand):
    help = "Start Temporal worker for order fulfillment and catalog sync"

    def handle(self, *args, **options):
        asyncio.run(self._run())

    async def _run(self):
        client = await Client.connect(settings.TEMPORAL_ADDRESS)
        worker = Worker(
            client,
            task_queue=settings.TEMPORAL_TASK_QUEUE_ORDER,
            workflows=[OrderFulfillmentWorkflow, CatalogSyncWorkflow],
            activities=[
                act_load_order_snapshot, act_verify_payment, act_final_availability_check,
                act_purchase_and_store_supplier_codes, act_send_order_codes_email,
                act_mark_order_completed, act_mark_order_needs_review, act_sync_prepaidforge_catalog,
            ],
        )
        self.stdout.write(self.style.SUCCESS(f"Temporal worker started: {settings.TEMPORAL_TASK_QUEUE_ORDER}"))
        await worker.run()
