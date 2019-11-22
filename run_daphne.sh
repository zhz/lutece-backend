echo "starting daphne websocket process ..."
daphne -u /tmp/daphne.sock Lutece.asgi:application &
