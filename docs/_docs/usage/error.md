---
title: Error Pages
description: MHTTC has custom error pages
---

# Error Pages

When running in non-debug mode, meaning that DEBUG is set to False in your
settings:

```python
DEBUG=False
```

If the user hits a 404 (page not found) we show them a custom view:

![404.png]({{ site.baseurl }}/docs/usage/img/404.png)

If the user triggers a server error, we show them a modified version of the above
with a different graphic.

Errors are sent to [Sentry](https://sentry.io) if you've defined the `SENTRY_ID`
in your environment.
