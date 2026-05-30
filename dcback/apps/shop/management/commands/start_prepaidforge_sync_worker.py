import asyncio

from django.conf import settings
from django.core.management.base import BaseCommand
from temporalio.client import Client, ScheduleOverlapPolicy
from temporalio.worker import Worker

from apps.shop.management.commands.ensure_prepaidforge_sync_schedule import ensure_prepaidforge_sync_schedule
from apps.shop.temporal_activities import sync_prepaidforge_products_activity
from apps.shop.temporal_workflows import PrepaidForgeProductSyncWorkflow


class Command(BaseCommand):
    help = "Start Temporal worker for PrepaidForge product sync."

    def add_arguments(self, parser):
        parser.add_argument("--address", default=settings.TEMPORAL_ADDRESS)
        parser.add_argument("--namespace", default=settings.TEMPORAL_NAMESPACE)
        parser.add_argument("--task-queue", default=settings.TEMPORAL_TASK_QUEUE_PREPAIDFORGE_SYNC)
        parser.add_argument("--schedule-id", default=settings.TEMPORAL_PREPAIDFORGE_SYNC_SCHEDULE_ID)
        parser.add_argument(
            "--ensure-schedule",
            action="store_true",
            help="Create or update the 5-minute Temporal schedule before starting the worker.",
        )
        parser.add_argument(
            "--trigger-now",
            action="store_true",
            help="Ensure the schedule and trigger one workflow immediately before polling.",
        )

    def handle(self, *args, **options):
        asyncio.run(
            self._run(
                address=options["address"],
                namespace=options["namespace"],
                task_queue=options["task_queue"],
                schedule_id=options["schedule_id"],
                ensure_schedule=options["ensure_schedule"],
                trigger_now=options["trigger_now"],
            )
        )

    async def _run(
        self,
        *,
        address: str,
        namespace: str,
        task_queue: str,
        schedule_id: str,
        ensure_schedule: bool,
        trigger_now: bool,
    ) -> None:
        client = await Client.connect(address, namespace=namespace)
        if ensure_schedule or trigger_now:
            status = await ensure_prepaidforge_sync_schedule(
                client,
                task_queue=task_queue,
                schedule_id=schedule_id,
            )
            self.stdout.write(self.style.SUCCESS(f"PrepaidForge sync schedule {status}: {schedule_id}"))

        if trigger_now:
            await client.get_schedule_handle(schedule_id).trigger(overlap=ScheduleOverlapPolicy.SKIP)
            self.stdout.write(self.style.SUCCESS(f"PrepaidForge sync schedule triggered: {schedule_id}"))

        worker = Worker(
            client,
            task_queue=task_queue,
            workflows=[PrepaidForgeProductSyncWorkflow],
            activities=[sync_prepaidforge_products_activity],
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Temporal worker started: address={address}, namespace={namespace}, task_queue={task_queue}"
            )
        )
        self.stdout.write(
            "Worker is polling for Temporal tasks and is expected to keep running. "
            "Use Ctrl+C to stop it."
        )
        if not ensure_schedule and not trigger_now:
            self.stdout.write(
                f"Schedule is not registered by this command unless you pass --ensure-schedule. "
                f"To register it separately, run: python manage.py ensure_prepaidforge_sync_schedule --schedule-id {schedule_id}"
            )
        await worker.run()
