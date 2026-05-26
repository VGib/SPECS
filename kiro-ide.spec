# Désactive l'extraction des symboles de débogage (indispensable pour Electron/Chromium pré-compilé)
%global debug_package %{nil}
%global __strip /bin/true

Name:           kiro-ide
Version:        0.12.200
Release:        1
Epoch:          1
Summary:        An agentic AI IDE with spec-driven development from prototype to production

License:        Commercial
Group:          Development/Tools/IDE
URL:            https://kiro.dev/
%define x_baseurl https://prod.download.desktop.kiro.dev/releases/stable/linux-x64/signed/%{version}

Source0:        %{x_baseurl}/deb/%{name}-%{version}-stable-linux-x64.deb

# --- DÉPENDANCES POUR LA CRÉATION DU RPM (BUILD) ---
BuildRequires:  binutils
BuildRequires:  openssl
BuildRequires:  sed
# ---------------------------------------------------

# Dépendances d'exécution adaptées pour openSUSE
Requires:       alsa
Requires:       atk
Requires:       bash
Requires:       cairo
Requires:       libcurl4 
Requires:       dbus-1
Requires:       glibc
Requires:       gtk3
Requires:       libX11-6
Requires:       libXcomposite1
Requires:       libXdamage1
Requires:       libXext6
Requires:       libXfixes3
Requires:       libXrandr2
Requires:       libcups2
Requires:       libexpat1
Requires:       libgcc_s1
Requires:       libglib-2_0-0
Requires:       libnspr4
Requires:       libnss3
Requires:       libopenssl3
Requires:       libpango-1_0-0
Requires:       libsecret-1-0
Requires:       libsoup-3_0-0
Requires:       libstdc++6
Requires:       libxcb1
Requires:       libxkbcommon0
Requires:       libxkbfile1
Requires:       systemd

Conflicts:      kiro

%description
An agentic AI IDE with spec-driven development from prototype to production.

%prep
# Crée le répertoire de build et s'y déplace
%setup -c -T


# 2. Utilisation de 'ar' (fourni par binutils) pour extraire le .deb
ar x %{SOURCE0} data.tar.xz
tar -xpf data.tar.xz

# 3. Supprime les binaires multi-plateforme inutiles (arm64, darwin, win32)
rm -rf usr/share/kiro/resources/app/extensions/kiro.kiro-agent/node_modules/onnxruntime-node/bin/napi-v3/darwin
rm -rf usr/share/kiro/resources/app/extensions/kiro.kiro-agent/node_modules/onnxruntime-node/bin/napi-v3/linux/arm64
rm -rf usr/share/kiro/resources/app/extensions/kiro.kiro-agent/node_modules/onnxruntime-node/bin/napi-v3/win32
find . -name "*win32-arm64*" -delete

# 4. Correction des chemins dans les fichiers .desktop
sed -i -e 's|/usr/share/kiro|/opt/Kiro|g' -e 's|Icon=code-oss|Icon=kiro|g' \
    usr/share/applications/*.desktop

%build
# Rien à compiler (binaire pré-compilé)

%install
# Préparation de l'arborescence dans le répertoire temporaire de build
mkdir -p %{buildroot}/opt/Kiro
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/licenses/%{name}
mkdir -p %{buildroot}%{_datadir}/metainfo
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/pixmaps
mkdir -p %{buildroot}%{_datadir}/mime/packages
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
mkdir -p %{buildroot}%{_datadir}/zsh/site-functions

# Copie des fichiers de l'application
cp -a usr/share/kiro/* %{buildroot}/opt/Kiro/

# Lien symbolique pour lancer l'IDE depuis le PATH
ln -s /opt/Kiro/bin/kiro %{buildroot}%{_bindir}/kiro


# Intégration système (Desktop, icônes, complétion)
install -m 0644 usr/share/appdata/kiro.appdata.xml %{buildroot}%{_datadir}/metainfo/
install -m 0644 usr/share/applications/kiro.desktop %{buildroot}%{_datadir}/applications/
install -m 0644 usr/share/applications/kiro-url-handler.desktop %{buildroot}%{_datadir}/applications/
install -m 0644 usr/share/pixmaps/code-oss.png %{buildroot}%{_datadir}/pixmaps/kiro.png
install -m 0644 usr/share/mime/packages/kiro-workspace.xml %{buildroot}%{_datadir}/mime/packages/
install -m 0644 usr/share/bash-completion/completions/kiro %{buildroot}%{_datadir}/bash-completion/completions/
install -m 0644 usr/share/zsh/vendor-completions/_kiro %{buildroot}%{_datadir}/zsh/site-functions/

%files
/opt/Kiro/
%{_bindir}/kiro
%{_datadir}/licenses/%{name}/
%{_datadir}/metainfo/kiro.appdata.xml
%{_datadir}/applications/kiro.desktop
%{_datadir}/applications/kiro-url-handler.desktop
%{_datadir}/pixmaps/kiro.png
%{_datadir}/mime/packages/kiro-workspace.xml
%{_datadir}/bash-completion/completions/kiro
%{_datadir}/zsh/site-functions/_kiro

%changelog
* Wed May 20 2026 AlphaLynx <alphalynx@alphalynx.dev> - 1:0.12.200-1
- Updated spec file with explicit binutils BuildRequires for openSUSE compatibility
