%global shinken_user shinken
%global shinken_group shinken

Summary:        Python Monitoring tool
Name:           shinken
Version:        2.2
Release:        1kaji0.2
URL:            http://www.%{name}-monitoring.org
Source0:        http://www.%{name}-monitoring.org/pub/%{name}_%{version}.orig.tar.gz
License:        AGPLv3+
Requires:       python
Requires:       python-pycurl
Requires:       python-cherrypy
Requires:       python-simplejson
Requires(post):  chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
#Requires:       nmap
Requires:       sudo

BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  graphviz
#BuildRequires:  python-sphinx
Group:          Application/System

BuildRoot:      %{_tmppath}/%{name}-%{version}-buildroot
Buildarch:      noarch

%description
Shinken is a new monitoring tool written in Python.
The main goal of Shinken is to allow users to have a fully flexible
architecture for their monitoring system that can easily scale to large
environments.
Shinken also provide interfaces with NDODB and Merlin database,
Livestatus connector Shinken does not include any human interfaces.

%package common
Summary: Shinken Common files
Group:          Application/System
#Requires: %{name} = %{version}-%{release}
Requires:       python
Requires:       python-pycurl

Requires(post):  chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts

%description common
Common files for shinken monitoring

%package doc
Summary: Shinken Documentation
Group:          Application/System

%description doc

%prep
%setup -q

# Apply all patches
for patch_file in $(cat debian/patches/series | grep -v "^#")
do
%{__patch} -p1 < debian/patches/$patch_file
done

# clean git files/
find . -name '.gitignore' -exec rm -f {} \;


%build
#%{__python} setup.py build
%{__python} manpages/generate_manpages.py
cd doc && make html

%install

#find %{buildroot} -size 0 -delete
rm -rf %{buildroot}

%{__python} setup.py install -O1 --root=%{buildroot} --install-scripts=%{_sbindir} --install-lib=%{python_sitelib}  --owner %{shinken_user} --group %{shinken_group}

