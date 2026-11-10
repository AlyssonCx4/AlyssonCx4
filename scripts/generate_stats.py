#!/usr/bin/env python3
"""Preenche os campos dinâmicos do banner do perfil.

Lê assets/banner.svg, busca os números atuais na API GraphQL do GitHub e
substitui os marcadores {{...}} que estão no arquivo. O resultado vai para
output/banner.svg, que é o arquivo versionado e exibido no README.

Os números são consultados dentro do workflow, por isso o SVG commitado
não depende de nenhum serviço externo no ar.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone

QUERY = """
query($login: String!) {
  user(login: $login) {
    login
    repositories(privacy: PUBLIC, ownerAffiliations: OWNER) { totalCount }
    followers { totalCount }
    contributionsCollection {
      contributionCalendar { totalContributions }
    }
  }
}
"""

SOURCE = "assets/banner.svg"
TARGET = "output/banner.svg"


def fetch(login):
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        try:
            import urllib.request
            req = urllib.request.Request(
                "https://api.github.com/graphql",
                data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                    "User-Agent": "AlyssonCx4-Profile-Workflow",
                },
            )
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if "errors" in data:
                    sys.exit(f"erro da API GraphQL: {data['errors']}")
                return data["data"]["user"]
        except Exception as err:
            print(f"aviso: erro com urllib: {err}, tentando gh cli...", file=sys.stderr)

    try:
        out = subprocess.run(
            ["gh", "api", "graphql", "-f", f"query={QUERY}", "-f", f"login={login}"],
            capture_output=True, text=True, check=True,
        )
        data = json.loads(out.stdout)
        if "errors" in data:
            sys.exit(f"erro da API GraphQL: {data['errors']}")
        return data["data"]["user"]
    except Exception as err:
        sys.exit(f"erro ao consultar API do GitHub via gh CLI e urllib: {err}")


def build_values(user):
    contributions = user["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    return {
        "PUBLIC_REPOS": str(user["repositories"]["totalCount"]),
        "FOLLOWERS": str(user["followers"]["totalCount"]),
        "CONTRIBUTIONS": str(contributions),
        "UPDATED_AT": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    }


def main():
    login = os.environ.get("GITHUB_LOGIN", "AlyssonCx4")
    os.makedirs("output", exist_ok=True)

    with open(SOURCE, encoding="utf-8") as fh:
        svg = fh.read()

    user_data = fetch(login)
    for key, value in build_values(user_data).items():
        svg = svg.replace(f"{{{{{key}}}}}", value)

    left = [k for k in ("PUBLIC_REPOS", "FOLLOWERS",
                        "CONTRIBUTIONS", "UPDATED_AT") if f"{{{{{k}}}}}" in svg]
    if left:
        sys.exit(f"marcadores não substituídos: {left}")

    with open(TARGET, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(f"{TARGET}: {os.path.getsize(TARGET)} bytes")


if __name__ == "__main__":
    main()

