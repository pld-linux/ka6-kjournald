#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.08.0
%define		kframever	6.8
%define		qtver		6.8
%define		kaname		kjournald
Summary:	kjournald
Name:		ka6-%{kaname}
Version:	25.08.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications/Games
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	a78e8e78cd8a6d4ba820233a05d9b553
URL:		http://www.kde.org/
BuildRequires:	Qt6Concurrent-devel
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= 5.11.1
BuildRequires:	Qt6Network-devel
BuildRequires:	Qt6PrintSupport-devel
BuildRequires:	Qt6Test-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-karchive-devel >= %{kframever}
BuildRequires:	kf6-kcompletion-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kiconthemes-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-kitemviews-devel >= %{kframever}
BuildRequires:	kf6-ktextwidgets-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
BuildRequires:	zlib-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project aims to provide an abstraction of the systemd's journald
API in terms of QAbstractItemModel classes. The main purpose is to
ease the integration of journald into Qt based applications (both QML
and QtWidget).

Additional to the library, the project provides a reference
implementation of the API, called `kjournaldbrowser`. Even though that
application provides a powerful journal database reader, we aim to do
a clear split between reuseable library and application logic.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_QML_NO_CACHEGEN=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build
rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/{ko,zh_CN}

# unsupported locale (glibc-2.41)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{kaname} --all-name --with-kde --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kjournaldbrowser
%{_libdir}/libkjournald.so
%ghost %{_libdir}/libkjournald.so.0
%attr(755,root,root) %{_libdir}/libkjournald.so.*.*
%dir %{_libdir}/qt6/qml/org/kde/kjournald
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/kjournald/kjournaldplugin.so
%{_libdir}/qt6/qml/org/kde/kjournald/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/kjournald/kjournald.qmltypes
%{_libdir}/qt6/qml/org/kde/kjournald/qmldir
%{_desktopdir}/org.kde.kjournaldbrowser.desktop
%{_datadir}/metainfo/org.kde.kjournaldbrowser.appdata.xml
%{_datadir}/qlogging-categories6/kjournald.categories
