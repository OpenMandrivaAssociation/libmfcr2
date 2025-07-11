%define	major _1
%define libname %mklibname mfcr2 %{major}
%define develname %mklibname mfcr2 -d

Summary:	A library for MFC/R2 signaling on E1 lines
Name:		libmfcr2
Version:	0.0.6
Release:	%mkrel 0.pre1.3
License:	GPL
Group:		System/Libraries
URL:		https://www.soft-switch.org/
Source0:	http://www.soft-switch.org/downloads/unicall/libmfcr2-%{version}pre1.tgz
BuildRequires:	autoconf2.5
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	spandsp-devel
BuildRequires:	libsupertone-devel
BuildRequires:	libunicall-devel >= 0.0.6
BuildRequires:	tiff-devel >= 3.6.1-3mdk
BuildRequires:	libxml2-devel
BuildRequires:	jpeg-devel
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
libmfcr2 is a library for MFC/R2 signalling on E1s.

%package -n	%{libname}
Summary:	A library for MFC/R2 signaling on E1 lines
Group:          System/Libraries

%description -n	%{libname}
libmfcr2 is a library for MFC/R2 signalling on E1s.

%package -n	%{develname}
Summary:	Header files and libraries needed for development with libmfcr2
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname mfcr2 _1 -d}

%description -n	%{develname}
This package includes the header files and libraries needed for
developing programs using libsupertone.

%prep

%setup -q -n %{name}-%{version}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# lib64 fix
perl -pi -e "s|^protocoldir=.*|protocoldir=\"%{_libdir}/unicall/protocols\"|g" configure.ac

%build
export WANT_AUTOCONF_2_5=1
rm -f configure
libtoolize --copy --force; aclocal; autoconf; automake --add-missing --copy

%configure2_5x \
    --enable-shared \
    --enable-static

make CFLAGS="%{optflags} -fPIC"

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_includedir}

%makeinstall_std

install -m0644 libmfcr2.h %{buildroot}%{_includedir}/
install -m0644 mfcr2.h %{buildroot}%{_includedir}/

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/unicall/protocols/*.so

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/unicall/protocols/*.a
%{_libdir}/unicall/protocols/*.la
%{_includedir}/*.h
