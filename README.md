# Card-Sorter
## Purpose
To build a card sorting machine. Include a website, randomize function, sort function, drag and drop card organizing.
Design will be based around a deck that is face up and scanned via a camera and OpenCV, then hit into a carousel of buckets with an arbitration bucket for bucket sort.
## Programing Steps
Set up the environment
Create a project folder, a Python virtual environment, and install the two packages you need: `pip install nicegui httpx`. NiceGUI is your whole backend+frontend framework; httpx is just for the outbound POST on Accept.

1. Write the data model file
Create `models.py` with a `Card` class (rank, suit, an `id` property for `rank-suit`) and your `RANK_ORDER` list for the custom A,K,Q...2 sort. No NiceGUI code here — this file should be plain Python you could unit test on its own.

2. Write the page skeleton
Create `main.py`. Start with just a title label and an empty `deck = []` list plus `hidden = False` flag at module level, and confirm `nicegui run` boots a blank page before adding any cards.

3. Render the card grid as images
Add a `@ui.refreshable` function that loops over `deck` and draws one `ui.image()` per card inside a container div with a fixed id, each image tagged with a `data-id` attribute matching `card.id`. Call it once on the page so something renders.

4. Load SortableJS and attach it to the container
Add the CDN `<script>` tag via `ui.add_head_html`, then after the grid renders, run a small JS snippet that calls `Sortable.create()` on the container. At this point dragging works visually but Python doesn't know about it yet.

5. Wire send-on-drop: JS notifies Python the moment a card is dropped
This is the piece that's different from 'sync only on Accept'. Register a Python handler with `ui.on('card_order_changed', handler)`. In Sortable's `onEnd` callback (JS), call the browser-global `emitEvent('card_order_changed', {order: ids})` where `ids` is the current list of `data-id`s read from the container. The Python handler receives that list and calls `deck.set_order(ids)` immediately — so `deck` is always in sync with what's on screen, no waiting for Accept.

7. Add the Randomize and Sort buttons
Both just mutate `deck` and `hidden`, then call `card_grid.refresh()` — same logic as before. Randomize additionally sets `disabled: true` on the Sortable instance (you can't rearrange cards you can't see); Sort leaves it enabled.

8. Add the Accept button
Since the array is now kept in sync on every drop, Accept no longer needs to query the DOM at all — it just reads `deck.export_order()` directly and POSTs it. This is simpler than the earlier 'sync on Accept' version because step 6 already did the work.

9. Write requirements.txt
Create a `requirements.txt` in your project root listing exactly what main.py imports: `nicegui`, `httpx`. Pin versions once your code is working (e.g. `nicegui==2.x.x`) so a rebuild months from now doesn't silently pull a breaking update.

10. Write the Dockerfile
Create a `Dockerfile` in the project root. Base it on `python:3.12-slim` (it has official arm64 builds, so it works natively on the Pi 4). Structure: copy requirements.txt first and run pip install (so Docker caches that layer separately from your code), then copy the rest of your app, then set the container's CMD to run main.py. Expose port 8080 (or whatever port your `ui.run()` call uses internally) with an `EXPOSE` line — this is documentation for Docker, not what actually publishes the port.

10. Build the image for the right architecture
If you're writing/building the Dockerfile on the Pi itself, a normal `docker build -t card-sorter .` just works, since it's already ARM. If you're building on an x86 dev machine and pushing/copying the image to the Pi, you need `docker buildx build --platform linux/arm64 -t card-sorter .` instead — a plain build produces an x86 image that will fail to run on the Pi with an 'exec format error'.

11. Build and sanity-check the image
Run `docker build -t card-sorter . ` (or the buildx variant) from the project root, then confirm it exists with `docker images`. Do a first test run locally with `docker run --rm -p 8080:8080 card-sorter` before worrying about port 2222 — confirms the image itself works before adding the port-mapping variable.

12. Map host port 2222 to the container's internal port
Your app's internal `ui.run(port=8080)` never has to change. Port mapping is entirely a `docker run` (or compose) concern: `docker run -d -p 2222:8080 --name card-sorter card-sorter`. This tells Docker 'requests hitting the host's port 2222 get forwarded to the container's port 8080.' The `-d` runs it detached (in the background) so it keeps running after you close the terminal.

13. Verify it's reachable on the local network first
From the Pi itself, confirm it's up with `curl http://localhost:2222` or by opening `http://<pi-ip>:2222` in a browser on the same network. If that doesn't load, check `docker ps` (is it running?) and `docker logs card-sorter` (did NiceGUI actually start?) before touching your router.

14. Set up the router port forward
Log into your router's admin page and forward external port 2222 to the Pi's local IP on port 2222 (match the port you chose in step 10a, or forward a different external port to 2222 on the Pi if you want them to differ). Give the Pi a static local IP or a DHCP reservation first — otherwise the forward breaks whenever the Pi's address changes.

15. Make it restart automatically
Add `docker run --restart unless-stopped ...` (or the equivalent in a docker-compose.yml) so the container comes back up automatically after a Pi reboot or crash, without you needing to SSH in and restart it manually.
