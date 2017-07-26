#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Tepl - Text editor product line
Summary(pl.UTF-8):	Tepl (Text editor product line) - linia produkcyjna edytorów
Name:		tepl
Version:	2.99.2
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/tepl/2.99/%{name}-%{version}.tar.xz
# Source0-md5:	2340f04086fdd565925c97da0f880ffa
URL:		https://wiki.gnome.org/Projects/Tepl
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.14
BuildRequires:	gettext-tools >= 0.19.4
BuildRequires:	glib2-devel >= 1:2.52
BuildRequires:	gobject-introspection-devel >= 1.42.0
BuildRequires:	gtk+3-devel >= 3.20
BuildRequires:	gtk-doc >= 1.25
BuildRequires:	gtksourceview3-devel >= 3.22
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxml2-devel >= 1:2.5
BuildRequires:	pkgconfig
BuildRequires:	uchardet-devel
#BuildRequires:	vala
Requires:	glib2 >= 1:2.52
Requires:	gtk+3 >= 3.20
Requires:	gtksourceview3 >= 3.22
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
Requires:	glib2-devel >= 1:2.52
Requires:	gtk+3-devel >= 3.20
Requires:	gtksourceview3-devel >= 3.22
Requires:	libxml2-devel >= 1:2.5
Requires:	uchardet-devel
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

%description -n vala-tepl
Vala API for Tepl library.

%description -n vala-tepl -l pl.UTF-8
API języka Vala do biblioteki Tepl.

%package apidocs
Summary:	API documentation for Tepl library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Tepl
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for Tepl library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Tepl.

%prep
%setup -q

%build
# rebuild ac/am/lt for as-needed to work
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%find_lang tepl-3

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f tepl-3.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_libdir}/libamtk-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libamtk-3.so.0
%attr(755,root,root) %{_libdir}/libtepl-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtepl-3.so.0
%{_libdir}/girepository-1.0/Amtk-3.typelib
%{_libdir}/girepository-1.0/Tepl-3.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libamtk-3.so
%attr(755,root,root) %{_libdir}/libtepl-3.so
%{_includedir}/amtk-3
%{_includedir}/tepl-3
%{_datadir}/gir-1.0/Amtk-3.gir
%{_datadir}/gir-1.0/Tepl-3.gir
%{_pkgconfigdir}/amtk-3.pc
%{_pkgconfigdir}/tepl-3.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libamtk-3.a
%{_libdir}/libtepl-3.a
%endif

%if 0
%files -n vala-tepl
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/tepl-3.deps
%{_datadir}/vala/vapi/tepl-3.vapi
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/tepl-3.0
