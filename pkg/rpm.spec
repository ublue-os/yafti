%global modname yafti

Name:           yafti
Version:        0.1.0
Release:        0%{?dist}
Summary:        Yet Another First Time Installer 
License:        Apache-2.0
URL:            https://pypi.io/project/yafti
Source0:        https://pypi.io/packages/source/y/%{modname}/%{modname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros


%?python_enable_dependency_generator

%description

Yet another first time installer

    $ yafti

%prep
%autosetup -n %{modname}-%{version}

%build
%py3_build

%install
%py3_install

%check
echo "OKAY"

%files -n %{modname}
%doc CHANGELOG.md
%license LICENSE
%{_bindir}/yafti
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-%{version}*
