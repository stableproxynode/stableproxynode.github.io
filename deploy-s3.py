#!/usr/bin/env python3
"""
Заливка index.html в S3-хранилище Timeweb (статический сайт).

Ключи берутся из переменных окружения, НЕ хранятся в коде:
    TW_S3_KEY     — Access Key хранилища
    TW_S3_SECRET  — Secret Key хранилища

Запуск:
    TW_S3_KEY=... TW_S3_SECRET=... python3 deploy-s3.py
"""
import os, sys, hashlib, hmac, datetime, urllib.request

ACCESS = os.environ.get("TW_S3_KEY")
SECRET = os.environ.get("TW_S3_SECRET")
HOST   = "s3.twcstorage.ru"
REGION = "ru-1"
SERVICE= "s3"
BUCKET = "stableproxynode"
KEY    = "index.html"
FILE   = os.path.join(os.path.dirname(__file__), "index.html")

if not ACCESS or not SECRET:
    sys.exit("Задай TW_S3_KEY и TW_S3_SECRET в переменных окружения.")

with open(FILE, "rb") as f:
    body = f.read()

sha256 = lambda b: hashlib.sha256(b).hexdigest()
hm = lambda k, m: hmac.new(k, m.encode(), hashlib.sha256).digest()

now = datetime.datetime.now(datetime.UTC)
amzdate, datestamp = now.strftime("%Y%m%dT%H%M%SZ"), now.strftime("%Y%m%d")
uri = f"/{BUCKET}/{KEY}"
ph = sha256(body)
ch = f"host:{HOST}\nx-amz-acl:public-read\nx-amz-content-sha256:{ph}\nx-amz-date:{amzdate}\n"
sh = "host;x-amz-acl;x-amz-content-sha256;x-amz-date"
creq = f"PUT\n{uri}\n\n{ch}\n{sh}\n{ph}"
scope = f"{datestamp}/{REGION}/{SERVICE}/aws4_request"
sts = f"AWS4-HMAC-SHA256\n{amzdate}\n{scope}\n{sha256(creq.encode())}"
ks = hm(hm(hm(hm(("AWS4"+SECRET).encode(), datestamp), REGION), SERVICE), "aws4_request")
sig = hmac.new(ks, sts.encode(), hashlib.sha256).hexdigest()
auth = f"AWS4-HMAC-SHA256 Credential={ACCESS}/{scope}, SignedHeaders={sh}, Signature={sig}"

req = urllib.request.Request(f"https://{HOST}{uri}", data=body, method="PUT")
for k, v in {"Host": HOST, "x-amz-acl": "public-read", "x-amz-content-sha256": ph,
             "x-amz-date": amzdate, "Authorization": auth,
             "Content-Type": "text/html; charset=utf-8"}.items():
    req.add_header(k, v)

r = urllib.request.urlopen(req)  # обычная проверка TLS-сертификата
print(f"OK {r.status} -> https://{BUCKET}.s3.twcstorage.ru/index.html")
