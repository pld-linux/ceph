#
# Conditional build:
%bcond_with	hadoop	# Hadoop client (requires JNI)
#
Summary:	User space components of the Ceph file system
Summary(pl.UTF-8):	Działające w przestrzeni użytkownika elementy systemu plików Ceph
Name:		ceph
Version:	0.52
Release:	1
License:	LGPL v2.1 (libraries), GPL v2 (some programs)
Group:		Base
Source0:	http://ceph.newdream.net/download/%{name}-%{version}.tar.bz2
# Source0-md5:	b3b9c8e7160d69cdf735628342a8dee0
Patch0:		%{name}-init-fix.patch
Patch1:		%{name}.logrotate.patch
Patch2:		%{name}-link.patch
URL:		http://ceph.newdream.net/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	boost-devel >= 1.34
BuildRequires:	cryptopp-devel
BuildRequires:	curl-devel
BuildRequires:	expat-devel >= 1.95
BuildRequires:	fcgi-devel
BuildRequires:	gdbm-devel
%{?with_hadoop:BuildRequires:	jdk}
BuildRequires:	keyutils-devel
BuildRequires:	leveldb-devel
BuildRequires:	libaio-devel
BuildRequires:	libatomic_ops
BuildRequires:	libedit-devel >= 2.11
BuildRequires:	libfuse-devel
BuildRequires:	libltdl-devel
BuildRequires:	libs3-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtcmalloc-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	libuuid-devel
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	python >= 1:2.4
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	sed >= 4.0
BuildRequires:	snappy-devel
Requires(post,preun):	/sbin/chkconfig
Requires(preun):	rc-scripts
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	gcephtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	libcls_.*.so.*

%description
Ceph is a distributed network file system designed to provide
excellent performance, reliability, and scalability.

%description -l pl.UTF-8
Ceph to rozproszony sieciowy system plików zaprojektowany z myślą o
dobrej wydajności, wiarygodności i skalowalności.

%package libs
Summary:	Ceph shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone Cepha
Group:		Libraries

%description libs
Ceph shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone Cepha.

%package devel
Summary:	Ceph header files
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Cepha
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains the headers needed to develop programs that use
Ceph.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia programów
wykorzystujących Cepha.

%package static
Summary:	Ceph static libraries
Summary(pl.UTF-8):	Biblioteki statyczne Cepha
License:	LGPLv2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static Ceph libraries.

%description static -l pl.UTF-8
Ten pakiet zawiera biblioteki statyczne Cepha.

%package -n python-ceph
Summary:	Ceph Python bindings
Summary(pl.UTF-8):	Wiązania Pythona do bibliotek Cepha
Group:		Development/Languages/Python
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-ceph
Ceph Python bindings.

%description -n python-ceph -l pl.UTF-8
Wiązania Pythona do bibliotek Cepha.

%package fuse
Summary:	Ceph FUSE-based client
Summary(pl.UTF-8):	Klient Cepha oparty na FUSE
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description fuse
FUSE based client for Ceph distributed network file system.

%description fuse -l pl.UTF-8
Oparty na FUSE klient rozproszonego sieciowego systemu plików Ceph.

%package radosgw
Summary:	rados REST gateway
Summary(pl.UTF-8):	Bramka REST-owa rados
Group:		Applications/System
#Requires:	apache-mod_fcgid

%description radosgw
radosgw is an S3 HTTP REST gateway for the RADOS object store. It is
implemented as a FastCGI module using libfcgi, and can be used in
conjunction with any FastCGI capable web server.

%description radosgw -l pl.UTF-8
radosgw to REST-owa bramka HTTP S3 do przechowalni obiektów RADOS.
Jest zaimplementowana jako moduł FastCGI wykorzystujący libfcgi i może
być używana w połączeniu z dowolnym serwerem WWW obsługującym FastCGI.