install -d -m0755  %{buildroot}%{_sysconfdir}/%{name}/
rm -rf %{buildroot}%{_sysconfdir}/%{name}/*
cp -rf  debian/etc/*  %{buildroot}%{_sysconfdir}/%{name}/
cp -rf  debian/kaji/etc/*  %{buildroot}%{_sysconfdir}/%{name}/
install -d -m0755 %{buildroot}/%{_mandir}/man8/
install -p -m0644 manpages/manpages/* %{buildroot}/%{_mandir}/man8/
install -d -m0755 %{buildroot}/usr/share/pyshared/shinken
mv  %{buildroot}/var/lib/shinken/modules  %{buildroot}/usr/share/pyshared/shinken

# Clean useless
rm -rf %{buildroot}/var/lib/shinken/share/templates
rm -rf %{buildroot}/var/lib/shinken/share/images
rm -rf %{buildroot}/%{python_sitelib}/modules/
rm -rf %{buildroot}/var/lib/shinken/doc/
rm -rf %{buildroot}/etc/shinken/packs/.placeholder
rm -rf %{buildroot}/var/lib/shinken/inventory/
rm -rf %{buildroot}/var/lib/shinken/libexec/
rm -rf %{buildroot}/var/lib/shinken/libexec/

# logrotate
install -d -m0755 %{buildroot}%{_sysconfdir}/logrotate.d
install -p -m0644 for_fedora/%{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/shinken

# tmpfiles
install -d -m0755 %{buildroot}%{_sysconfdir}/tmpfiles.d
install -m0644  for_fedora/%{name}-tmpfiles.conf %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

# log
install -d -m0755 %{buildroot}%{_localstatedir}/log/%{name}
install -d -m0755 %{buildroot}%{_localstatedir}/log/%{name}/archives
# lib
install -d -m0755 %{buildroot}%{_localstatedir}/lib/%{name}
#run
mkdir -p %{buildroot}%{_localstatedir}/run/
install -d -m0755 %{buildroot}%{_localstatedir}/run/%{name}

%clean

%pre  common
getent group %{shinken_group} >/dev/null || groupadd -r %{shinken_group}
getent passwd %{shinken_user} >/dev/null || useradd -r -g %{shinken_group} -d /home/%{shinken_user} -m -s /bin/bash %{shinken_user}
exit 0

%post common
if [ $1 -eq 1 ] ; then
  /sbin/chkconfig --add %{name}-arbiter || :
  /sbin/chkconfig --add %{name}-broker || :
  /sbin/chkconfig --add %{name}-poller || :
  /sbin/chkconfig --add %{name}-reactionner || :
  /sbin/chkconfig --add %{name}-scheduler || :
  /sbin/chkconfig --add %{name}-receiver || :
fi

%preun common
if [ $1 -eq 0 ] ; then
  /sbin/service %{name}-arbiter stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del %{name}-arbiter || :
  /sbin/service %{name}-broker stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del %{name}-broker || :
  /sbin/service %{name}-poller stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del %{name}-poller || :
  /sbin/service %{name}-reactionner stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del %{name}-reactionner || :
  /sbin/service %{name}-scheduler stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del %{name}-scheduler || :
  /sbin/service %{name}-receiver stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del %{name}-receiver || :
fi

%postun common



%files common
#%attr(0755,root,root) %{_initrddir}/%{name}
%{python_sitelib}/%{name}
%{python_sitelib}/Shinken-*.egg-info
/var/lib/shinken/cli/
/usr/share/pyshared/shinken
#%{_usr}/lib/%{name}/plugins
#%doc etc/packs COPYING THANKS
%config(noreplace) %{_sysconfdir}/default/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%attr(-,%{shinken_user} ,%{shinken_group}) %dir %{_localstatedir}/log/%{name}
%attr(-,%{shinken_user} ,%{shinken_group}) %dir %{_localstatedir}/lib/%{name}
%attr(-,%{shinken_user} ,%{shinken_group}) %dir %{_localstatedir}/run/%{name}
# shinken
%attr(0755,root,root) %{_sysconfdir}/init.d/%{name}*
%{_sbindir}/%{name}
#man
%{_mandir}/man8/%{name}*
# shinken-discovery
%{_sbindir}/%{name}-discovery
# arbiter
%{_sbindir}/%{name}-arbiter
#%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/shinken.cfg
%config(noreplace) %{_sysconfdir}/%{name}/hosts/
%config(noreplace) %{_sysconfdir}/%{name}/packs/
%config(noreplace) %{_sysconfdir}/%{name}/commands.cfg
%config(noreplace) %{_sysconfdir}/%{name}/contacts.cfg
%config(noreplace) %{_sysconfdir}/%{name}/resource.cfg
%config(noreplace) %{_sysconfdir}/%{name}/templates.cfg
%config(noreplace) %{_sysconfdir}/%{name}/timeperiods.cfg
%config(noreplace) %{_sysconfdir}/%{name}/arbiters/arbiter.cfg
%config(noreplace) %{_sysconfdir}/%{name}/realms/realms.cfg
#reactionner
%{_sbindir}/%{name}-reactionner
%config(noreplace) %{_sysconfdir}/%{name}/daemons/reactionnerd.ini
%config(noreplace) %{_sysconfdir}/%{name}/reactionners/reactionner.cfg
# scheduler
%{_sbindir}/%{name}-scheduler
%config(noreplace) %{_sysconfdir}/%{name}/daemons/schedulerd.ini
%config(noreplace) %{_sysconfdir}/%{name}/schedulers/scheduler.cfg
# poller
%{_sbindir}/%{name}-poller
%config(noreplace) %{_sysconfdir}/%{name}/daemons/pollerd.ini
%config(noreplace) %{_sysconfdir}/%{name}/pollers/poller.cfg
# broker
%{_sbindir}/%{name}-broker
%config(noreplace) %{_sysconfdir}/%{name}/daemons/brokerd.ini
%config(noreplace) %{_sysconfdir}/%{name}/brokers/broker.cfg
# receiver
%{_sbindir}/%{name}-receiver
%config(noreplace) %{_sysconfdir}/%{name}/daemons/receiverd.ini
%config(noreplace) %{_sysconfdir}/%{name}/receivers/receiver.cfg

%files doc
%docdir %{_localstatedir}/lib/%{name}/doc/build/html

%changelog
* Tue Feb 17 2015 Thibault Cohen <thibault.cohen@savoirfairelinux.com> - 2.2-1kaji0.2
- Synchronise with debian packages

* Thu Jan 22 2015 Thibault Cohen <thibault.cohen@savoirfairelinux.com> - 2.0.3-3kaji0.2
- Synchronise with debian packages

* Tue Jan 28 2014 Thibault Cohen <thibault.cohen@savoirfairelinux.com> - 1.4-2
- Synchronise with debian packages

* Mon May 27 2013 David Hannequin <david.hannequin@gmail.com> - 1.4-1
- Update from upstream.

* Mon Mar 11 2013 David Hannequin <david.hannequin@gmail.com> - 1.2.4-6
- Fix broker summary.

* Sat Mar 9 2013 David Hannequin <david.hannequin@gmail.com> - 1.2.4-5
- Add Webui menu patch.

* Wed Mar 6 2013 David Hannequin <david.hannequin@gmail.com> - 1.2.4-2
- Fix discovery rules.

* Sun Feb 24 2013 David Hannequin <david.hannequin@gmail.com> - 1.2.4-1
- Update from upstream.

* Wed Jan 30 2013 David Hannequin <david.hannequin@gmail.com> - 1.2.3-1
- Update from upstream.

* Sat Dec 15 2012 David Hannequin <david.hannequin@gmail.com> - 1.2.2-1
- Update from upstream,
- Delete eue module,
- Fix web site url,
- Fix Bug 874092 (thanks Sébastien Andreatta).

* Fri Dec 14 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-7
- Fix uninstall receiver.

* Mon Nov 5 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-6
- Fix bug 874089.

* Sun Sep 16 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-5
- Add support of el6,
- Remove shebang from Python libraries,
- Delete echo printing,
- Remove CFLAGS.

* Mon Sep 10 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-4
- Add COPYING README THANKS file,
- delete defattr.

* Sun Sep 09 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-3
- Delete require python-sqlite2.

* Sun Jul 22 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-2
- Add build patch.

* Tue Mar 13 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-1
- Update from upstream,
- Add shinken packs

* Mon Oct 24 2011 David Hannequin <david.hannequin@gmail.com> - 0.8.1-1
- Update from upstream,
- Add manpage,
- Add require nagios plugins.

* Mon May 30 2011 David Hannequin <david.hannequin@gmail.com> - 0.6.5-1
- Update from upstream,
- Add require python-redis,
- Add require python-memcached.

* Mon May 30 2011 David Hannequin <david.hannequin@gmail.com> - 0.6.4-3
- Fix path in default shinken file,
- Fix path in setup.cfg,
- Add file FROM_NAGIOS_TO_SHINKEN.

* Sun May 29 2011 David Hannequin <david.hannequin@gmail.com> - 0.6.4-2
- Fix shinken configuration,
- Replace macro,
- Update from upstreamr.

* Fri May 20 2011 David Hannequin <david.hannequin@gmail.com> - 0.6.4-1
- Update from upstream.

* Fri Apr 29 2011 David Hannequin <david.hannequin@gmail.com> - 0.6-1
- Fisrt release for fedora.
