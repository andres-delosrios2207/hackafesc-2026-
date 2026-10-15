# HackaFESC 2026 - Procesamiento de datos
# HackaFESC 2026 - Procesamiento de datos
import csv, os, re
from collections import defaultdict
from datetime import datetime

os.makedirs('output', exist_ok=True)

def norm_date(f):
    f = f.strip()
    if re.match(r'^\d{4}-\d{2}-\d{2}$', f):
        try: datetime.strptime(f, "%Y-%m-%d"); return f
        except: return None
    m = re.match(r'^(\d{2})/(\d{2})/(\d{4})$', f)
    if m:
        try: return datetime.strptime(f, "%d/%m/%Y").strftime("%Y-%m-%d")
        except: return None
    m = re.match(r'^(\d{4})(\d{2})(\d{2})$', f)
    if m:
        try: return datetime.strptime(f, "%Y%m%d").strftime("%Y-%m-%d")
        except: return None
    return None

empresas = {}
with open('data/EMPRESA.csv', 'r', encoding='utf-8') as f:
    for r in csv.DictReader(f): empresas[r['COD_EMP']] = r['NOM_EMP']

aportes = defaultdict(list)
with open('data/APORTES.csv', 'r', encoding='utf-8') as f:
    for r in csv.DictReader(f): aportes[r['NRO_DOC']].append(r['PERIODO'])

oriente = {}
with open('data/extracto_caja_oriente.csv', 'r', encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter=';'):
        oriente[str(int(r['id_afiliado']))] = r['situacion']

ben_counts = defaultdict(int)
with open('data/AFI_BEN.csv', 'r', encoding='utf-8') as f:
    for r in csv.DictReader(f): ben_counts[r['NRO_DOC_AFI']] += 1

afi_docs = set()
with open('data/AFI_MAE.csv', 'r', encoding='utf-8') as f:
    for r in csv.DictReader(f): afi_docs.add(r['NRO_DOC'])

excepciones = []
with open('data/AFI_BEN.csv', 'r', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['NRO_DOC_AFI'] not in afi_docs:
            excepciones.append([r['NRO_DOC_BEN'], 'BENEFICIARIO_HUERFANO', 'Titular no existe en maestro'])

for doc, sit in oriente.items():
    if doc not in afi_docs:
        excepciones.append([doc, 'CRUCE_NO_COINCIDE', 'No existe en nuestra base'])

activos = []
inactivos = 0
vistos = set()
dup_rep = set()

with open('data/AFI_MAE.csv', 'r', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        doc = r['NRO_DOC']
        if doc in vistos:
            if doc not in dup_rep:
                excepciones.append([doc, 'DUPLICADO', 'Aparece mas de una vez'])
                dup_rep.add(doc)
            continue
        vistos.add(doc)

        if not norm_date(r['FEC_AFI']):
            excepciones.append([doc, 'FECHA_INVALIDA', 'Fecha no reconocida'])
        
        est = r['EST_AFI']
        if est not in ('A', 'I'):
            excepciones.append([doc, 'CODIGO_INVALIDO', 'Estado diferente de A o I'])
            continue

        cod_emp = r['COD_EMP']
        if est == 'A' and cod_emp not in empresas:
            excepciones.append([doc, 'SIN_EMPRESA', 'Sin empresa asociada'])
            continue

        if doc in oriente:
            sit = oriente[doc]
            if (est == 'A' and sit != 'VIGENTE') or (est == 'I' and sit == 'VIGENTE'):
                excepciones.append([doc, 'CRUCE_NO_COINCIDE', 'Discrepancia de estado'])
        
        if est == 'A':
            nom = " ".join([x for x in (r['NOM1'], r['NOM2'], r['APE1'], r['APE2']) if x.strip()])
            ult_ap = max(aportes[doc]) if doc in aportes else ''
            activos.append([doc, nom, 'ACTIVO', cod_emp, empresas[cod_emp], ben_counts[doc], ult_ap])
        else:
            inactivos += 1

with open('output/afiliados_activos.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['documento','nombre','estado','cod_empresa','empresa','beneficiarios','ultimo_aporte'])
    w.writerows(activos)

with open('output/excepciones.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['documento','tipo','detalle'])
    w.writerows(excepciones)

with open('output/totales.txt', 'w', encoding='utf-8') as f:
    f.write(f"total_afiliados={len(vistos)}\nactivos={len(activos)}\ninactivos={inactivos}\nexcepciones={len(excepciones)}\n")
