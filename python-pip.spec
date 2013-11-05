%global module pip

Name:           python-%{module}
Version:        1.4.1
Release:        1
Group:          Development/Python
Summary:        A tool for installing and managing Python packages (easy_install replacement)

License:        MIT
URL:            http://pypi.python.org/pypi/pip
Source0:        http://pypi.python.org/packages/source/p/pip/%{module}-%{version}.tar.gz

BuildArch:      noarch
 
BuildRequires:  pkgconfig(python)
BuildRequires:  python-distribute

Requires:       python-distribute
Requires:       python-pkg-resources

%description
`pip` is a tool for installing and managing Python packages, such as
those found in the `Python Package Index`_. It's a replacement for
easy_install_.

%package -n python3-pip
Summary:        A tool for installing and managing Python3 packages (easy_install replacement)
Group:          Development/Python

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-distribute
Requires:  	python3-distribute
Requires:       python3-pkg-resources

%description -n python3-pip
Pip is a replacement for `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_.  It uses mostly the
same techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.

%prep
%setup -q -c
# Remove bundled egg-info
rm -rf %{module}-%{version}/%{module}.egg-info

mv %{module}-%{version} python2
cp -r python2 python3

pushd python2
%apply_patches
%{__sed} -i '1d' pip/__init__.py
popd

pushd python3
%apply_patches
%{__sed} -i '1d' pip/__init__.py
popd


%build
pushd python2
python setup.py build
popd

pushd python3
python3 setup.py build
popd

%install
pushd python3
python3 setup.py install --skip-build --root %{buildroot}

# Change the name of the python3 pip executable in order to not conflict with
# the python2 executable
mv %{buildroot}%{_bindir}/pip %{buildroot}%{_bindir}/python3-pip

# The install process creates both pip and pip-<python_abiversion> that seem to
# be the same. Remove the extra script
pushd %{buildroot}%{_bindir}
%{__rm} -rf pip-3*
popd

popd

pushd python2
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# The install process creates both pip and pip-<python_abiversion> that seem to
# be the same. Since removing pip-* also clobbers pip-python3, just remove pip-2*
pushd %{buildroot}%{_bindir}
%{__rm} -rf pip-2*
popd

popd

%files
%doc python2/LICENSE.txt python2/PKG-INFO python2/docs
%attr(755,root,root) %{_bindir}/pip
%{python_sitelib}/pip*

%files -n python3-pip
%doc python3/LICENSE.txt python3/PKG-INFO python3/docs
%attr(755,root,root) %{_bindir}/python3-pip
%{python3_sitelib}/pip*
