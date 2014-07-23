%global shinken_user shinken
%global shinken_group shinken

Summary:        Python Monitoring tool
Name:           shinken
Version:        1.4
Release:        2%{?dist}
URL:            http://www.%{name}-monitoring.org
Source0:        http://www.%{name}-monitoring.org/pub/%{name}_%{version}+kaji.orig.tar.gz
#Source1:        %{name}-etc.tar.gz
License:        AGPLv3+
Requires:       python 
Requires:       python-pyro 
Requires:       python-simplejson 
Requires(post):  chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
Requires:       nmap 
Requires:       sudo  
Patch0:         10_webui.patch
Patch1:         11_shinken_init.patch
Patch2:         12_fix_worker_restart.patch
Patch3:         13_fix_ndo_mysql.patch
Patch4:         14_fix_fedora_init_shinken.patch
Patch5:         15_fix_setup_python24.patch
Patch6:         16_clean_trigger_functions.patch
#Patch7:         17_small_fix_nrpe_protocol.patch
Patch8:         18_fix_graphite_broker.patch

BuildRequires:  python-devel
BuildRequires:  python-setuptools
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
Requires:       python-pyro
Requires:       python-simplejson
Requires(post):  chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts

%description common
Common files for shinken monitoring

# BROKER MODULES
%package module-broker-ndodb-mysql
Summary: Shinken
Group:          Application/System
Requires: %{name}-common = %{version}-%{release}, MySQL-python

%description module-broker-ndodb-mysql
Shinken broker NdoDB module for Mysql


%package module-broker-webui
Summary: Shinken
Group:          Application/System
Requires: %{name}-common = %{version}-%{release}

%description module-broker-webui
Shinken broker WebUI module 


%package module-broker-livestatus
Summary: Shinken module
Group:          Application/System
Requires: %{name}-common = %{version}-%{release}

%description module-broker-livestatus
Shinken Broker Livestatus module


%package module-broker-livestatus-logstore-mongodb
Summary: Shinken module
Group:          Application/System
Requires: %{name}-module-broker-livestatus = %{version}-%{release}

%description module-broker-livestatus-logstore-mongodb
Shinken MongoDB Logstore module for Livestatus


%package module-broker-livestatus-logstore-null
Summary: Shinken module
Group:          Application/System
Requires: %{name}-module-broker-livestatus = %{version}-%{release}

%description module-broker-livestatus-logstore-null
Shinken Null Logstore module for Livestatus


%package module-broker-livestatus-logstore-sqlite
Summary: Shinken module
Group:          Application/System
Requires: %{name}-module-broker-livestatus = %{version}-%{release}

%description module-broker-livestatus-logstore-sqlite
Shinken Sqlite Logstore module for Livestatus


%package module-broker-perfdata-host
Summary: Shinken module
Group:          Application/System
Requires: %{name}-common = %{version}-%{release}

%description module-broker-perfdata-host
Shinken Host perfdata module for Broker


%package module-broker-perfdata-service
Summary: Shinken module
Group:          Application/System
Requires: %{name}-common = %{version}-%{release}

%description module-broker-perfdata-service
Shinken Service perfdata module for Broker


%package module-broker-simplelog
Summary: Shinken module
Group:          Application/System
Requires: %{name}-common = %{version}-%{release}

%description module-broker-simplelog
Shinken Simplelog module for Broker


# ARBITER MODULES
%package module-arbiter-hack_poller_tag_by_macros
Summary: Shinken module
Group:          Application/System
Requires: %{name}-common = %{version}-%{release}

%description module-arbiter-hack_poller_tag_by_macros
Shinken Arbiter module for centreon


%package module-arbiter-hot_dependencies_arbiter
Summary: Shinken module
Group:          Application/System
Requires: %{name}-common = %{version}-%{release}

%description module-arbiter-hot_dependencies_arbiter
Shinken Hot dependencies module for Arbiter

# RECEIVER MODULES
%package module-receiver-commandfile
Summary: Shinken module
Group:          Application/System
Requires: %{name}-common = %{version}-%{release}

%description module-receiver-commandfile
Shinken Commandfile module for Arbiter or Receiver


%package module-receiver-nsca
Summary: Shinken module
Group:          Application/System
Requires: %{name}-common = %{version}-%{release}

%description module-receiver-nsca
Shinken NSCA module for Receiver

