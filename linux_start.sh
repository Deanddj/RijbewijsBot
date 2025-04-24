#!/bin/bash

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

/usr/bin/python3 "$SCRIPT_DIR/rijbewijs_aanvraag.py"
/usr/bin/python3 "$SCRIPT_DIR/rijbewijs_ophalen.py"