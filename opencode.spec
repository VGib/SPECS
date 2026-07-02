Name:           opencode
Version:        1.17.13
Release:        1%{?dist}
Summary:        The AI coding agent built for the terminal

License:        MIT
URL:            https://github.com/anomalyco/opencode

# Définition des sources par architecture pour spectool
Source0:        https://github.com/anomalyco/opencode/releases/download/v%{version}/opencode-linux-x64.tar.gz

# Correspondance avec le 'depends' du PKGBUILD
Requires:       ripgrep

# On indique à RPM qu'on ne compile rien (ce sont déjà des binaires)
# et qu'il ne faut pas chercher à générer des paquets de debug ou "stripper" le binaire
%global debug_package %{nil}
%global __os_install_post %{nil}

# Limité aux architectures supportées
ExclusiveArch:  x86_64

%description
The AI coding agent built for the terminal. Distributed as a pre-compiled binary.

%prep
# On crée manuellement le dossier source car le tar.gz n'a pas forcément de dossier racine standard
%setup -q -c -T

# Selon l'architecture de build, on extrait la bonne source
tar -xzf  %{SOURCE0} 


%build
# Rien à compiler ici, c'est du pré-compilé (-bin)

%install
# Création du dossier de destination /usr/bin/
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}

# Installation du binaire avec les bons droits (équivalent de install -Dm755)
install -m 0755 opencode %{buildroot}%{_bindir}/opencode

%files
%{_bindir}/opencode

%changelog
* Sat May 23 2026 dax/adam <contact@example.com> - 1.14.28-1
- Initial release port from Arch Linux PKGBUILD