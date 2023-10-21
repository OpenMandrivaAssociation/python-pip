# Created by pyp2rpm-1.0.0
%define pypi_name pip

Name:		python-pip
Version:	23.3.1
Release:	1
Group:		Development/Python
Summary:	pip installs packages. Python packages. An easy_install replacement
License:	MIT
URL:		http://pypi.python.org/pypi/pip
Source0:	https://files.pythonhosted.org/packages/source/p/pip/pip-%{version}.tar.gz
Patch0:		pip-22.2.2-workaround-crash.patch
BuildArch:	noarch
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(tomli)
BuildRequires:	python-setuptools
BuildRequires:	python-pkg-resources

Requires:	python-setuptools
Requires:	python-pkg-resources

Requires:	python-wheel
Requires:	python%{pyver}dist(flit-core)

# FIXME this is just because py_build uses pip
# Got to fall back to setup.py for bootstrapping
BuildRequires:	python-pip
BuildRequires:	python-wheel
BuildRequires:	python%{pyver}dist(flit-core)

%rename python3-pip

%description
`pip` is a tool for installing and managing Python packages, such as
those found in the `Python Package Index`_. It's a replacement for
easy_install_.

It is strongly recommended to install the corresponding rpm packages
instead of installing packages with pip.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%build
%py_build

%install
%py_install

%files
%doc LICENSE.txt PKG-INFO docs
%attr(755,root,root) %{_bindir}/pip*
%{py3_puresitedir}/pip*
