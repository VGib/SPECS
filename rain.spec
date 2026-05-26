Name:           rain
Version:        1.24.4
Release:        0
Summary:        Aws rain for cloudformation
License:        Proprietary
URL:            https://github.com/aws-cloudformation/rain

# 1. Restriction d'architecture
ExclusiveArch:  x86_64


# 2. Restriction à Tumbleweed (bloque si < 1550)
%if 0%{?suse_version} <= 1600
%error "Ce paquet est conçu uniquement pour openSUSE Tumbleweed."
%endif

# Empêche RPM de modifier le binaire Bun
%global __os_install_post %{nil}
%global debug_package %{nil}

# Utilisation des fichiers locaux (à télécharger avec curl au préalable)
Source0:        https://github.com/aws-cloudformation/rain/releases/download/v%{version}/rain-v%{version}_linux-amd64.zip

Requires:       bash
Recommends:     git-core, gh, ripgrep, tmux, bubblewrap, socat

%description
Claude Code is an agentic coding tool that lives in your terminal.
Version spécifique pour Tumbleweed x86_64.

%prep
%setup -q -c -n %{name}-%{version}

%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 rain-v%{version}_linux-amd64/rain %{buildroot}%{_bindir}/rain

%files
%{_bindir}/rain
