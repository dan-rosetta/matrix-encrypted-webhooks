import asyncio
import logging
import os
import sys
import traceback

from E2EEClient import E2EEClient
from WebhookServer import WebhookServer

async def main() -> None:
    logging.basicConfig(
        level=logging.getLevelName(
            os.environ.get('PYTHON_LOG_LEVEL', 'info').upper()),
        format='%(asctime)s | %(levelname)s | module:%(name)s | %(message)s'
    )

    webhook_server = WebhookServer()
    matrix_client = E2EEClient(webhook_server.get_known_rooms())
    processes = [matrix_client.run(), webhook_server.run(matrix_client)]

    await asyncio.gather(*processes, return_exceptions=True)

def run_async_main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except Exception:
        logging.critical(traceback.format_exc())
        sys.exit(1)
    except KeyboardInterrupt:
        logging.critical('Received keyboard interrupt.')
        sys.exit(0)

if __name__ == "__main__":
    run_async_main()
