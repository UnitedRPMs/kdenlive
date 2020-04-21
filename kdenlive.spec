#
# spec file for package kdenlive
#
# Copyright (c) 2020 UnitedRPMs.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://goo.gl/zqFJft
#

# Guide thanks to http://www.linuxfromscratch.org/blfs/view/cvs/kde/kdenlive.html

%global gitdate 20200420
%global commit0 952c69bb520a65223e4f0dfccef8a029ae979942
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:    kdenlive
Summary: Non-linear video editor
Version: 20.03.90
Release: 7%{dist}

License: GPLv2+
URL:     http://www.kdenlive.org
Source0: https://github.com/KDE/kdenlive/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
#Source0: https://download.kde.org/stable/applications/{version}/src/{name}-{version}.tar.xz
Source1: https://github.com/UnitedRPMs/kdenlive/releases/download/lang/lang.tar.gz
Patch:	mlt_fix.patch

BuildRequires: desktop-file-utils
BuildRequires: extra-cmake-modules
BuildRequires: gettext
BuildRequires: qt5-qtbase
BuildRequires: make
BuildRequires: cmake(Qt5Multimedia)
BuildRequires: cmake(KF5Declarative)
BuildRequires: cmake(KF5Purpose)
BuildRequires: cmake(KF5Archive)
BuildRequires: cmake(KF5Bookmarks)
BuildRequires: cmake(KF5Config)
BuildRequires: cmake(KF5ConfigWidgets)
BuildRequires: cmake(KF5CoreAddons)
BuildRequires: cmake(KF5DocTools)
BuildRequires: cmake(KF5DBusAddons)
BuildRequires: cmake(KF5GuiAddons)
BuildRequires: cmake(KF5I18n)
BuildRequires: cmake(KF5IconThemes)
BuildRequires: cmake(KF5ItemViews)
BuildRequires: cmake(KF5KIO)
BuildRequires: cmake(KF5JobWidgets)
BuildRequires: cmake(KF5NewStuff)
BuildRequires: cmake(KF5Notifications)
BuildRequires: cmake(KF5NotifyConfig)
BuildRequires: cmake(KF5Plotting)
BuildRequires: cmake(KF5TextWidgets)
BuildRequires: cmake(KF5XmlGui)
BuildRequires: cmake(KF5Crash)
BuildRequires: cmake(KF5FileMetaData)
BuildRequires: libappstream-glib

BuildRequires: pkgconfig(libv4l2)
BuildRequires: pkgconfig(mlt++) >= 6.0
%global mlt_version %(pkg-config --modversion mlt++ 2>/dev/null || echo 6.0)

BuildRequires: pkgconfig(Qt5Concurrent)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5OpenGL)
BuildRequires: pkgconfig(Qt5Script)
BuildRequires: pkgconfig(Qt5Svg)
BuildRequires: pkgconfig(Qt5Qml)
BuildRequires: pkgconfig(Qt5Quick)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt5WebKitWidgets)

## workaround for missing dependency in kf5-kio, can remove
## once kf5-kio-5.24.0-2 (or newer is available)
BuildRequires: kf5-kinit-devel
%{?kf5_kinit_requires}
Requires: dvdauthor
Requires: dvgrab
Requires: ffmpeg
%if 0%{?fedora} > 24
Requires: mlt-freeworld%{?_isa} >= %{mlt_version}
%else
Requires: mlt%{?_isa} >= %{mlt_version}
%endif
Recommends: recordmydesktop
Requires: qt5-qtquickcontrols2
Requires: frei0r-plugins

%description
Kdenlive is an intuitive and powerful multi-track video editor, including most
recent video technologies.


%prep
%autosetup -n kdenlive-%{commit0} -p1 -a 1 
#autosetup -n kdenlive-%{version} 

# First, fix some issues identified by gcc7:
sed -e '/KLocal/a #include <functional>' \
    -i src/profiles/tree/profiletreemodel.cpp  &&
sed -e '/abs/s/leftDist/(int)&/' \
    -i src/scopes/audioscopes/spectrogram.cpp

