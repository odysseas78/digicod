import asyncio
from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from temporalio.client import (
    Client,
    Schedule,
    ScheduleActionStartWorkflow,
    ScheduleAlreadyRunningError,
    ScheduleIntervalSpec,
    ScheduleOverlapPolicy,
    SchedulePolicy,
    ScheduleSpec,
    ScheduleUpdate,
)

from apps.shop.temporal_workflows import PrepaidForgeProductSyncWorkflow


def build_prepaidforge_sync_schedule(task_queue: str, workflow_id: str) -> Schedule:
    return Schedule(
        action=ScheduleActionStartWorkflow(
            PrepaidForgeProductSyncWorkflow.run,
            id=workflow_id,
            task_queue=task_queue,
            execution_timeout=timedelta(minutes=15),
            static_summary="PrepaidForge product sync",
        ),
        spec=ScheduleSpec(
            intervals=[ScheduleIntervalSpec(every=timedelta(minutes=5))],
        ),
        policy=SchedulePolicy(overlap=ScheduleOverlapPolicy.SKIP),
    )


async def ensure_prepaidforge_sync_schedule(client: Client, *, task_queue: str, schedule_id: str) -> str:
    workflow_id = f"{schedule_id}-workflow"
    schedule = build_prepaidforge_sync_schedule(task_queue, workflow_id)

    try:
        await client.create_schedule(schedule_id, schedule)
        return "created"
    except ScheduleAlreadyRunningError:
        handle = client.get_schedule_handle(schedule_id)
        await handle.update(lambda _: ScheduleUpdate(schedule=schedule))
        return "updated"


class Command(BaseCommand):
    help = "Create or update the Temporal schedule for PrepaidForge product sync."

    def add_arguments(self, parser):
        parser.add_argument("--address", default=settings.TEMPORAL_ADDRESS)
        parser.add_argument("--namespace", default=settings.TEMPORAL_NAMESPACE)
        parser.add_argument("--task-queue", default=settings.TEMPORAL_TASK_QUEUE_PREPAIDFORGE_SYNC)
        parser.add_argument("--schedule-id", default=settings.TEMPORAL_PREPAIDFORGE_SYNC_SCHEDULE_ID)

    def handle(self, *args, **options):
        status = asyncio.run(
            self._run(
                address=options["address"],
                namespace=options["namespace"],
                task_queue=options["task_queue"],
                schedule_id=options["schedule_id"],
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"PrepaidForge sync schedule {status}: {options['schedule_id']} "
                f"(address={options['address']}, namespace={options['namespace']}, task_queue={options['task_queue']})"
            )
        )

    async def _run(self, *, address: str, namespace: str, task_queue: str, schedule_id: str) -> str:
        client = await Client.connect(address, namespace=namespace)
        return await ensure_prepaidforge_sync_schedule(
            client,
            task_queue=task_queue,
            schedule_id=schedule_id,
        )
