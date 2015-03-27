# Created by pyp2rpm-1.0.0
%define pypi_name pip

Name:           python-pip
Version:        6.0.6
Release:        1
Group:          Development/Python
Summary:        Pip installs packages. Python packages. An easy_install replacement

License:        MIT
URL:            http://pypi.python.org/pypi/pip
Source0:        http://pypi.python.org/packages/source/p/pip/pip-%{version}.tar.gz

BuildArch:      noarch
 
BuildRequires:  pkgconfig(python)
BuildRequires:  python2-setuptools
BuildRequires:  pkgconfig(python3)
BuildRequires:  python-setuptools

Requires:       python-setuptools
Requires:       python-pkg-resources
%rename python3-pip

%description
`pip` is a tool for installing and managing Python packages, such as
those found in the `Python Package Index`_. It's a replacement for
easy_install_.

%package -n python2-pip
Summary:        A tool for installing and managing Python3 packages
Group:          Development/Python

Requires:	python2-setuptools

%description -n python2-pip
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
python2} setup.py build
pushd %{py3dir}
python3 setup.py build
popd

%install
python2} setup.py install -O1 --skip-build --root %{buildroot}

# The install process creates both pip and pip-<python_abiversion> that seem to
# be the same. Since removing pip-* also clobbers pip-python3, just remove pip-2*
pushd %{buildroot}%{_bindir}
rm -rf pip2*

# Change the name of the python2 pip executable in order to not conflict with
# the python3 executable
mv %{buildroot}%{_bindir}/pip %{buildroot}%{_bindir}/python2-pip

popd

pushd %{py3dir}
python3 setup.py install --skip-build --root %{buildroot}

# The install process creates both pip and pip-<python_abiversion> that seem to
# be the same. Remove the extra script
pushd %{buildroot}%{_bindir}
rm -rf pip3*

popd

%files
%doc LICENSE.txt PKG-INFO docs
%attr(755,root,root) %{_bindir}/pip
%{py3_puresitedir}/pip*

%files -n python2-pip
%doc LICENSE.txt PKG-INFO docs
%attr(755,root,root) %{_bindir}/python2-pip
%{py2_puresitedir}/pip*
