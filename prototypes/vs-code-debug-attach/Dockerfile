# Exercise runtime for the Debugging Gym VS Code prototype.
#
# This is a disposable code spike: it runs a buggy Python program plus a
# harness, and exposes a Debug Adapter Protocol server (debugpy) on the
# mapped port so the learner's own VS Code can attach and hit breakpoints.
#
# It is intentionally small (runs on the 16 GB / 8 CPU VM constraint) and is
# NOT the product -- it answers one question: can VS Code attach to a hosted
# exercise runtime and debug with breakpoints?

FROM python:3.11-slim

# debugpy is the DAP server VS Code speaks to for Python.
RUN pip install --no-cache-dir debugpy

WORKDIR /app
COPY app/ /app/

# 5678 is debugpy's default attach port.
EXPOSE 5678

# Default: run the harness to show the defect is present. The learner's VS
# Code overrides this with a debugpy launch (see the attach instructions).
CMD ["python", "harness.py"]