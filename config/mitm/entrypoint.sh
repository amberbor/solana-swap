#!/bin/bash

# Start Xvfb to create a virtual display
Xvfb :99 -screen 0 1024x768x16 &

# Set the DISPLAY environment variable to use the virtual display
export DISPLAY=:99

# Start Chromium in the background
chromium-browser --no-sandbox https://photon-sol.tinyastro.io/en/discover &

# Start mitmproxy with the web interface enabled
mitmdump -s /src/mitm_run.py --mode regular@8082 &
mitmweb --web-host 0.0.0.0 --web-port 8081 --mode regular@8083 &

# Wait for all background processes to finish
wait
