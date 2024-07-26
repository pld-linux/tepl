#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
#
Summary:	Tepl - Text editor product line
Summary(pl.UTF-8):	Tepl (Text editor product line) - linia produkcyjna edytorów
Name:		tepl
Version:	6.8.0
Release:	2
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://download.gnome.org/sources/tepl/6.8/%{name}-%{version}.tar.xz
# Source0-md5:	5d29b2c9032a1ba2d33ef9c9c9c7de79
URL:		https://wiki.gnome.org/Projects/Tepl
BuildRequires:	gettext-tools >= 0.19.6
BuildRequires:	glib2-devel >= 1:2.74
BuildRequires:	gobject-introspection-devel >= 1.42.0
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk+3-devel >= 3.22
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.25}
BuildRequires:	libgedit-amtk-devel >= 5.8
BuildRequires:	libgedit-gtksourceview-devel >= 299.0.4
BuildRequires:	libicu-devel
BuildRequires:	libxml2-devel >= 1:2.5
BuildRequires:	meson >= 0.64
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
#BuildRequires:	vala
Requires:	glib2 >= 1:2.74
Requires:	gtk+3 >= 3.22
Requires:	libgedit-gtksourceview >= 299.0.4
Requires:	libxml2 >= 1:2.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tepl is a library that eases the development of GtkSourceView-based
text editors and IDEs.

Tepl was previously named Gtef (GTK+ text editor framework). The
project has been renamed in June 2017 to have a more beautiful name.

%description -l pl.UTF-8
Tepl to biblioteka ułatawiająca tworzenie edytorów tekstu i IDE
opartych na GtkSourceView.

Tepl wcześniej nazywał się Gtef (GTK+ text editor framework - skielet
edytorów tekstu GTK+); nazwa została zmieniona w czerwcu 2017 na
ładniej brzmiącą.

%package devel
Summary:	Header files for Tepl library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Tepl
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.74
Requires:	gsettings-desktop-schemas-devel
Requires:	gtk+3-devel >= 3.22
Requires:	libgedit-amtk-devel >= 5.8
Requires:	libgedit-gtksourceview-devel >= 299.0.4
Requires:	libicu-devel
Requires:	libxml2-devel >= 1:2.5
# temporary? no vapi in 2.99.2
Obsoletes:	vala-tepl < 2.99.2

%description devel
Header files for Tepl library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Tepl.

%package static
Summary:	Static Tepl library
Summary(pl.UTF-8):	Statyczna biblioteka Tepl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Tepl library.

%description static -l pl.UTF-8
Statyczna biblioteka Tepl.

%package -n vala-tepl
Summary:	Vala API for Tepl library
Summary(pl.UTF-8):	API języka Vala do biblioteki Tepl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala
BuildArch:	noarch

%description -n vala-tepl
Vala API for Tepl library.

%description -n vala-tepl -l pl.UTF-8
API języka Vala do biblioteki Tepl.

%package apidocs
Summary:	API documentation for Tepl library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Tepl
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Tepl library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Tepl.

%prep
%setup -q

%build
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	%{?with_apidocs:-Dgtk_doc=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%find_lang tepl-6

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f tepl-6.lang
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_libdir}/libtepl-6.so.4
%{_libdir}/girepository-1.0/Tepl-6.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtepl-6.so
%{_includedir}/tepl-6
%{_datadir}/gir-1.0/Tepl-6.gir
%{_pkgconfigdir}/tepl-6.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libtepl-6.a
%endif

%if 0
%files -n vala-tepl
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/tepl-6.deps
%{_datadir}/vala/vapi/tepl-6.vapi
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/tepl-6
%endif