# POLLER MODULE
%package module-poller-nrpe
Summary: Shinken module
Group:          Application/System
Requires: %{name}-common = %{version}-%{release}

%description module-poller-nrpe
Shinken NRPE module for Poller


# OTHER MODULE
%package module-retention-pickle
Summary: Shinken module
Group:          Application/System
Requires: %{name}-common = %{version}-%{release}

%description module-retention-pickle
Shinken retention module for Arbiter, Scheduler, Broker


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
#%patch7 -p1
%patch8 -p1

# clean git files/
find . -name '.gitignore' -exec rm -f {} \;

# Check confuguration files 
sed -i -e 's!./$SCRIPT!python ./$SCRIPT!' test/quick_tests.sh
sed -i -e 's!include var/void_for_git!exclude var/void_for_git!'  MANIFEST.in

rm -rf  shinken/webui/plugins/eue shinken/webui/plugins/mobile/htdocs/css/log.css shinken/webui/plugins/mobile/htdocs/css/system.css shinken/webui/plugins/mobile/htdocs/css/details.css etc/packs/os/collectd/discovery.cfg etc/packs/databases/mongodb/macros.cfg shinken/webui/plugins_skonf bin/shinken-skonf etc/packs/trending shinken/modules/glances_ui/plugins/cv_memory/htdocs/js/memory.js 

%build
%{__python} setup.py build 

%install

#find %{buildroot} -size 0 -delete

%{__python} setup.py install -O1 --skip-build --root %{buildroot} --install-scripts=/usr/sbin/ --owner %{shinken_user} --group %{shinken_group}

install -d -m0755 %{buildroot}%{_sbindir}
install -p -m0755 bin/shinken-{arbiter,admin,discovery,broker,poller,reactionner,receiver,scheduler} %{buildroot}%{_sbindir}

