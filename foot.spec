#
# Conditional build:
%bcond_with	pgo		# disable profile guided optimizations

Summary:	A fast, lightweight and minimalistic Wayland terminal emulator
Name:		foot
Version:	1.22.0
Release:	2
License:	MIT
Group:		Applications/Terminal
Source0:	https://codeberg.org/dnkl/foot/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ffe00f17300f19bac5eb6d0f933ed3a7
Patch0:		x32.patch
Patch1:		header-gen-race.patch
URL:		https://codeberg.org/dnkl/foot/
BuildRequires:	fcft-devel < 4.0.0
BuildRequires:	fcft-devel >= 3.3.1
BuildRequires:	fontconfig-devel
BuildRequires:	libutf8proc-devel
BuildRequires:	meson >= 0.59.0
BuildRequires:	ninja
BuildRequires:	pixman-devel
BuildRequires:	pkgconfig
BuildRequires:	python3
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	scdoc
BuildRequires:	systemd-devel
BuildRequires:	tllist-devel >= 1.1.0
BuildRequires:	wayland-devel
BuildRequires:	wayland-protocols >= 1.41
BuildRequires:	xorg-lib-libxkbcommon-devel >= 1.8.0
%if %{with pgo}
BuildRequires:	cage
BuildRequires:	fonts-TTF-DejaVu
%endif
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires(post,preun):	systemd-units >= 1:250.1
Requires:	fcft < 4.0.0
Requires:	fcft >= 3.3.1
Requires:	hicolor-icon-theme
Requires:	terminfo >= 6.2.20210731
Requires:	xorg-lib-libxkbcommon >= 1.8.0
Obsoletes:	terminfo-foot < 1.10.3-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A fast, lightweight and minimalistic Wayland terminal emulator.

%package -n bash-completion-foot
Summary:	Bash completion for foot command line
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-foot
Bash completion for foot command line.

%package -n fish-completion-foot
Summary:	fish-completion for foot
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	fish
BuildArch:	noarch

%description -n fish-completion-foot
fish-completion for foot.

%description -n fish-completion-foot -l pl.UTF-8
Pakiet ten dostarcza uzupełnianie nazw w fish dla foot.

%package -n zsh-completion-foot
Summary:	ZSH completion for foot command line
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
BuildArch:	noarch

%description -n zsh-completion-foot
ZSH completion for foot command line.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%build
%meson \
	%{?with_pgo:-Db_pgo=generate} \
	-Dutmp-backend=libutempter \
	-Dutmp-default-helper-path=/usr/sbin/utempter \
	-Dterminfo=disabled

%meson_build

%if %{with pgo}
%meson_test

./pgo/full-headless-cage.sh . build

%__meson configure build \
	-Db_pgo=use

%meson_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_icon_cache hicolor
%systemd_user_post foot-server.service foot-server.socket

%preun
%systemd_user_preun foot-server.service foot-server.socket

%postun
%update_desktop_database_postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md
%dir %{_sysconfdir}/xdg/foot
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xdg/foot/foot.ini
%attr(755,root,root) %{_bindir}/foot
%attr(755,root,root) %{_bindir}/footclient
%{systemduserunitdir}/foot-server.service
%{systemduserunitdir}/foot-server.socket
%{_datadir}/foot
%{_desktopdir}/foot.desktop
%{_desktopdir}/foot-server.desktop
%{_desktopdir}/footclient.desktop
%{_iconsdir}/hicolor/*/apps/foot.png
%{_iconsdir}/hicolor/scalable/apps/foot.svg
%{_mandir}/man1/foot.1*
%{_mandir}/man1/footclient.1*
%{_mandir}/man5/foot.ini.5*
%{_mandir}/man7/foot-ctlseqs.7*

%files -n bash-completion-foot
%defattr(644,root,root,755)
%{bash_compdir}/foot
%{bash_compdir}/footclient

%files -n fish-completion-foot
%defattr(644,root,root,755)
%{fish_compdir}/foot.fish
%{fish_compdir}/footclient.fish

%files -n zsh-completion-foot
%defattr(644,root,root,755)
%{zsh_compdir}/_foot
%{zsh_compdir}/_footclient
