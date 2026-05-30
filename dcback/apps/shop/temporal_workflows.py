from __future__ import annotations

from datetime import timedelta
from typing import Any

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from apps.shop.temporal_activities import sync_prepaidforge_products_activity


@workflow.defn
class PrepaidForgeProductSyncWorkflow:
    @workflow.run
    async def run(self) -> dict[str, Any]:
        workflow.logger.info("Starting PrepaidForge product sync workflow.")
        return await workflow.execute_activity(
            sync_prepaidforge_products_activity,
            start_to_close_timeout=timedelta(minutes=10),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=30),
                maximum_interval=timedelta(minutes=2),
                maximum_attempts=3,
            ),
        )