# LANG
#echo 'ki18n_install(po)
#if (KF5DocTools_FOUND)
# kdoctools_install(po)
#endif()' >> CMakeLists.txt

# cmake 3.10 fix
%if 0%{?fedora} >= 28
sed -i '/project(Kdenlive)/a SET_SOURCE_FILES_PROPERTIES(${_impl} PROPERTIES SKIP_AUTOMOC TRUE)' CMakeLists.txt
%endif


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF -DKDE_INSTALL_USE_QT_SYS_PATHS=ON  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang %{name} --with-kde


%check
%if 0%{?fedora} >= 28
appstream-util validate-relax --nonet %{buildroot}/%{_kf5_datadir}/metainfo/org.kde.%{name}.appdata.xml ||:
%else
appstream-util validate-relax --nonet %{buildroot}%{_kf5_datadir}/appdata/org.kde.%{name}.appdata.xml ||:
%endif
desktop-file-validate %{buildroot}/%{_kf5_datadir}/applications/org.kde.%{name}.desktop


%post
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null || :
/bin/touch --no-create %{_kf5_datadir}/mime/packages &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  /bin/touch --no-create %{_kf5_datadir}/icons/hicolor &>/dev/null
  /usr/bin/gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &>/dev/null || :
  /bin/touch --no-create %{_kf5_datadir}/mime/packages &> /dev/null || :
  /usr/bin/update-mime-database %{_kf5_datadir}/mime &> /dev/null || :
  /usr/bin/update-desktop-database &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :
/usr/bin/update-mime-database %{?fedora:-n} %{_kf5_datadir}/mime &> /dev/null || :

%files -f %{name}.lang
%doc AUTHORS README.md
%license COPYING
%{_docdir}/Kdenlive/
%{_kf5_bindir}/kdenlive_render
%{_kf5_bindir}/%{name}
%{_kf5_datadir}/applications/org.kde.%{name}.desktop
%if 0%{?fedora} >= 28
%{_kf5_datadir}/metainfo/org.kde.kdenlive.appdata.xml
%else
%{_kf5_datadir}/appdata/*.appdata.xml
%endif
%{_kf5_datadir}/kdenlive/
%{_kf5_datadir}/mime/packages/org.kde.kdenlive.xml
%{_kf5_datadir}/mime/packages/westley.xml
%{_kf5_datadir}/icons/hicolor/*/*/*
%{_kf5_datadir}/config.kcfg/kdenlivesettings.kcfg
%{_kf5_datadir}/knotifications5/kdenlive.notifyrc
%{_kf5_datadir}/kservices5/mltpreview.desktop
%{_kf5_datadir}/kxmlgui5/kdenlive/
%{_kf5_sysconfdir}/xdg/kdenlive_renderprofiles.knsrc
%{_kf5_sysconfdir}/xdg/kdenlive_titles.knsrc
%{_kf5_sysconfdir}/xdg/kdenlive_wipes.knsrc
%{_kf5_qtplugindir}/mltpreview.so
%{_kf5_mandir}/man1/kdenlive.1*
%{_kf5_mandir}/man1/kdenlive_render.1*
%{_sysconfdir}/xdg/kdenlive_keyboardschemes.knsrc
%if 0%{?fedora} >= 29
%{_kf5_datadir}/qlogging-categories5/kdenlive.categories
%else
%{_sysconfdir}/xdg/kdenlive.categories
%endif
%{_docdir}/HTML/*/kdenlive/


%changelog

* Mon Apr 20 2020 David Va <davidva AT tuta DOT io> 20.03.90-7
- Updated to 20.03.90

* Wed Mar 11 2020 David Va <davidva AT tuta DOT io> 19.12.3-7
- Updated to 19.12.3

* Fri Feb 07 2020 David Va <davidva AT tuta DOT io> 19.12.2-7
- Updated to 19.12.2

* Fri Dec 13 2019 David Va <davidva AT tuta DOT io> 19.12.1-7
- Updated to 19.12.1

