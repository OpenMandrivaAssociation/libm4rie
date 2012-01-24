%define patchlevel		.p1
%define	snapshot		20111004
%define	name			libm4rie
%define major			0
%define	libm4rie		%mklibname m4rie %{major}
%define	libm4rie_devel		%mklibname m4rie -d

Name:		%{name}
Group:		Sciences/Mathematics
License:	GPL
Summary:	Fast arithmetic with dense matrices over F2 for 2 <= e <= 10
Version:	0.%{snapshot}
Release:	%mkrel 1
# sagemath 4.8 spkg renamed
Source:		libm4rie-%{snapshot}%{patchlevel}.tar.bz2
URL:		http://m4ri.sagemath.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	libm4ri-devel

%description
M4RIE is a library for fast arithmetic with dense matrices over F2 for
2 <= e <= 10. It was started and is currently maintained by Martin Albrecht.
The name stems from the fact that is relies heavily on M4RI. M4RI is will be
included in the Sage mathematics software in the near future. M4RIE is
available under the General Public License Version 2 or later (GPLv2+).

%package	-n %{libm4rie}
Group:		System/Libraries
Summary:	M4RIE runtime library
Requires:	%{libm4rie} = %{version}-%{release}
Provides:	%{name} = %{version}-%{release}
Provides:	lib%{name} = %{version}-%{release}

%description	-n %{libm4rie}
M4RIE is a library for fast arithmetic with dense matrices over F2 for
2 <= e <= 10. It was started and is currently maintained by Martin Albrecht.
The name stems from the fact that is relies heavily on M4RI. M4RI is will be
included in the Sage mathematics software in the near future. M4RIE is
available under the General Public License Version 2 or later (GPLv2+).

%package	-n %{libm4rie_devel}
Group:		Development/C
Summary:	M4RIE development files
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{namee}-devel = %{version}-%{release}
Requires:	%{libm4rie} = %{version}-%{release}

%description	-n %{libm4rie_devel}
Fast arithmetic with dense matrices over F2 for 2 <= e <= 10.

%prep
%setup -q -n libm4rie-%{snapshot}%{patchlevel}

%build
pushd m4rie
    autoreconf
    %configure --disable-static
    %make
popd

%install
pushd m4rie
    %makeinstall_std
popd

%clean
rm -rf %{buildroot}

%files		-n %{libm4rie}
%defattr(-,root,root)
%{_libdir}/libm4rie-0.0.%{snapshot}.so

%files		-n %{libm4rie_devel}
%defattr(-,root,root)
%dir %{_includedir}/m4rie
%{_includedir}/m4rie/*
%{_libdir}/libm4rie.so
