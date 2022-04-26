from datasette import hookimpl
from functools import wraps
import time

SCRIPT = """
<script>
let footer = document.querySelector("footer");
if (footer) {
    let ms = MS;
    let s = ` &middot; Page took ${ms.toFixed(3)}ms`;
    footer.innerHTML += s;
}
</script>
"""


@hookimpl
def asgi_wrapper(datasette):
    def wrap_with_total_page_time(app):
        @wraps(app)
        async def add_total_page_time(scope, receive, send):
            start = time.perf_counter()
            is_html = False

            async def wrapped_send(event):
                nonlocal is_html
                if event["type"] == "http.response.start":
                    headers = event.get("headers") or []
                    if b"text/html" in dict(headers)[b"content-type"]:
                        is_html = True
                    await send(event)
                elif is_html and event["type"] == "http.response.body":
                    # if it's HTML and there is no more body, append the rest
                    if not event.get("more_body"):
                        event["more_body"] = 1
                        await send(event)
                        await send(
                            {
                                "type": "http.response.body",
                                "body": SCRIPT.replace(
                                    "MS", str((time.perf_counter() - start) * 1000)
                                ).encode("utf-8"),
                            }
                        )
                else:
                    await send(event)

            await app(scope, receive, wrapped_send)

        return add_total_page_time

    return wrap_with_total_page_time