%package obsync
Summary:	Synchronize data between cloud object storage providers or a local directory
Summary(pl.UTF-8):	Synchronizacja danych między obiektami przechowywanymi w chmurze i katalogami lokalnymi
Group:		Applications/Networking
Requires:	python
Requires:	python-boto

%description obsync
obsync is a tool to synchronize objects between cloud object storage
providers, such as Amazon S3 (or compatible services), a Ceph RADOS
cluster, or a local directory.

%description obsync -l pl.UTF-8
obsync to narzędzie do synchronizacji obiektów między systemami
przechowującymi obiekty w chmurze, takimi jak Amazon S3 (lub serwisy
kompatybilne) a klastrem Ceph RADOS lub katalogiem lokalnym.

%package resource-agents
Summary:	OCF Resource Agents for Ceph processes
Summary(pl.UTF-8):	Agenci OCF do monitorowania procesów Cepha
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	resource-agents

%description resource-agents
OCF Resource Agents for Ceph processes.

%description resource-agents -l pl.UTF-8
Agenci OCF do monitorowania procesów Cepha.

%package -n hadoop-cephfs
Summary:	Hadoop client for Ceph filesystem
Summary(pl.UTF-8):	Klient Hadoopa dla systemu plików Ceph
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	hadoop

%description -n hadoop-cephfs
Hadoop client for Ceph filesystem.

%description -n hadoop-cephfs -l pl.UTF-8
Klient Hadoopa dla systemu plików Ceph.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1

%{__sed} -i -e '1s,/usr/bin/env python,/usr/bin/python,' src/obsync/obsync

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%{?with_hadoop:CPPFLAGS="%{rpmcppflags} -I%{_jvmdir}/java/include -I%{_jvmdir}/java/include/linux"}
%configure \
	--sbindir=/sbin \
	--with-cryptopp \
	--with-hadoop%{!?with_hadoop:=no} \
	--with-ocf \
	--with-radosgw \
	--with-system-leveldb \
	--with-system-libs3 \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_localstatedir}/{lib/ceph/tmp,log/ceph/stat} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{ceph,bash_completion.d,logrotate.d,rc.d/init.d}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -p src/init-ceph $RPM_BUILD_ROOT/etc/rc.d/init.d/ceph
install -p src/logrotate.conf $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/ceph

%if %{with hadoop}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libhadoopcephfs.{la,a}
%endif

