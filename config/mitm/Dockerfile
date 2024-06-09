FROM mitmproxy/mitmproxy

WORKDIR /src

COPY ./requirements.txt ./
# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    chromium-browser \
    libffi-dev \
    libssl-dev \
    python3-pip \
    xvfb \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY ./config/mitm/entrypoint.sh ./
COPY src/ .

RUN chmod +x /src/entrypoint.sh

ENTRYPOINT ["/src/entrypoint.sh"]