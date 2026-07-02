%global pkgname kiro-cli
%global pkgver  2.10.0
%global pkgrel  1

Name:           %{pkgname}
Version:        %{pkgver}
Release:        %{pkgrel}%{?dist}
Summary:        Prompt to code to deployment in your terminal
Group:          Applications/System
License:        Commercial (AWS Intellectual Property License / Service Terms)
URL:            https://kiro.dev/cli/

# Définition des sources pour spectool
Source1:        https://desktop-release.q.us-east-1.amazonaws.com/%{version}/kirocli-x86_64-linux.tar.zst

BuildRequires:  sed
Requires:       glibc gcc bash
Conflicts:      amazon-q

# On restreint aux architectures supportées par l'application
ExclusiveArch:  x86_64

# Désactiver l'extraction des symboles de debug (équivalent à !debug dans Arch)
%global debug_package %{nil}

%description
Prompt to code to deployment in your terminal.
By downloading and using Kiro CLI, you agree to the AWS Customer Agreement, 
AWS Intellectual Property License, Service Terms, and Privacy Notice.

%prep
# On extrait la bonne archive selon l'architecture cible
%setup -q -c -T -a 1


# Copie de la licence dans le dossier de build

# Application du correctif dans les scripts (équivalent du prepare Arch)
cd kirocli/bin
sed -i 's|\$HOME/.local/bin/kiro-cli|%{_bindir}/kiro-cli|g' q qchat

%build
cd kirocli
mkdir completions
./bin/kiro-cli completion bash > completions/kiro-cli
./bin/kiro-cli completion zsh > completions/_kiro-cli
./bin/kiro-cli completion fish > completions/kiro-cli.fish

%install
rm -rf %{buildroot}
cd kirocli

# Installation des exécutables
install -Dm755 bin/kiro-cli -t %{buildroot}%{_bindir}
install -Dm755 bin/kiro-cli-chat -t %{buildroot}%{_bindir}
install -Dm755 bin/kiro-cli-term -t %{buildroot}%{_bindir}
install -Dm755 bin/q -t %{buildroot}%{_bindir}

# Installation des complétions shell
install -Dm644 completions/kiro-cli -t %{buildroot}%{_datadir}/bash-completion/completions
install -Dm644 completions/_kiro-cli -t %{buildroot}%{_datadir}/zsh/site-functions
install -Dm644 completions/kiro-cli.fish -t %{buildroot}%{_datadir}/fish/vendor_completions.d


%files
%{_bindir}/kiro-cli
%{_bindir}/kiro-cli-chat
%{_bindir}/kiro-cli-term
%{_bindir}/q
%{_datadir}/bash-completion/completions/kiro-cli
%{_datadir}/zsh/site-functions/_kiro-cli
%{_datadir}/fish/vendor_completions.d/kiro-cli.fish

%changelog
* Tue May 26 2026 AlphaLynx <alphalynx at alphalynx dot dev> - 2.4.1-1
- Initial RPM release translated from Arch Linux PKGBUILD
