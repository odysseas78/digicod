from __future__ import annotations

from typing import Any

from asgiref.sync import sync_to_async
from django.db import close_old_connections
from temporalio import activity

from apps.shop.prepaidforge import PrepaidForgeClient


def _sync_prepaidforge_products() -> dict[str, Any]:
    close_old_connections()
    try:
        activity.logger.info("Starting PrepaidForge product sync.")
        summary = PrepaidForgeClient().sync_products()
        activity.logger.info("Finished PrepaidForge product sync: %s", summary)
        return summary
    finally:
        close_old_connections()


@activity.defn
async def sync_prepaidforge_products_activity() -> dict[str, Any]:
    return await sync_to_async(_sync_prepaidforge_products, thread_sensitive=True)()
