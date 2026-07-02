Name:           claude-code
Version:        2.1.198
Release:        0
Summary:        An agentic coding tool that lives in your terminal
License:        Proprietary
URL:            https://github.com/anthropics/claude-code

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
Source0:        https://code.claude.com/docs/en/legal-and-compliance.md
Source1:        https://downloads.claude.ai/claude-code-releases/%{version}/linux-x64/claude

Requires:       bash
Recommends:     git-core, gh, ripgrep, tmux, bubblewrap, socat

%description
Claude Code is an agentic coding tool that lives in your terminal.
Version spécifique pour Tumbleweed x86_64.

%prep
%setup -q -c -T

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_prefix}/lib/%{name}

# Installation du binaire
install -m 755 %{_sourcedir}/claude %{buildroot}%{_prefix}/lib/%{name}/claude

# Création du wrapper
cat > %{buildroot}%{_bindir}/claude << 'EOF'
#!/bin/sh
export DISABLE_AUTOUPDATER=1
exec %{_prefix}/lib/%{name}/claude "$@"
EOF
chmod 755 %{buildroot}%{_bindir}/claude

# Licence
install -Dm 644 %{_sourcedir}/legal-and-compliance.md %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

%files
%{_bindir}/claude
%{_prefix}/lib/%{name}/
%{_datadir}/licenses/%{name}/LICENSE
