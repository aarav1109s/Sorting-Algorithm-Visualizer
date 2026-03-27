# Sorting Algorithm Visualizer — pygame in Docker with VNC for GUI access.
#
# Build:
#   docker build -t sorting-viz .
#
# Run (then open VNC to localhost:5900 — no password; use only on trusted networks):
#   docker run --rm -p 5900:5900 sorting-viz
#
# On another PC: docker run --rm -p 5900:5900 sorting-viz
#   then VNC to that machine's IP address, port 5900.

FROM python:3.12-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    libsdl2-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libfreetype6 \
    xvfb \
    x11vnc \
    fluxbox \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY algorithms.py main.py .
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN sed -i 's/\r$//' /docker-entrypoint.sh && chmod +x /docker-entrypoint.sh

EXPOSE 5900

ENTRYPOINT ["/docker-entrypoint.sh"]
