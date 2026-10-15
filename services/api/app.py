# API de consulta local de afiliados
# API de consulta local de afiliados
import json, logging, os, re, sys, csv
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)s [cierre-api] %(message)s")
log = logging.getLogger("cierre-api")
ROUTE = re.compile(r"^/afiliados/([0-9]+)$")

def find_member(documento):
    empresas = {}
    try:
        with open('/data/EMPRESA.csv', 'r', encoding='utf-8') as f:
            for r in csv.DictReader(f): empresas[r['COD_EMP']] = r['NOM_EMP']
        with open('/data/AFI_MAE.csv', 'r', encoding='utf-8') as f:
            for r in csv.DictReader(f):
                if r['NRO_DOC'] == documento:
                    nom = " ".join([x for x in (r['NOM1'], r['NOM2'], r['APE1'], r['APE2']) if x.strip()])
                    est = "ACTIVO" if r['EST_AFI'] == 'A' else ("INACTIVO" if r['EST_AFI'] == 'I' else "DESCONOCIDO")
                    return {"documento": documento, "nombre": nom, "estado": est, "empresa": empresas.get(r['COD_EMP'], "")}
    except Exception as e:
        log.error("Error CSV: %s", e)
    return None

class Handler(BaseHTTPRequestHandler):
    def _send(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health": return self._send(200, {"status": "UP"})
        match = ROUTE.match(self.path)
        if not match: return self._send(404, {"error": "ruta no encontrada"})
        documento = match.group(1)
        member = find_member(documento)
        if member is None: return self._send(404, {"error": "afiliado no encontrado"})
        log.info("GET /afiliados/%s 200", documento)
        return self._send(200, member)
    def log_message(self, fmt, *args): return

if __name__ == "__main__":
    port = int(os.environ.get("API_PORT", "8081"))
    log.info("cierre-api activo en puerto %s (modo CSV local)", port)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
