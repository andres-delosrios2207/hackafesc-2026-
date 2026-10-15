#!/usr/bin/env bash
# Script principal de ejecucion y validacion
set -e
mkdir -p output

TOP_LINE=$(grep -h -o "codigo=CIE-[0-9]\{4\}" logs/*.log | sort | uniq -c | sort -nr | head -n 1)
COUNT=$(echo "$TOP_LINE" | awk '{print $1}')
TOP_CODE=$(echo "$TOP_LINE" | awk '{print $2}' | cut -d'=' -f2)
echo "codigo_error=$TOP_CODE" > output/top_error.txt
echo "ocurrencias=$COUNT" >> output/top_error.txt

python3 scripts/procesar.py
