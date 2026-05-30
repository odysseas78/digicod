from __future__ import annotations

from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from workflows.activities import (
        act_load_order_snapshot,
        act_verify_payment,
        act_final_availability_check,
        act_purchase_and_store_supplier_codes,
        act_send_order_codes_email,
        act_mark_order_completed,
        act_mark_order_needs_review,
    )

@workflow.defn
class OrderFulfillmentWorkflow:
    @workflow.run
    async def run(self, order_id: str) -> str:
        await workflow.execute_activity(act_load_order_snapshot, order_id, start_to_close_timeout=timedelta(seconds=10), retry_policy=RetryPolicy(maximum_attempts=3))
        await workflow.execute_activity(act_verify_payment, order_id, start_to_close_timeout=timedelta(seconds=10), retry_policy=RetryPolicy(maximum_attempts=1))

        availability = await workflow.execute_activity(act_final_availability_check, order_id, start_to_close_timeout=timedelta(seconds=20), retry_policy=RetryPolicy(maximum_attempts=3))
        if not availability.get("ok"):
            await workflow.execute_activity(act_mark_order_needs_review, args=[order_id, "Final supplier availability check failed", availability], start_to_close_timeout=timedelta(seconds=10), retry_policy=RetryPolicy(maximum_attempts=3))
            return "needs_review"

        try:
            await workflow.execute_activity(
                act_purchase_and_store_supplier_codes,
                order_id,
                start_to_close_timeout=timedelta(minutes=3),
                retry_policy=RetryPolicy(maximum_attempts=1),
            )
        except Exception as exc:
            await workflow.execute_activity(act_mark_order_needs_review, args=[order_id, f"Supplier purchase failed or uncertain: {exc}", {}], start_to_close_timeout=timedelta(seconds=10), retry_policy=RetryPolicy(maximum_attempts=3))
            return "needs_review"

        await workflow.execute_activity(
            act_send_order_codes_email,
            order_id,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=RetryPolicy(initial_interval=timedelta(seconds=10), maximum_interval=timedelta(minutes=10), maximum_attempts=10),
        )

        await workflow.execute_activity(act_mark_order_completed, order_id, start_to_close_timeout=timedelta(seconds=10), retry_policy=RetryPolicy(maximum_attempts=3))
        return "completed"