* Fri Nov 22 2019 David Va <davidva AT tuta DOT io> 19.11.80-7
- Updated to 19.11.80

* Fri Oct 11 2019 David Va <davidva AT tuta DOT io> 19.08.2-7
- Updated to 19.08.2

* Sun Oct 06 2019 David Va <davidva AT tuta DOT io> 19.08.1-9
- Added Requires qt5-qtquickcontrols2

* Mon Sep 23 2019 David Va <davidva AT tuta DOT io> 19.08.1-8
- Added Requires frei0r-plugins

* Wed Sep 11 2019 David Va <davidva AT tuta DOT io> 19.08.1-7
- Updated to 19.08.1

* Tue Aug 20 2019 David Va <davidva AT tuta DOT io> 19.08.0-8
- Updated to current commit stable

* Tue Aug 13 2019 David Va <davidva AT tuta DOT io> 19.08-7
- Updated to 19.08

* Sun Jul 14 2019 David Va <davidva AT tuta DOT io> 19.04.3-7
- Updated to 19.04.3

* Fri Jun 07 2019 David Va <davidva AT tuta DOT io> 19.04.2-7
- Updated to 19.04.2

* Thu May 16 2019 David Va <davidva AT tuta DOT io> 19.04.1-7
- Updated to 19.04.1

* Thu Apr 18 2019 David Va <davidva AT tuta DOT io> 19.04.0-7
- Updated to 19.04.0

* Wed Apr 10 2019 David Va <davidva AT tuta DOT io> 19.03.90-7
- Updated to 19.03.90

* Sat Feb 16 2019 David Va <davidva AT tuta DOT io> 18.12.2-7
- Updated to 18.12.2

* Thu Jan 10 2019 David Va <davidva AT tuta DOT io> 18.12.1-3
- Updated to 18.12.1

* Tue Dec 11 2018 David Va <davidva AT tuta DOT io> 18.12.0-3
- Updated to 18.12.0

* Sat Nov 10 2018 David Va <davidva AT tuta DOT io> 18.08.3-3
- MLT fix path

* Thu Nov 08 2018 David Va <davidva AT tuta DOT io> 18.08.3-2
- Updated to 18.08.3

* Wed Oct 10 2018 David Va <davidva AT tuta DOT io> 18.08.2-2
- Updated to 18.08.2

* Thu Sep 06 2018 David Va <davidva AT tuta DOT io> 18.08.1-2
- Updated to 18.08.1

* Fri Aug 17 2018 David Va <davidva AT tuta DOT io> 18.08.0-2
- Updated to 18.08.0

* Sat Aug 04 2018 David Va <davidva AT tuta DOT io> 18.07.90-2
- Updated to 18.07.90

* Fri Jul 27 2018 David Va <davidva AT tuta DOT io> 18.07.80-2
- Updated to 18.07.80

* Fri Jul 13 2018 David Va <davidva AT tuta DOT io> 18.04.3-2
- Updated to 18.04.3

* Thu Jun 07 2018 David Vásquez <davidva AT tutanota DOT com> - 18.04.2-2
- Updated to 18.04.2

* Fri May 11 2018 David Vásquez <davidva AT tutanota DOT com> - 18.04.1-2
- Updated to 18.04.1

* Thu Apr 19 2018 David Vásquez <davidva AT tutanota DOT com> - 18.04.0-2
- Updated to 18.04.0

* Fri Apr 13 2018 David Vásquez <davidva AT tutanota DOT com> - 18.03.90-2
- Updated to 18.03.90

* Wed Mar 07 2018 David Vásquez <davidva AT tutanota DOT com> - 17.12.3-2
- Updated to 17.12.3

* Tue Feb 06 2018 David Vásquez <davidva AT tutanota DOT com> - 17.12.2-2
- Updated to 17.12.2

* Thu Jan 11 2018 David Vásquez <davidva AT tutanota DOT com> - 17.12.1-2
- Updated to 17.12.1-2

* Fri Dec 15 2017 David Vásquez <davidva AT tutanota DOT com> - 17.12.0-2
- Updated to 17.12.0-2

