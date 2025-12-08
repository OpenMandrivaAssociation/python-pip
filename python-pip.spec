%define pypi_name pip

Name:		python-pip
Version:	25.3
Release:	2
Group:		Development/Python
Summary:	pip installs packages. Python packages. An easy_install replacement
License:	MIT
URL:		https://pypi.python.org/pypi/pip
Source0:	https://files.pythonhosted.org/packages/source/p/pip/pip-%{version}.tar.gz
#Patch0:		pip-22.2.2-workaround-crash.patch
BuildArch:	noarch
# We're not using declarative build features here because declarative uses
# pip to build -- but we can't depend on a preexisting version of ourselves.
# We'll run pip from inside the source tree instead.
BuildRequires:	python
BuildRequires:	python%{pyver}dist(flit-core)
BuildRequires:	python%{pyver}dist(packaging)
Requires:	python%{pyver}dist(packaging)

# This "obsoletes without provides" is intentional.
# We want to obsolete python-pip-bootstrap because
# python-pip is the "real thing", but we don't want
# to fulfill the python-pip-bootstrap build dependency
# in packages we depend on (those should be built
# with the bootstrap version to not generate a
# dependency loop)
Obsoletes:	python-pip-bootstrap < 4.0.0

%rename python3-pip

%description
`pip` is a tool for installing and managing Python packages, such as
those found in the `Python Package Index`_. It's a replacement for
easy_install_.

It is strongly recommended to install the corresponding rpm packages
instead of installing packages with pip.

%prep
%autosetup -p1 -n pip-%{version}

%build
export PYTHONPATH=$(pwd)/src
python -m pip wheel --wheel-dir ../RPMBUILD_wheels --no-deps --no-build-isolation --verbose .

%install
export PYTHONPATH=$(pwd)/src
python -m pip install --root=%{buildroot} --no-deps --verbose --ignore-installed --no-warn-script-location --no-index --no-cache-dir --find-links ../RPMBUILD_wheels ../RPMBUILD_wheels/*.whl

%files
%doc LICENSE.txt PKG-INFO docs
%attr(755,root,root) %{_bindir}/pip*
%{py3_puresitedir}/pip*
