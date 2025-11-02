# scripts/generate_datapackage.py
"""
Script para gerar automaticamente datapackage.json e datapackage.yaml
a partir dos CSVs da pasta data/ no repositório:
https://github.com/vivigoncalvesportonascimento/painel-secom-vivi
"""

from pathlib import Path
from frictionless import Resource
import yaml
import json

# Caminhos
DATA_DIR = Path("data")
OUT_JSON = Path("datapackage.json")
OUT_YAML = Path("datapackage.yaml")

def make_resource_from_csv(csv_path: Path):
    """Cria um resource Frictionless e infere o schema de um CSV."""
    print(f"🔍 Processando: {csv_path.name}")
    resource = Resource(path=str(csv_path))
    resource.infer()
    resource.name = csv_path.stem
    return resource

def main():
    print("🚀 Gerando datapackage para o repositório 'painel-secom-vivi'...")

    csv_files = sorted(DATA_DIR.glob("*.csv"))
    if not csv_files:
        print("⚠️ Nenhum arquivo CSV encontrado na pasta data/")
        return

    resources = []
    for csv_path in csv_files:
        resource = make_resource_from_csv(csv_path)
        resources.append(resource.to_descriptor())

    datapackage_descriptor = {
        "name": "painel-secom-vivi",
        "title": "Painel SECOM - Dados transformados",
        "description": (
            "Pacote de dados contendo os CSVs transformados do projeto "
            "Painel SECOM (repositório vivigoncalvesportonascimento/painel-secom-vivi)."
        ),
        "homepage": "https://github.com/vivigoncalvesportonascimento/painel-secom-vivi",
        "resources": resources,
    }

    # Salvar JSON
    with OUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(datapackage_descriptor, f, indent=2, ensure_ascii=False)
    print(f"💾 Criado: {OUT_JSON}")

    # Salvar YAML
    with OUT_YAML.open("w", encoding="utf-8") as f:
        yaml.safe_dump(datapackage_descriptor, f, sort_keys=False, allow_unicode=True)
    print(f"💾 Criado: {OUT_YAML}")

    print("✅ Geração concluída!")

if __name__ == "__main__":
    main()
