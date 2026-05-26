# SPECS — RPM Spec Files pour openSUSE Tumbleweed

Dépôt de fichiers `.spec` pour construire des paquets RPM notamment des outils de développement AI et cloud sur openSUSE Tumbleweed (x86_64).

## Utilisation

```bash
# Télécharger les sources
spectool -g -R SPECS/<paquet>.spec

# Construire le RPM
rpmbuild -bb SPECS/<paquet>.spec
```

## Structure

Tous les specs repackagent des binaires pré-compilés (pas de compilation depuis les sources). Les symboles de debug et le stripping sont désactivés (`%global debug_package %{nil}`).

## Remarques
Pour kiro-cli il y a un problème avec la librairie libcurl4, veuillez accepter le cassage des liens avec zypper install


## Auteur

VGib
