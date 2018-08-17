#xyr build defines
# This section will be re-written by Jenkins build system.

%define name sspl
%define url  http://gerrit.mero.colo.seagate.com:8080/#/admin/projects
#xyr end defines

%define _unpackaged_files_terminate_build 0
%define _binaries_in_noarch_packages_terminate_build   0

Name:       %{name}
Version:    %{version}
Provides:   %{name} = %{version}
Obsoletes:  %{name} <= %{version}
Release:    %{dist}
Summary:    Installs SSPL
BuildArch:  noarch
Group:      System Environment/Daemons
License:    Seagate Proprietary
URL:        %{url}/%{name}
Source0:    %{name}-%{version}.tgz
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: rpm-build sudo python-Levenshtein
Requires:   python-daemon python-zope-interface python-zope-event python-zope-component python-pika python-jsonschema rabbitmq-server
Requires:   pysnmp systemd-python pygobject2 python-slip-dbus udisks2 python-psutil python-inotify python-paramiko hdparm pyserial facter
Requires:   libsspl_sec libsspl_sec-method_none zabbix20-agent
Requires:   perl(Config::Any)
Requires(pre): shadow-utils

%description
Installs SSPL

%prep
%setup -n sspl/low-level

%build

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%install
# Copy config file and service startup to correct locations

mkdir -p ${RPM_BUILD_ROOT}/etc/{systemd/system,dbus-1/system.d,polkit-1/rules.d,sspl-ll/templates/snmp}
cp -afv files/etc ${RPM_BUILD_ROOT}/

# Copy the service into /opt/seagate/sspl where it will execute from
mkdir -p ${RPM_BUILD_ROOT}/opt/seagate/sspl/low-level
cp -rp . ${RPM_BUILD_ROOT}/opt/seagate/sspl/low-level

%post
case "$1" in
    1)  # Add the sspl-ll user during first install if it doesnt exist
        id -u sspl-ll &>/dev/null || /usr/sbin/useradd -r -g zabbix \
            -s /sbin/nologin  \
            -c "User account to run the sspl-ll service" sspl-ll
        ;;
    
    2)  # In case of upgrade start sspl-ll after upgrade
        systemctl restart sspl-ll.service 2> /dev/null
        ;;
esac

mkdir -p /var/log/journal
systemctl restart systemd-journald

# Have systemd reload
systemctl daemon-reload

# Enable services to start at boot
systemctl enable rabbitmq-server

# Restart dbus with new policy files
systemctl restart dbus

%preun
# Remove configuration in case of uninstall
[[ $1 = 0 ]] &&  rm -f /var/sspl/sspl-configured
systemctl stop sspl-ll.service 2> /dev/null

%files
%defattr(-,sspl-ll,root,-)
/opt/seagate/sspl/*
/etc/sspl_ll.conf.sample
/etc/systemd/system/sspl-ll.service

%changelog
* Fri Aug 10 2018 Ujjwal Lanjewar <ujjwal.lanjewar@seagate.com>
- Added version infrastructure and upgrade support

* Wed Oct 18 2017 Oleg Gut <oleg.gut@seagate.com>
- Reworking spec

* Tue Jun 09 2015 Aden Jake Abernathy <aden.j.abernathy@seagate.com>
- Linking into security libraries to apply authentication signatures

* Mon Jun 01 2015 David Adair <dadair@seagate.com>
- Add jenkins-friendly template.  Convert to single tarball for all of sspl.

* Fri May 29 2015 Aden jake Abernathy <aden.j.abernathy@seagate.com> - 1.0.0-9
- Adding request actuator for journald logging, updating systemd unit file
- Adding enabling and disabling of services, moving rabbitmq init script to unit file

* Fri May 01 2015 Aden jake Abernathy <aden.j.abernathy@seagate.com> - 1.0.0-8
- Adding service watchdog module

* Fri Apr 24 2015 Aden jake Abernathy <aden.j.abernathy@seagate.com> - 1.0.0-7
- Updating to run sspl-ll service as sspl-ll user instead of root

* Fri Feb 13 2015 Aden Jake Abernathy <aden.j.abernathy@seagate.com> - 1.0.0-1
- Initial spec file
