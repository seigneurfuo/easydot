# fedpkg --release f40 local

Name:           easydot
Version:        0.2.3
Release:        %autorelease
BuildArch:      noarch
Summary:        Un gestionnaire de fichiers de configuration

License:        None
URL:            https://seigneurfuo.com

Requires:       python3
Requires:       python3-PyQt6

%description
Un gestionnaire de fichiers de configuration

%install

# Programme
mkdir -p %{buildroot}/opt/%{name}-gui

install -m 755 ../../%{name}.py %{buildroot}/opt/%{name}-gui/%{name}.py
install -m 755 ../../%{name}-gui.py %{buildroot}/opt/%{name}-gui/%{name}-gui.py
install -m 644 ../../mainwindow.ui %{buildroot}/opt/%{name}-gui/mainwindow.ui

install -m 644 ../../README.md %{buildroot}/opt/%{name}-gui/README.md

# Racourci
mkdir -p "%{buildroot}/usr/share/applications"
install -m 644 ./%{name}-gui.desktop %{buildroot}/usr/share/applications/%{name}-gui.desktop

%files
/opt/%{name}-gui/%{name}.py
/opt/%{name}-gui/%{name}-gui.py

/opt/%{name}-gui/mainwindow.ui
/opt/%{name}-gui/README.md

/usr/share/applications/%{name}-gui.desktop
