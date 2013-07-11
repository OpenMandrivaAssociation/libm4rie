%define	snapshot		20130416
%define	name			libm4rie
%define major			0
%define	libm4rie		%mklibname m4rie %{major}
%define	libm4rie_devel		%mklibname m4rie -d

Name:		%{name}
Group:		Sciences/Mathematics
License:	GPL
Summary:	Linear Algebra over F_2^e
Version:	0.%{snapshot}
Release:	1
URL:		http://m4ri.sagemath.org
Source:		http://m4ri.sagemath.org/downloads/m4rie-%{snapshot}.tar.gz
# The doxygen control file was omitted from this release
Source1:	m4rie-doxyfile
Source2:	%{name}.rpmlintrc
# Fix compiler warnings that may indicate runtime / test-time problems
Patch0:		m4rie-warning.patch
# Add aarch64 support.
Patch1:		m4rie-aarch64.patch
# Fix a broken doxygen construct
Patch2:		m4rie-doxygen.patch

BuildRequires:	doxygen
BuildRequires:	givaro-devel
BuildRequires:	gmpxx-devel
BuildRequires:	gomp-devel
BuildRequires:	libm4ri-devel
BuildRequires:	texlive

%description
M4RIE is a library for fast arithmetic with dense matrices over F_2^e.
It is an add-on to the M4RI library, which implements fast arithmetic
with dense matrices over F_2.  M4RIE is used by the Sage mathematics
software.

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
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n m4rie-%{snapshot}
%patch0
%patch1
%patch2
cp -p %{SOURCE1} m4rie/Doxyfile

%build
perl -pi -e 's|^(libm4rie_la_LIBADD = -lm4ri)|$1 -lm|;' Makefile.am
autoreconf -i
%configure --disable-static

# The configure step picks up -fopenmp from the m4ri CFLAGS.  However, m4rie
# does not contain any OpenMP-using code.  The end result is that libm4rie is
# unnecessarily linked with libgomp, leading to rpmlint complaints.
sed -i "s/M4RI_CFLAGS =.*/M4RI_CFLAGS =/" Makefile bench/Makefile

%make
cd m4rie
doxygen
cd ../doc/latex
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib%{name}.la

%check
make check

%files		-n %{libm4rie}
%doc COPYING
%{_libdir}/libm4rie-*.so

%files		-n %{libm4rie_devel}
%doc doc/latex/refman.pdf
%{_includedir}/m4rie
%{_libdir}/libm4rie.so