* Wed Dec 06 2017 David Vásquez <davidva AT tutanota DOT com> - 17.11.90-2
- Updated to 17.11.90

* Tue Nov 07 2017 David Vásquez <davidva AT tutanota DOT com> - 17.08.3-2
- Updated to 17.08.3-2

* Sun Oct 15 2017 David Vásquez <davidva AT tutanota DOT com> - 17.08.2-3
- recordmydesktop retired from official, then changed requires to recommends

* Fri Oct 13 2017 David Vásquez <davidva AT tutanota DOT com> - 17.08.2-2
- Updated to 17.08.2-2

* Sun Oct 01 2017 David Vásquez <davidva AT tutanota DOT com> - 17.08.1-2
- Updated to 17.08.1-2

* Wed May 31 2017 David Vásquez <davidva AT tutanota DOT com> - 17.04.1-2.gitb965270
- Updated to 17.04.1-2.gitb965270

* Sun Mar 26 2017 David Vásquez <davidva AT tutanota DOT com> - 16.12.3-1.20170326gitc17302f
- Updated to 16.12.3-1.20170326gitc17302f

* Sat Feb 25 2017 David Vásquez <davidva AT tutanota DOT com> - 16.12.2-1.20170225git640d446
- Updated to 16.12.2-1.20170225git640d446

* Sat Jan 07 2017 Pavlo Rudyi <paulcarroty at riseup.net> 16.21-1
- Updated to 16.12

* Thu Oct 13 2016 David Vásquez <davidva AT tutanota DOT com> - 16.08.2-1
- Updated to 16.08.2

* Tue Aug 23 2016 David Vásquez <davidva AT tutanota DOT com> - 16.08.0-1
- Updated to 16.08.0

* Tue Jul 12 2016 David Vásquez <davidva AT tutanota DOT com> - 16.04.3-1
- Updated to 16.04.3

* Sun Jun 26 2016 The UnitedRPMs Project (Key for UnitedRPMs infrastructure) <unitedrpms@protonmail.com> - 16.04.1-3
- Rebuild with new ffmpeg

* Fri May 27 2016 David Vásquez <davidva AT tutanota DOT com> 16.04.1-2
- Added missing dependencies
- Disabled, build testing
- Automatic qt system path

* Fri May 13 2016 Sérgio Basto <sergio@serjux.com> - 16.04.1-1
- Update to 16.04.1

* Thu Mar 24 2016 Sérgio Basto <sergio@serjux.com> - 15.12.2-2
- Fix rfbz #4015

* Wed Feb 17 2016 Rex Dieter <rdieter@fedoraproject.org> 15.12.2-1
- 15.12.2

* Mon Nov 09 2015 Rex Dieter <rdieter@fedoraproject.org> 15.08.2-1
- 15.08.2

* Mon Dec 22 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.10-1
- 0.9.10

* Wed Aug 06 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.8-2
- optimize mime scriptlets

* Wed May 14 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.8-1
- 0.9.8

* Mon Apr 07 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.9.6-4
- Rebuilt for rfbz#3209

* Wed Oct 09 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.9.6-3
- rebuilt for mlt

* Sun May 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.9.6-2
- Rebuilt for x264/FFmpeg

* Sun Apr 07 2013 Rex Dieter <rdieter@fedoraproject.org> 0.9.6-1
- 0.9.6

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.9.4-2
- Mass rebuilt for Fedora 19 Features

* Tue Jan 29 2013 Rex Dieter <rdieter@fedoraproject.org> 0.9.4-1
- 0.9.4

* Tue Jun 19 2012 Richard Shaw <hobbes1069@gmail.com> - 0.9.2-2
- Rebuild for updated mlt.

* Thu May 31 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.2-1
- 0.9.2

* Tue May 15 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9-1
- 0.9
- pkgconfig-style deps

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.8.2.1-3
- Rebuilt for c++ ABI breakage

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.8.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 10 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.2.1-1
- 0.8.2.1

