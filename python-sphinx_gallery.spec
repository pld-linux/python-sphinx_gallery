# NOTE: for versions >= 0.5 (for Python 3.5+) see python3-sphinx_gallery.spec
#
# Conditional build:
%bcond_with	tests	# unit tests [testconfs dir is missing in dist tarball]
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-sphinx_gallery.spec)

Summary:	Sphinx extension to automatically generate an examples gallery
Summary(pl.UTF-8):	Rozszerzenie Sphinksa do automatycznego generowania galerii przykładów
Name:		python-sphinx_gallery
# NOTE: keep 0.4.x here; 0.5+ don't support python 2
Version:	0.4.0
Release:	5
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sphinx-gallery/
Source0:	https://files.pythonhosted.org/packages/source/s/sphinx-gallery/sphinx-gallery-%{version}.tar.gz
# Source0-md5:	1f3e578107ca253a184889733a4fbcea
URL:		https://github.com/sphinx-gallery/sphinx-gallery
%if %{with python2}
BuildRequires:	python-modules >= 1:2.5
%{?with_tests:BuildRequires:	python-pytest}
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
%{?with_tests:BuildRequires:	python3-pytest}
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.5
Provides:	python-sphinx-gallery = %{version}-%{release}
Obsoletes:	python-sphinx-gallery < 0.4.0-5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Sphinx extension that builds an HTML version of any Python script
and puts it into an examples gallery.
  
It is extracted from the scikit-learn project and aims to be an
independent general purpose extension.

%description -l pl.UTF-8
Rozszerzenie Sphinksa tworzące wersję HTML dowolnego skryptu Pythona i
umieszczające go w galerii przykładów.

Zostało wyciągnięte z projektu scikit-learn z myślą o używaniu jako
niezależne rozszerzenie ogólnego przeznaczenia.

%package -n python3-sphinx_gallery
Summary:	Sphinx extension to automatically generate an examples gallery
Summary(pl.UTF-8):	Rozszerzenie Sphinksa do automatycznego generowania galerii przykładów
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2
Provides:	python3-sphinx-gallery = %{version}-%{release}
Obsoletes:	python3-sphinx-gallery < 0.4.0-5

%description -n python3-sphinx_gallery
A Sphinx extension that builds an HTML version of any Python script
and puts it into an examples gallery.
  
It is extracted from the scikit-learn project and aims to be an
independent general purpose extension.

%description -n python3-sphinx_gallery -l pl.UTF-8
Rozszerzenie Sphinksa tworzące wersję HTML dowolnego skryptu Pythona i
umieszczające go w galerii przykładów.

Zostało wyciągnięte z projektu scikit-learn z myślą o używaniu jako
niezależne rozszerzenie ogólnego przeznaczenia.

%prep
%setup -q -n sphinx-gallery-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd)/build-2/lib \
pytest-2 sphinx_gallery/tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/build-3/lib \
pytest-3 sphinx_gallery/tests
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/sphinx_gallery/tests
%endif

%if %{with python3}
# ensure tools come from python3 package
%{__rm} -r $RPM_BUILD_ROOT%{_bindir}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/sphinx_gallery/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%if %{without python3}
%attr(755,root,root) %{_bindir}/copy_sphinxgallery.sh
%attr(755,root,root) %{_bindir}/sphx_glr_python_to_jupyter.py
%endif
%{py_sitescriptdir}/sphinx_gallery
%{py_sitescriptdir}/sphinx_gallery-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-sphinx_gallery
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/copy_sphinxgallery.sh
%attr(755,root,root) %{_bindir}/sphx_glr_python_to_jupyter.py
%{py3_sitescriptdir}/sphinx_gallery
%{py3_sitescriptdir}/sphinx_gallery-%{version}-py*.egg-info
%endif
