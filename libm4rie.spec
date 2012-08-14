%define	snapshot		20120415
%define	name			libm4rie
%define major			0
%define	libm4rie		%mklibname m4rie %{major}
%define	libm4rie_devel		%mklibname m4rie -d

Name:		%{name}
Group:		Sciences/Mathematics
License:	GPL
Summary:	Fast arithmetic with dense matrices over F2 for 2 <= e <= 10
Version:	0.%{snapshot}
Release:	1
URL:		http://m4ri.sagemath.org
Source:		http://m4ri.sagemath.org/downloads/m4rie-%{snapshot}.tar.gz

BuildRequires:	doxygen
BuildRequires:	givaro-devel
BuildRequires:	gmpxx-devel
BuildRequires:	gomp-devel
BuildRequires:	libm4ri-devel
BuildRequires:	texlive
# Patch sent upstream 25 April 2012.  Adapt to changes in givaro 3.5.0.
Patch0:		m4rie-givaro.patch

%description
M4RIE is a library for fast arithmetic with dense matrices over F2 for
2 <= e <= 10. It was started and is currently maintained by Martin Albrecht.
The name stems from the fact that is relies heavily on M4RI. M4RI is will be
included in the Sage mathematics software in the near future. M4RIE is
available under the General Public License Version 2 or later (GPLv2+).

%package	-n %{libm4rie}
Group:		System/Libraries
Summary:	M4RIE runtime library
Provides:	m4rie = %{version}-%{release}
Provides:	libm4rie = %{version}-%{release}

%description	-n %{libm4rie}
M4RIE is a library for fast arithmetic with dense matrices over F2 for
2 <= e <= 10. It was started and is currently maintained by Martin Albrecht.
The name stems from the fact that is relies heavily on M4RI. M4RI is will be
included in the Sage mathematics software in the near future. M4RIE is
available under the General Public License Version 2 or later (GPLv2+).

%package	-n %{libm4rie_devel}
Group:		Development/C
Summary:	M4RIE development files
Provides:	m4rie-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libm4rie} = %{version}-%{release}

%description	-n %{libm4rie_devel}
Fast arithmetic with dense matrices over F2 for 2 <= e <= 10.

%prep
%setup -q -n m4rie-%{snapshot}
%patch0 -p1

# Fix the version number in the doxygen documentation
sed -ri "s/^(PROJECT_NUMBER[[:blank:]]+= 0\.).*/\1%{version}/" src/Doxyfile

%build
perl -pi -e 's|^(libm4rie_la_LIBADD = -lm4ri)|$1 -lm|;' Makefile.am
autoreconf
%configure --disable-static

# The configure step picks up -fopenmp from the m4ri CFLAGS.  However, m4rie
# does not contain any OpenMP-using code.  The end result is that libm4rie is
# unnecessarily linked with libgomp, leading to rpmlint complaints.
sed -i "s/M4RI_CFLAGS =.*/M4RI_CFLAGS =/" Makefile bench/Makefile

%make
cd src
doxygen

%install
%makeinstall_std
rm -f doc/html/installdox

%check
make check

%files		-n %{libm4rie}
%doc COPYING
%{_libdir}/libm4rie-*.so

%files		-n %{libm4rie_devel}
%doc doc/html
%{_includedir}/m4rie
%{_libdir}/libm4rie.so
