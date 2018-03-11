#!/bin/bash

# Start a simple Python web server for serving D3 visualizations.
#
# Run with:
#   ./webserver.sh
#
# Then visit http://localhost:8000/d3/index.html with your browser.
#
# See http://bl.ocks.org/fancellu/2c782394602a93921faff74e594d1bb1
#
# Chris Joakim, Microsoft, 2018/03/11

python -m http.server 8000
