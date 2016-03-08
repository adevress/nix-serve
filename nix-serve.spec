# unversionned doc dir F20 change https://fedoraproject.org/wiki/Changes/UnversionedDocdirs
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}


Name:				nix-serve
Version:			2.0
Release:			1%{?dist}
Summary:			PSGI script to create nix binary cache
Group:				Applications/Internet
License:			GPLv2+
URL:				https://github.com/adevress/nix-serve
Source0:			nix-serve-2.0.tar.gz
BuildRoot:			%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:			noarch

BuildRequires:			systemd
Requires:                       perl-Plack
Requires:			nix >= 1.10
Requires(pre):			shadow-utils

%description
nix-serve provides a simple way to create nix binary repository on top of existing nix-store


%prep
%setup -q

%build

%install
rm -rf %{buildroot}
install -m 755 -D bin/nix-serve %{buildroot}/%{_bindir}/nix-serve
install -m 755 -D nix-serve.psgi %{buildroot}/%{_libexecdir}/nix-serve/nix-serve.psgi
install -m 755 -D dist/nix-serve.service %{buildroot}/%{_unitdir}/nix-serve.service


%pre
useradd --system nix-serve &> /dev/null || true

%post
%systemd_post nix-serve.service

%preun
%systemd_preun nix-serve.service

%postun
%systemd_postun_with_restart nix-serve.service
 

%files
%defattr (-,root,root)
%{_bindir}/*
%{_libexecdir}/*
%{_unitdir}/*

%changelog
* Tue Mar 08 2016 Adrien Devresse <adevress at epfl.ch> - 2.0-1
 - Initial version