%{__rm} $RPM_BUILD_ROOT%{_libdir}/rados-classes/*.{a,la}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ceph
%service ceph restart

%preun
if [ "$1" = "0" ] ; then
	%service ceph stop
	/sbin/chkconfig --del ceph
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	-n hadoop-cephfs -p /sbin/ldconfig
%postun	-n hadoop-cephfs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# COPYING specifies licenses of individual parts
%doc AUTHORS COPYING README src/sample.ceph.conf src/sample.fetch_config
%attr(754,root,root) /etc/rc.d/init.d/ceph
%dir %{_sysconfdir}/ceph
%attr(755,root,root) %{_bindir}/ceph
%attr(755,root,root) %{_bindir}/cephfs
%attr(755,root,root) %{_bindir}/ceph-conf
%attr(755,root,root) %{_bindir}/ceph-clsinfo
%attr(755,root,root) %{_bindir}/ceph-dencoder
%attr(755,root,root) %{_bindir}/crushtool
%attr(755,root,root) %{_bindir}/monmaptool
%attr(755,root,root) %{_bindir}/osdmaptool
%attr(755,root,root) %{_bindir}/ceph-authtool
%attr(755,root,root) %{_bindir}/ceph-syn
%attr(755,root,root) %{_bindir}/ceph-run
%attr(755,root,root) %{_bindir}/ceph-mon
%attr(755,root,root) %{_bindir}/ceph-mds
%attr(755,root,root) %{_bindir}/ceph-osd
%attr(755,root,root) %{_bindir}/ceph-rbdnamer
%attr(755,root,root) %{_bindir}/librados-config
%attr(755,root,root) %{_bindir}/rados
%attr(755,root,root) %{_bindir}/rbd
%attr(755,root,root) %{_bindir}/ceph-debugpack
%attr(755,root,root) %{_bindir}/ceph-coverage
%dir %{_libdir}/rados-classes
%attr(755,root,root) %{_libdir}/rados-classes/libcls_lock.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_rbd.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_rgw.so*
%attr(755,root,root) /sbin/ceph-disk-activate
%attr(755,root,root) /sbin/ceph-disk-prepare
%attr(755,root,root) /sbin/mkcephfs
%attr(755,root,root) /sbin/mount.ceph
%dir %{_libdir}/ceph
%attr(755,root,root) %{_libdir}/ceph/ceph_common.sh
%config(noreplace) /etc/logrotate.d/ceph
%config(noreplace) %{_sysconfdir}/bash_completion.d/rados
%config(noreplace) %{_sysconfdir}/bash_completion.d/ceph
%config(noreplace) %{_sysconfdir}/bash_completion.d/rbd
%{_mandir}/man8/ceph.8*
%{_mandir}/man8/ceph-authtool.8*
%{_mandir}/man8/ceph-clsinfo.8*
%{_mandir}/man8/ceph-conf.8*
%{_mandir}/man8/ceph-debugpack.8*
%{_mandir}/man8/ceph-dencoder.8*
%{_mandir}/man8/ceph-mds.8*
%{_mandir}/man8/ceph-mon.8*
%{_mandir}/man8/ceph-osd.8*
%{_mandir}/man8/ceph-rbdnamer.8*
%{_mandir}/man8/ceph-run.8*
%{_mandir}/man8/ceph-syn.8*
%{_mandir}/man8/cephfs.8*
%{_mandir}/man8/crushtool.8*
%{_mandir}/man8/librados-config.8*
%{_mandir}/man8/mkcephfs.8*
%{_mandir}/man8/monmaptool.8*
%{_mandir}/man8/mount.ceph.8*
%{_mandir}/man8/osdmaptool.8*
%{_mandir}/man8/rados.8*
%{_mandir}/man8/radosgw.8*
%{_mandir}/man8/radosgw-admin.8*
%{_mandir}/man8/rbd.8*

%dir %{_localstatedir}/lib/ceph
%dir %{_localstatedir}/lib/ceph/tmp
%dir %{_localstatedir}/log/ceph

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcephfs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcephfs.so.1
%attr(755,root,root) %{_libdir}/librados.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librados.so.2
%attr(755,root,root) %{_libdir}/librbd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librbd.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcephfs.so
%attr(755,root,root) %{_libdir}/librados.so
%attr(755,root,root) %{_libdir}/librbd.so
%{_libdir}/libcephfs.la
%{_libdir}/librados.la
%{_libdir}/librbd.la
%{_includedir}/cephfs
%{_includedir}/rados
%{_includedir}/rbd

%files static
%defattr(644,root,root,755)
%{_libdir}/libcephfs.a
%{_libdir}/librados.a
%{_libdir}/librbd.a

%files -n python-ceph
%defattr(644,root,root,755)
%{py_sitescriptdir}/rados.py[co]
%{py_sitescriptdir}/rbd.py[co]

%files fuse
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ceph-fuse
%{_mandir}/man8/ceph-fuse.8*

%files radosgw
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/radosgw
%attr(755,root,root) %{_bindir}/radosgw-admin
%{_sysconfdir}/bash_completion.d/radosgw-admin

%files obsync
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/obsync
%attr(755,root,root) %{_bindir}/boto_tool
%{_mandir}/man1/obsync.1*

%files resource-agents
%defattr(644,root,root,755)
%dir %{_prefix}/lib/ocf/resource.d/ceph
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/ceph/ceph
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/ceph/mds
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/ceph/mon
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/ceph/osd
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/ceph/rbd

%if %{with hadoop}
%files -n hadoop-cephfs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhadoopcephfs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhadoopcephfs.so.1
%attr(755,root,root) %{_libdir}/libhadoopcephfs.so
%endif
