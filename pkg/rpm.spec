%global modname yafti

Name:           yafti
Version:        0.10.2
Release:        0%{?dist}
Summary:        Yet Another First Time Installer 
License:        Apache-2.0
URL:            https://pypi.io/project/yafti
Source0:        https://pypi.io/packages/source/y/%{modname}/%{modname}-%{version}.tar.gz

BuildArch:      noarch

Requires: libadwaita
BuildRequires:  pyproject-rpm-macros

%generate_buildrequires
%pyproject_buildrequires

%?python_enable_dependency_generator

%description

Yet another first time installer

    $ yafti

%prep
%autosetup -n %{modname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%check
echo "OKAY"

%files -n %{modname}
%license LICENSE
%{_bindir}/yafti
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-%{version}*
