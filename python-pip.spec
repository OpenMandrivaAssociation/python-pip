# Created by pyp2rpm-1.0.0
%define pypi_name pip

Name:           python-pip
Version:        1.4.1
Release:        22
Group:          Development/Python
Summary:        pip installs packages. Python packages. An easy_install replacement

License:        MIT
URL:            http://pypi.python.org/pypi/pip
Source0:        http://pypi.python.org/packages/source/p/pip/pip-%{version}.tar.gz
Patch0:         pip-1.4.1-mga-change-match_hostname-to-follow-RFC-6125.patch

BuildArch:      noarch
 
BuildRequires:  pkgconfig(python)
BuildRequires:  python-distribute
BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-distribute

Requires:       python-distribute
Requires:       python-pkg-resources

%description
`pip` is a tool for installing and managing Python packages, such as
those found in the `Python Package Index`_. It's a replacement for
easy_install_.

%package -n python3-pip
Summary:        A tool for installing and managing Python3 packages
Group:          Development/Python

Requires:	python3-distribute

%description -n python3-pip
Pip is a replacement for `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_.  It uses mostly the
same techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%apply_patches
%{__sed} -i '1d' pip/__init__.py

cp -a . %{py3dir}

%build
%{__python} setup.py build
pushd %{py3dir}
%{__python3} setup.py build
popd

%install
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}

# Change the name of the python3 pip executable in order to not conflict with
# the python2 executable
mv %{buildroot}%{_bindir}/pip %{buildroot}%{_bindir}/python3-pip

# The install process creates both pip and pip-<python_abiversion> that seem to
# be the same. Remove the extra script
pushd %{buildroot}%{_bindir}
%{__rm} -rf pip-3*

popd
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# The install process creates both pip and pip-<python_abiversion> that seem to
# be the same. Since removing pip-* also clobbers pip-python3, just remove pip-2*
pushd %{buildroot}%{_bindir}
%{__rm} -rf pip-2*


%files
%doc LICENSE.txt PKG-INFO docs
%attr(755,root,root) %{_bindir}/pip
%{python_sitelib}/pip*

%files -n python3-pip
%doc LICENSE.txt PKG-INFO docs
%attr(755,root,root) %{_bindir}/python3-pip
%{python3_sitelib}/pip*
