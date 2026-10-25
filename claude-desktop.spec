#
# spec file for package claude-desktop
#

%define _build_id_links none
# Désactive la compression/strip des binaires pré-compilés (Electron)
%global __os_install_post %{nil}

Name:           claude-desktop
Version:        3.6556.2
Release:        1%{?dist}
Summary:        Official Claude AI desktop app from Anthropic — Chat, Cowork, and Claude Code

License:        Proprietary
URL:            https://claude.com/download
Source0:        https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/%{name}/%{name}_%{version}_amd64.deb

BuildRequires:  binutils
BuildRequires:  tar
BuildRequires:  coreutils

# Dépendances traduites pour openSUSE
Requires:       alsa-lib
Requires:       libAtkSpire0 or at-spi2-core
Requires:       bubblewrap
Requires:       libcairo2
Requires:       dbus-1
Requires:       libexpat1
Requires:       gcc-libs
Requires:       glib2
Requires:       glibc
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       libcap-ng0
Requires:       libcups2
Requires:       libdrm2
Requires:       libnotify4
Requires:       libpipewire-0_3-0
Requires:       libseccomp1
Requires:       libsecret-1-0
Requires:       libX11-6
Requires:       libxcb1
Requires:       libXcomposite1
Requires:       libXdamage1
Requires:       libXext6
Requires:       libXfixes3
Requires:       libxkbcommon0
Requires:       libXrandr2
Requires:       libXtst6
Requires:       Mesa
Requires:       libnspr4
Requires:       libnss3
Requires:       pango
Requires:       socat
Requires:       systemd
Requires:       util-linux-libs
Requires:       virtiofsd
Requires:       xdg-desktop-portal
Requires:       xdg-utils

# Dépendances conditionnelles pour la machine virtuelle Cowork (uniquement x86_64)
%ifarch x86_64
Requires:       qemu-x86
Requires:       edk2-ovmf
%endif

# Sur aarch64, QEMU et l'EDK2 restent optionnels ou gérés à la volée
%ifarch aarch64
Recommends:     qemu-arm
Recommends:     edk2-aarch64
%endif

Recommends:     gnome-keyring
Recommends:     kwalletcli
Recommends:     libayatana-appindicator3-1
Recommends:     openssh
Recommends:     xdg-desktop-portal-gtk
Recommends:     xdg-desktop-portal-kde

Conflicts:      claude
Conflicts:      claude-desktop-bin

%description
Official Claude AI desktop app from Anthropic — Chat, Cowork, and Claude Code.
Repackaged from Anthropic's official Debian distribution.

%build
# Aucun build nécessaire (paquet binaire pré-compilé)

%install

# Extraction du paquet .deb selon l'architecture
ar x %{SOURCE0}

# Extraction du payload data.tar.xz directement dans le dossier racine RPM
cd  %{buildroot}

tar -xf %{builddir}/data.tar.xz 

# Configuration du sandbox chrome-sandbox (setuid root)
chmod 4755 %{buildroot}/usr/lib/claude-desktop/chrome-sandbox

# Suppression des fichiers spécifiques à Debian/Lintian inutiles sous openSUSE
rm -rf %{buildroot}/usr/share/lintian

# --- Correctifs de compatibilité Cowork -----------------------------------
# virtiofsd : Debian le place dans /usr/bin, openSUSE dans /usr/libexec ou /usr/bin selon la version
ln -s ../lib/virtiofsd %{buildroot}/usr/bin/virtiofsd || ln -s ../libexec/virtiofsd %{buildroot}/usr/bin/virtiofsd || true


# Licence
mkdir -p %{buildroot}/usr/share/licenses/%{name}
if [ -f %{buildroot}/usr/share/doc/claude-desktop/copyright ]; then
    mv %{buildroot}/usr/share/doc/claude-desktop/copyright %{buildroot}/usr/share/licenses/%{name}/LICENSE
fi

%files
%defattr(-,root,root,-)
/usr/bin/claude-desktop
/usr/lib/claude-desktop/
/usr/share/applications/
/usr/share/licenses
/usr/share/icons/
/usr/share/doc
/usr/share/applications/
%if 0%{?_licensedir:1}
%license /usr/share/licenses/%{name}/LICENSE
%endif
%ghost /usr/bin/virtiofsd