* Tue Nov 15 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.2-2
- rebuild

* Fri Nov 11 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.2-1
- 0.8.2
- tighten mlt deps

* Thu Jul 21 2011 Ryan Rix <ry@n.rix.si> 0.8-1
- New version
- Add patch to fix FTBFS

* Fri Apr 15 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.8-2
- update scriptlets, %%_kde4_... macros/best-practices
- +Requires: kdebase-runtime (versioned)
- fix ftbfs

* Thu Apr 07 2011 Ryan Rix <ry@n.rix.si> - 0.7.8-1
- new version

* Mon Mar 01 2010 Zarko <zarko.pintar@gmail.com> - 0.7.7.1-1
- new version

* Thu Feb 18 2010 Zarko <zarko.pintar@gmail.com> - 0.7.7-1
- new version

* Mon Sep 07 2009 Zarko <zarko.pintar@gmail.com> - 0.7.5-1
- new version

* Sat May 30 2009 Zarko <zarko.pintar@gmail.com> - 0.7.4-2
- added updating of mime database
- changed dir of .desktop file

* Fri May 22 2009 Zarko <zarko.pintar@gmail.com> - 0.7.4-1
- new release
- spec cleaning

* Thu Apr 16 2009 Zarko <zarko.pintar@gmail.com> - 0.7.3-2
- some clearing
- added doc files

* Wed Apr 15 2009 Zarko <zarko.pintar@gmail.com> - 0.7.3-1
- new release

* Sun Apr 12 2009 Zarko <zarko.pintar@gmail.com> - 0.7.2.1-2
- spec convert to kde4 macros

* Mon Mar 16 2009 Zarko <zarko.pintar@gmail.com> - 0.7.2.1-1
- update to 0.7.2.1
- spec cleaned
- Resolve RPATHs

* Sun Nov 16 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 0.7-1
- update to 0.7

* Wed Nov  5 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 0.7-0.1.20081104svn2622
- update to last svn revision

* Tue Nov  4 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 0.7-0.beta1
- clean up spec

* Fri Oct 17 2008 jeff <moe@blagblagblag.org> - 0.7-1.beta1
- Add URL
- Full URL for Source:
- Remove all Requires:
- Update BuildRoot
- Remove Packager: Brixton Linux Action Group
- Add BuildRequires: ffmpeg-devel kdebindings-devel soprano-devel
- Update %%files
- %%doc with only effects/README
- GPLv2+
- Add lang files

* Tue Jul  8 2008 jeff <moe@blagblagblag.org> - 0.6-1.svn2298.0blag.f9
- Update to KDE4 branch
  https://kdenlive.svn.sourceforge.net/svnroot/kdenlive/branches/KDE4

* Tue Jul  8 2008 jeff <moe@blagblagblag.org> - 0.6-1.svn2298.0blag.f9
- Update to svn r2298
- New Requires
- kdenlive-svn-r2298-renderer-CMakeLists.patch 

* Sun Nov 11 2007 jeff <moe@blagblagblag.org> - 0.5-1blag.f7
- Update to 0.5 final

* Tue Apr 17 2007 jeff <moe@blagblagblag.org> - 0.5-0svn20070417.0blag.fc6
- svn to 20070417

* Fri Apr  6 2007 jeff <moe@blagblagblag.org> - 0.5-0svn20070406.0blag.fc6
- svn to 20070406

* Tue Apr  3 2007 jeff <moe@blagblagblag.org> - 0.5-0svn20070403.0blag.fc6
- svn to 20070403

* Thu Mar 22 2007 jeff <moe@blagblagblag.org> - 0.5-0svn20070322.0blag.fc6
- svn to 20070322

* Thu Mar 15 2007 jeff <moe@blagblagblag.org> - 0.5-0svn20070316.0blag.fc6
- BLAG'd

* Sun Apr 27 2003 Jason Wood <jasonwood@blueyonder.co.uk> 0.2.2-1mdk
- First stab at an RPM package.
- This is taken from kdenlive-0.2.2 source package.
