"""Gera o source.json que o SideStore le para listar e atualizar o app.

Roda no final do workflow, com o .ipa ja empacotado. A URL aponta para a
tag exata daquele build — nao para 'latest', que neste repositorio e
disputada com a release 'apk' do workflow de Android.

Schema: https://faq.altstore.io/developers/make-a-source
"""
import datetime
import json
import os
import sys

ipa = os.environ["IPA_NAME"]
if not os.path.exists(ipa):
    sys.exit("sem .ipa — source.json nao gerado")

repo = os.environ["REPO"]           # ex.: isabellaR-a6/vale-do-girassol
tag = os.environ["TAG"]             # ex.: build-4
build = tag.rsplit("-", 1)[-1]

fonte = {
    "name": os.environ["SOURCE_NOME"],
    "identifier": os.environ["SOURCE_ID"],
    "subtitle": "Jogos feitos pela Isabella",
    "apps": [
        {
            "name": os.environ["APP_NOME"],
            "bundleIdentifier": os.environ["APP_BUNDLE_ID"],
            "developerName": "Isabella Radael",
            "subtitle": os.environ["APP_SUBTITULO"],
            "localizedDescription": os.environ["APP_DESCRICAO"],
            "iconURL": os.environ["APP_ICONE_URL"],
            "appPermissions": {"entitlements": [], "privacy": {}},
            "versions": [
                {
                    # o build entra na versao para o SideStore enxergar
                    # cada compilacao nova como atualizacao
                    "version": f"1.0.{build}",
                    "buildVersion": build,
                    "date": datetime.date.today().isoformat(),
                    "downloadURL": (
                        f"https://github.com/{repo}/releases/download/{tag}/{ipa}"
                    ),
                    "size": os.path.getsize(ipa),
                    "localizedDescription": f"Build {build}.",
                    "minOSVersion": "15.0",
                }
            ],
        }
    ],
    "news": [],
}

with open("source.json", "w", encoding="utf-8") as f:
    json.dump(fonte, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"source.json gerado: versao 1.0.{build}, {os.path.getsize(ipa)} bytes")