install -d -m0755 %{buildroot}%{python_sitelib}/%{name}
install -p %{name}/*.py %{buildroot}%{python_sitelib}/%{name}
cp -rf %{name}/{clients,core,misc,modules,objects,plugins,webui,daemons} %{buildroot}%{python_sitelib}/%{name}

install -d -m0755 %{buildroot}%{_sysconfdir}/%{name}/
rm -rf %{buildroot}%{_sysconfdir}/%{name}/*

install -d -m0755 %{buildroot}%{_sysconfdir}/%{name}/objects
install -d -m0755 %{buildroot}%{_sysconfdir}/%{name}/objects/{contacts,discovery,hosts,services}

#install -p -m0644 for_fedora/etc/objects/contacts/nagiosadmin.cfg %{buildroot}%{_sysconfdir}/%{name}/objects/contacts/nagiosadmin.cfg
#install -p -m0644 for_fedora/etc/objects/hosts/localhost.cfg %{buildroot}%{_sysconfdir}/%{name}/objects/hosts/localhost.cfg
#install -p -m0644 for_fedora/etc/objects/services/linux_disks.cfg %{buildroot}%{_sysconfdir}/%{name}/objects/services/linux_disks.cfg
#install -p -m0644 for_fedora/etc/htpasswd.users %{buildroot}%{_sysconfdir}/%{name}/htpasswd.users
#install -p -m0644 for_fedora/etc/%{name}-specific.cfg %{buildroot}%{_sysconfdir}/%{name}/
#install -p -m0644 for_fedora/etc/discovery*.cfg %{buildroot}%{_sysconfdir}/%{name}/
#install -p -m0644 for_fedora/etc/{contactgroups,nagios,timeperiods,%{name}-specific,escalations,servicegroups,resource,templates}.cfg %{buildroot}%{_sysconfdir}/%{name}/
#install -p -m0644 for_fedora/etc/{brokerd,pollerd,reactionnerd,receiverd,schedulerd}.ini %{buildroot}%{_sysconfdir}/%{name}/

cp -fr debian/etc/*  %{buildroot}%{_sysconfdir}/%{name}/

install -d -m0755 %{buildroot}%{_initrddir}
install -p -m0644 for_fedora/init.d/%{name}-arbiter %{buildroot}%{_initrddir}/%{name}-arbiter
install -p -m0644 for_fedora/init.d/%{name}-scheduler %{buildroot}%{_initrddir}/%{name}-scheduler
install -p -m0644 for_fedora/init.d/%{name}-poller %{buildroot}%{_initrddir}/%{name}-poller
install -p -m0644 for_fedora/init.d/%{name}-broker %{buildroot}%{_initrddir}/%{name}-broker
install -p -m0644 for_fedora/init.d/%{name}-reactionner %{buildroot}%{_initrddir}/%{name}-reactionner
install -p -m0644 for_fedora/init.d/%{name}-receiver %{buildroot}%{_initrddir}/%{name}-receiver

install -d -m0755 %{buildroot}%{_sysconfdir}/logrotate.d
install -p -m0644 for_fedora/%{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/shinken

install -d -m0755 %{buildroot}%{_sysconfdir}/tmpfiles.d
install -m0644  for_fedora/%{name}-tmpfiles.conf %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

install -d -m0755 %{buildroot}%{_localstatedir}/log/%{name}
install -d -m0755 %{buildroot}%{_localstatedir}/log/%{name}/archives
install -d -m0755 %{buildroot}%{_localstatedir}/lib/%{name}

mkdir -p %{buildroot}%{_localstatedir}/run/
install -d -m0755 %{buildroot}%{_localstatedir}/run/%{name}

install -d -m0755 %{buildroot}%{_mandir}/man3
install -p -m0644 doc/man/* %{buildroot}%{_mandir}/man3

install -d -m0755 %{buildroot}%{_usr}/lib/%{name}/plugins/discovery
install  -m0755 libexec/*.py %{buildroot}%{_usr}/lib/%{name}/plugins
install  -m0644 libexec/*.ini %{buildroot}%{_usr}/lib/%{name}/plugins
install  -m0755 libexec/discovery/*.py %{buildroot}%{_usr}/lib/%{name}/plugins/discovery

# ????
for lib in %{buildroot}%{python_sitearch}/%{name}/*.py; do
 sed '/\/usr\/bin\/env/d' $lib > $lib.new &&
 touch -r $lib $lib.new &&
 mv $lib.new $lib
done

# ????
for Files in %{buildroot}%{python_sitelib}/%{name}/__init__.py %{buildroot}%{python_sitelib}/%{name}/core/__init__.py %{buildroot}%{python_sitelib}/%{name}/daemons/*.py %{buildroot}%{python_sitelib}/%{name}/modules/{openldap_ui.py,nrpe_poller.py,livestatus_broker/livestatus_query_cache.py} ; do
  %{__sed} -i.orig -e 1d ${Files}
  touch -r ${Files}.orig ${Files}
  %{__rm} ${Files}.orig
done

chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/css/font-awesome-ie7.min.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/css/font-awesome.min.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/shinken-greeting.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/system/views/log.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/login/htdocs/css/login.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/jquery.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/application.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/eltdetail/htdocs/js/domtab.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/dashboard/views/dashboard.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/problems/views/widget_problems.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/dashboard/htdocs/css/fullscreen.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/README.md
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/css/bootstrap.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/dashboard/htdocs/css/shinken-currently.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/impacts/views/impacts.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/dashboard/htdocs/js/jquery.jclock.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/views/widget.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/views/pagination_element.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/css/custom/layout.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/dashboard/htdocs/css/fullscreen-widget.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/css/bootstrap.min.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/font/fontawesome-webfont.svg
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/views/header_element.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/dashboard/htdocs/css/dashboard.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/bootstrap-scrollspy.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins_hostd/login/htdocs/js/jQuery.dPassword.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/dashboard/htdocs/css/widget.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins_hostd/login/htdocs/css/login.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/jquery.meow.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/problems/views/widget_last_problems.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/eltdetail/htdocs/css/eltdetail.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/system/htdocs/css/system.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/dashboard/views/fullscreen.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/css/elements/jquery.meow.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/bootstrap-carousel.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/views/footer_element.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/system/htdocs/css/log.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/problems/views/problems.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/bootstrap.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/bootstrap.min.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/google-code-prettify/prettify.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/impacts/htdocs/css/impacts.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/dashboard/views/currently.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/login/views/login.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/bootstrap-typeahead.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/system/views/system.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/google-code-prettify/prettify.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/eltdetail/views/eltdetail.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/css/docs.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/views/layout.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/css/font-awesome.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/css/font-awesome-ie7.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/shinkenui.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/plugins/system/views/system_widget.tpl
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/js/bootstrap-alert.js
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/htdocs/css/custom/badger.css
chmod -x %{buildroot}%{python_sitelib}/%{name}/webui/views/navigation_element.tpl


#sed -i -e 's!/usr/local/shinken/libexec!%{_libdir}/nagios/plugins!' %{buildroot}%{_sysconfdir}/%{name}/resource.cfg
#sed -i -e 's!/usr/lib/nagios/plugins!%{_libdir}/nagios/plugins!' %{buildroot}%{_sysconfdir}/%{name}/resource.cfg
sed -i -e 's!/usr/local/shinken/var/arbiterd.pid!/var/run/shinken/arbiterd.pid!' %{buildroot}%{_sysconfdir}/%{name}/shinken.cfg
sed -i -e 's!command_file=/usr/local/shinken/var/rw/nagios.cmd!command_file=/var/lib/shinken/nagios.cmd!' %{buildroot}%{_sysconfdir}/%{name}/shinken.cfg
#sed -i -e 's!cfg_file=hostgroups.cfg!!' %{buildroot}%{_sysconfdir}/%{name}/shinken.cfg
#sed -i -e 's!,Windows_administrator!!' %{buildroot}%{_sysconfdir}/%{name}/contactgroups.cfg
sed -i -e 's!/usr/local/shinken/src/!/usr/sbin/!' FROM_NAGIOS_TO_SHINKEN
sed -i -e 's!/usr/local/nagios/etc/!/etc/shinken/!' FROM_NAGIOS_TO_SHINKEN
sed -i -e 's!/usr/local/shinken/src/etc/!/etc/shinken/!' FROM_NAGIOS_TO_SHINKEN
sed -i -e 's!(you can also be even more lazy and call the bin/launch_all.sh script).!!' FROM_NAGIOS_TO_SHINKEN

rm -rf %{buildroot}%{_localstatedir}/{log,run,lib}/%{name}/void_for_git
rm %{buildroot}%{_sysconfdir}/default/shinken
rm -rf %{buildroot}%{_sysconfdir}/init.d/shinken*
rm -rf %{buildroot}%{_usr}/lib/%{name}/plugins/*.{pyc,pyo}
rm -rf %{buildroot}%{_sbindir}/shinken-{arbiter,discovery,broker,poller,reactionner,receiver,scheduler}.py

find  %{buildroot}%{python_sitelib}/%{name} -type f | xargs sed -i 's|#!/usr/bin/python||g' 

chmod +x %{buildroot}%{python_sitelib}/%{name}/{acknowledge.py,trigger_functions.py,__init__.py,action.py,db_sqlite.py,dependencynode.py,satellite.py,bin.py,notification.py,sorteddict.py,skonfuiworker.py,arbiterlink.py,eventhandler.py,autoslots.py,modulesmanager.py,borg.py,memoized.py,singleton.py}

sed -i 's|#!/usr/bin/env python||g' %{buildroot}%{python_sitelib}/%{name}/webui/plugins/mobile/mobile.py
sed -i 's|#!/usr/bin/env python||g' %{buildroot}%{python_sitelib}/%{name}/modules/webui_broker/helper.py
sed -i 's|#!/usr/bin/env python||g' %{buildroot}%{python_sitelib}/%{name}/webui/plugins/mobile/mobile.py
sed -i 's|#!/usr/bin/env python||g' %{buildroot}%{python_sitelib}/%{name}/modules/webui_broker/helper.py
rm -rf  %{buildroot}%{python_sitelib}/%{name}/webui/plugins/user/{__init__.pyo,__init__.pyc}
rm -rf  %{buildroot}%{python_sitelib}/%{name}/webui/plugins/eue
chmod -x %{buildroot}%{python_sitelib}/%{name}/{acknowledge.py,trigger_functions.py,__init__.py}

# Delete useless files and modules
rm -rf %{buildroot}%{_sysconfdir}/%{name}/shinken-specific/arbiter-collectd.cfg
rm -rf %{buildroot}%{_sysconfdir}/%{name}/shinken-specific/arbiter-ws.cfg
rm -rf %{buildroot}%{_sysconfdir}/%{name}/shinken-specific/broker-graphite.cfg
rm -rf %{buildroot}%{_sysconfdir}/%{name}/shinken-specific/broker-webui-cfgpassword.cfg
rm -rf %{buildroot}%{_sysconfdir}/%{name}/shinken-specific/broker-webui-mongodb.cfg
rm -rf %{buildroot}%{_sysconfdir}/%{name}/shinken-specific/broker-webui-sqlitedb.cfg
rm -rf %{buildroot}%{_sysconfdir}/%{name}/shinken-specific/broker-webui-graphite.cfg
rm -rf %{buildroot}%{_sysconfdir}/%{name}/shinken-specific/broker-npcd.cfg
rm -rf %{buildroot}%{_sysconfdir}/%{name}/shinken-specific/retention-mongodb.cfg
rm -rf %{buildroot}%{_sysconfdir}/%{name}/packs/.placeholder
rm -rf %{buildroot}%{python_sitelib}/%{name}/discovery/
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/*.pyo
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/__init__.pyo
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/*.pyc
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/__init__.pyc
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/*/*.pyo
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/*/*.pyc
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/active_directory_ui.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/android_sms.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/aws_import_arbiter.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/canopsis_broker.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/cfg_password_ui_.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/collectd_arbiter.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/couchdb_broker/
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/dummy_*
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/file_tag_arbiter.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/glances_ui/
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/glpi_arbiter.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/glpidb_broker/
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/graphite_broker.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/graphite_ui.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/ip_tag_arbiter/
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/hack_commands_poller_tag_arbiter.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/landscape_import_arbiter.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/memcache_retention_scheduler.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/merlindb_broker/
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/mongodb_generic.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/mongodb_retention.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/mysql_import_arbiter.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/nagios_retention_file_scheduler.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/ndodb_oracle_broker/
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/npcdmod_broker.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/openldap_ui.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/passwd_ui.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/pickle_retention_file_scheduler.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/pnp_ui.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/redis_retention_scheduler.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/sqlite_generic.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/status_dat_broker/
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/syslog_broker.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/trending_broker.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/tsca/
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/ws_arbiter.py
rm -rf %{buildroot}%{python_sitelib}/%{name}/modules/zmq_broker.py


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
%{python_sitelib}/%{name}/*.py
%{python_sitelib}/%{name}/*.pyc
%{python_sitelib}/%{name}/*.pyo
%{python_sitelib}/%{name}/clients/
%{python_sitelib}/%{name}/core/
%{python_sitelib}/%{name}/daemons/
%{python_sitelib}/%{name}/misc/
%{python_sitelib}/%{name}/plugins/
%{python_sitelib}/%{name}/objects/
%{python_sitelib}/%{name}/trending/
%{python_sitelib}/%{name}/modules/__init__.py*
%{python_sitelib}/Shinken-1.4-py2.6.egg-info
%{_sbindir}/%{name}-receiver*
%{_sbindir}/%{name}-discovery
%{_sbindir}/%{name}-admin
%{_sbindir}/%{name}-hostd
%{_sbindir}/%{name}-packs
%{_usr}/lib/%{name}/plugins
%doc etc/packs COPYING THANKS 
%{_mandir}/man3/%{name}-*
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%attr(-,%{shinken_user} ,%{shinken_group}) %dir %{_localstatedir}/log/%{name}
%attr(-,%{shinken_user} ,%{shinken_group}) %dir %{_localstatedir}/lib/%{name}
%attr(-,%{shinken_user} ,%{shinken_group}) %dir %{_localstatedir}/run/%{name}
# arbiter
%attr(0755,root,root) %{_initrddir}/%{name}-arbiter
%{_sbindir}/%{name}-arbiter*
%{_mandir}/man3/%{name}-arbiter*
#%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/shinken.cfg
%config(noreplace) %{_sysconfdir}/%{name}/hosts/
%config(noreplace) %{_sysconfdir}/%{name}/packs/
%config(noreplace) %{_sysconfdir}/%{name}/commands.cfg
%config(noreplace) %{_sysconfdir}/%{name}/contacts.cfg
%config(noreplace) %{_sysconfdir}/%{name}/resource.cfg
%config(noreplace) %{_sysconfdir}/%{name}/templates.cfg
%config(noreplace) %{_sysconfdir}/%{name}/timeperiods.cfg
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/arbiter.cfg
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/realms.cfg
#reactionner
%attr(0755,root,root) %{_initrddir}/%{name}-reactionner
%{_sbindir}/%{name}-reactionner*
%{_mandir}/man3/%{name}-reactionner*
%config(noreplace) %{_sysconfdir}/%{name}/daemons/reactionnerd.ini
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/reactionner.cfg
# scheduler
%attr(0755,root,root) %{_initrddir}/%{name}-scheduler
%{_sbindir}/%{name}-scheduler*
%{_mandir}/man3/%{name}-scheduler*
%config(noreplace) %{_sysconfdir}/%{name}/daemons/schedulerd.ini
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/scheduler.cfg
# poller
%attr(0755,root,root) %{_initrddir}/%{name}-poller
%{_sbindir}/%{name}-poller*
%{_mandir}/man3/%{name}-poller*
%config(noreplace) %{_sysconfdir}/%{name}/daemons/pollerd.ini
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/poller.cfg
# broker
%attr(0755,root,root) %{_initrddir}/%{name}-broker
%{_sbindir}/%{name}-broker*
%{_mandir}/man3/%{name}-broker*
%config(noreplace) %{_sysconfdir}/%{name}/daemons/brokerd.ini
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/broker.cfg
# receiver
%attr(0755,root,root) %{_initrddir}/%{name}-receiver
%{_sbindir}/%{name}-receiver*
%{_mandir}/man3/%{name}-receiver*
%config(noreplace) %{_sysconfdir}/%{name}/daemons/receiverd.ini
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/receiver.cfg


# ARBITER MODULES
%files module-arbiter-hot_dependencies_arbiter
%{python_sitelib}/%{name}/modules/hot_dependencies_arbiter.*
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/arbiter-hotdependencies.cfg

%files module-arbiter-hack_poller_tag_by_macros
%{python_sitelib}/%{name}/modules/hack_poller_tag_by_macros*
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/arbiter-hack_poller_tag_by_macros.cfg

# RECEIVER MODULES
%files module-receiver-nsca
%{python_sitelib}/%{name}/modules/nsca.*
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/arbiter-nsca.cfg

%files module-receiver-commandfile
%{python_sitelib}/%{name}/modules/named_pipe.*
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/commandfile.cfg

# POLLER MODULES
%files module-poller-nrpe
%{python_sitelib}/%{name}/modules/nrpe_poller.*
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/poller-nrpe.cfg

# BROKER MODULES
%files module-broker-simplelog
%{python_sitelib}/%{name}/modules/simplelog_broker.py*
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/broker-simplelog.cfg

%files module-broker-perfdata-host
%{python_sitelib}/%{name}/modules/host_perfdata_broker/
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/broker-perfdata-host.cfg

%files module-broker-perfdata-service
%{python_sitelib}/%{name}/modules/service_perfdata_broker/
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/broker-perfdata-service.cfg

%files module-broker-livestatus
%{python_sitelib}/%{name}/modules/livestatus_broker/*
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/broker-livestatus.cfg

%files module-broker-livestatus-logstore-mongodb
%{python_sitelib}/%{name}/modules/logstore_mongodb.*
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/broker-livestatus-mongodb.cfg

%files module-broker-livestatus-logstore-null
%{python_sitelib}/%{name}/modules/logstore_null.*
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/broker-livestatus-null.cfg

%files module-broker-livestatus-logstore-sqlite
%{python_sitelib}/%{name}/modules/logstore_sqlite.*
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/broker-livestatus-sqlite.cfg

%files module-broker-ndodb-mysql
%{python_sitelib}/%{name}/modules/ndodb_mysql_broker
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/broker-ndodb-mysql.cfg

%files module-broker-webui
%{python_sitelib}/%{name}/webui
%{python_sitelib}/%{name}/modules/webui_broker/
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/broker-webui.cfg

# OTHER MODULES
%files module-retention-pickle
%{python_sitelib}/%{name}/modules/pickle_retention_file_generic.*
%config(noreplace) %{_sysconfdir}/%{name}/shinken-specific/retention-picklefile.cfg

%changelog
* Tue Jan 28 2014 Thibault Cohen <thibault.cohen@savoirfairelinux.com> - 1.4-2
- Synchronise with debian packages

* Wed May 27 2013 David Hannequin <david.hannequin@gmail.com> - 1.4-1
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

* Wed Nov 5 2012 David Hannequin <david.hannequin@gmail.com> - 1.0.1-6
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

* Sun Apr 29 2011 David Hannequin <david.hannequin@gmail.com> - 0.6-1
- Fisrt release for fedora.
