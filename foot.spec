Summary:	A fast, lightweight and minimalistic Wayland terminal emulator
Name:		foot
Version:	1.10.3
Release:	1
License:	MIT
Group:		Applications/Terminal
Source0:	https://codeberg.org/dnkl/foot/archive/%{version}.tar.gz
# Source0-md5:	75e66a87d6e6e4e265d1219e459f53df
URL:		https://codeberg.org/dnkl/foot/
BuildRequires:	fcft-devel < 3.0.0
BuildRequires:	fcft-devel >= 2.4.0
BuildRequires:	fontconfig-devel
BuildRequires:	libutf8proc-devel
BuildRequires:	meson >= 0.54.0
BuildRequires:	ninja
BuildRequires:	pixman-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	scdoc
BuildRequires:	tllist-devel >= 1.0.4
BuildRequires:	wayland-devel
BuildRequires:	wayland-protocols >= 1.21
BuildRequires:	xorg-lib-libxkbcommon-devel >= 1.0.0
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires:	fcft < 3.0.0
Requires:	fcft >= 2.4.0
Requires:	hicolor-icon-theme
Requires:	terminfo-foot = %{version}-%{release}
Requires:	xorg-lib-libxkbcommon >= 1.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A fast, lightweight and minimalistic Wayland terminal emulator.

%package -n terminfo-foot
Summary:	terminfo database entries for foot terminal emulator
Requires:	terminfo
BuildArch:	noarch

%description -n terminfo-foot
terminfo database entries for foot terminal emulator.

%package -n bash-completion-foot
Summary:	Bash completion for foot command line
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
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
%setup -q -n %{name}

%build
%meson build
%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_icon_cache hicolor

%postun
%update_desktop_database_postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md
%attr(755,root,root) %{_bindir}/foot
%attr(755,root,root) %{_bindir}/footclient
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

%files -n terminfo-foot
%defattr(644,root,root,755)
%{_datadir}/terminfo/f/foot
%{_datadir}/terminfo/f/foot-direct

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
