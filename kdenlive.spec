
Name:    kdenlive
Summary: Non-linear video editor
Version: 15.12.2
Release: 2%{?dist}

License: GPLv2+
URL:     http://www.kdenlive.org
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/applications/%{version}/src/kdenlive-%{version}.tar.xz

BuildRequires: desktop-file-utils
BuildRequires: extra-cmake-modules
BuildRequires: gettext
BuildRequires: kf5-rpm-macros
BuildRequires: kf5-karchive-devel
BuildRequires: kf5-kbookmarks-devel
BuildRequires: kf5-kconfig-devel
BuildRequires: kf5-kconfigwidgets-devel
BuildRequires: kf5-kcoreaddons-devel
BuildRequires: kf5-kdoctools-devel
BuildRequires: kf5-kdbusaddons-devel
BuildRequires: kf5-kguiaddons-devel
BuildRequires: kf5-ki18n-devel
BuildRequires: kf5-kiconthemes-devel
BuildRequires: kf5-kitemviews-devel
BuildRequires: kf5-kio-devel
BuildRequires: kf5-kjobwidgets-devel
BuildRequires: kf5-knewstuff-devel
BuildRequires: kf5-knotifications-devel
BuildRequires: kf5-knotifyconfig-devel
BuildRequires: kf5-kplotting-devel
BuildRequires: kf5-ktextwidgets-devel
BuildRequires: kf5-kxmlgui-devel
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

%{?kf5_kinit_requires}
Requires: dvdauthor
Requires: dvgrab
Requires: ffmpeg
Requires: mlt%{?_isa} >= %{mlt_version}
Requires: recordmydesktop

%description
Kdenlive is an intuitive and powerful multi-track video editor, including most
recent video technologies.


%prep
%setup -q


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

## unpackaged files
# legacy/deprecated/unused bits
rm -rfv %{buildroot}%{_datadir}/menu/
rm -rfv %{buildroot}%{_datadir}/pixmaps/

# fix/rename appdata
mv %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml \
   %{buildroot}%{_datadir}/appdata/org.kde.%{name}.appdata.xml


%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/org.kde.%{name}.appdata.xml ||:
desktop-file-validate %{buildroot}%{_datadir}/applications/org.kde.%{name}.desktop


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/mime/packages &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
  touch --no-create %{_datadir}/mime/packages &> /dev/null || :
  update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
  update-desktop-database &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%files
%doc AUTHORS README
%license COPYING
%{_kf5_docdir}/HTML/en/kdenlive/
%{_kf5_bindir}/kdenlive_render
%{_kf5_bindir}/%{name}
%{_datadir}/applications/org.kde.%{name}.desktop
%{_datadir}/appdata/org.kde.%{name}.appdata.xml
%{_kf5_datadir}/kdenlive/
%{_kf5_datadir}/mime/packages/kdenlive.xml
%{_datadir}/mime/packages/westley.xml
%{_datadir}/icons/hicolor/*/*/*
%{_sysconfdir}/xdg/kdenlive_projectprofiles.knsrc
%{_sysconfdir}/xdg/kdenlive_renderprofiles.knsrc
%{_sysconfdir}/xdg/kdenlive_titles.knsrc
%{_sysconfdir}/xdg/kdenlive_wipes.knsrc
%{_kf5_qtplugindir}/mltpreview.so
%{_datadir}/config.kcfg/kdenlivesettings.kcfg
%{_datadir}/knotifications5/kdenlive.notifyrc
%{_datadir}/kservices5/mltpreview.desktop
%{_datadir}/kxmlgui5/kdenlive/
%{_mandir}/man1/kdenlive.1*
%{_mandir}/man1/kdenlive_render.1*



%changelog
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
