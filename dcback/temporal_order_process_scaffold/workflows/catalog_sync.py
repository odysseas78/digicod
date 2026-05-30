from __future__ import annotations

from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from workflows.activities import act_sync_prepaidforge_catalog

@workflow.defn
class CatalogSyncWorkflow:
    @workflow.run
    async def run(self) -> dict:
        return await workflow.execute_activity(
            act_sync_prepaidforge_catalog,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )
