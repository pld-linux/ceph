#
# Conditional build:
%bcond_without	java	# Java binding
%bcond_with	zfs	# ZFS support [needs zfs.pc, not provided yet(?)]
#
Summary:	User space components of the Ceph file system
Summary(pl.UTF-8):	Działające w przestrzeni użytkownika elementy systemu plików Ceph
Name:		ceph
Version:	0.76
Release:	1
License:	LGPL v2.1 (libraries), GPL v2 (some programs)
Group:		Base
Source0:	http://ceph.com/download/%{name}-%{version}.tar.bz2
# Source0-md5:	7a7b82f711f8fac716284aa8c5e53b75
Patch0:		%{name}-init-fix.patch
Patch1:		%{name}.logrotate.patch
URL:		http://ceph.com/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	boost-devel >= 1.34
BuildRequires:	cryptopp-devel
BuildRequires:	curl-devel
BuildRequires:	expat-devel >= 1.95
BuildRequires:	fcgi-devel
BuildRequires:	gdbm-devel
%if %{with java}
BuildRequires:	jdk
%endif
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
BuildRequires:	snappy-devel
%ifarch %{x8664}
BuildRequires:	yasm
%endif
%{?with_zfs:BuildRequires:	zfs-devel}
Requires(post,preun):	/sbin/chkconfig
Requires(preun):	rc-scripts
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	gcephtool
Obsoletes:	hadoop-cephfs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	libcls_.*.so.* libec_.*.so.*

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
License:	LGPL v2.1
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	boost-devel >= 1.34
Requires:	cryptopp-devel
Requires:	leveldb-devel
Requires:	libatomic_ops
Requires:	libuuid-devel

%description devel
This package contains the headers needed to develop programs that use
Ceph.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia programów
wykorzystujących Cepha.

%package static
Summary:	Ceph static libraries
Summary(pl.UTF-8):	Biblioteki statyczne Cepha
License:	LGPL v2.1
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

%package -n java-cephfs
Summary:	CephFS Java bindings
Summary(pl.UTF-8):	Wiązania Javy do biblioteki CephFS
Group:		Libraries/Java
Requires:	%{name}-libs = %{version}-%{release}

%description -n java-cephfs
CephFS Java bindings.

%description -n java-cephfs -l pl.UTF-8
Wiązania Javy do biblioteki CephFS.

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

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
# ac_cv_prog_uudecode_base64=no is a hack to compile Test.class instead of
# using included one which fails with Sun/Oracle JDK 1.6
%configure \
	%{?with_java:JAVAC=/usr/bin/javac} \
	ac_cv_prog_uudecode_base64=no \
	--sbindir=/sbin \
	--with-cryptopp \
	%{?with_zfs:--with-libzfs} \
	--with-ocf \
	--with-radosgw \
	--with-system-leveldb \
	--with-system-libs3 \
	%{?with_java:--enable-cephfs-java --with-jdk-dir=%{_jvmdir}/java} \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_localstatedir}/{lib/ceph/tmp,log/ceph/stat} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{ceph,bash_completion.d,logrotate.d,rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	javadir=%{_javadir}

install -p src/init-ceph $RPM_BUILD_ROOT/etc/rc.d/init.d/ceph
install -p src/logrotate.conf $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/ceph

# loadable modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ceph/erasure-code/*.{a,la}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/rados-classes/*.la
%if %{with java}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcephfs_jni.{la,a}
%endif

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/ceph/sample.{ceph.conf,fetch_config}

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

%post	-n java-cephfs -p /sbin/ldconfig
%postun	-n java-cephfs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# COPYING specifies licenses of individual parts
%doc AUTHORS COPYING README src/sample.ceph.conf src/sample.fetch_config
%attr(754,root,root) /etc/rc.d/init.d/ceph
%dir %{_sysconfdir}/ceph
%attr(755,root,root) %{_bindir}/ceph
%attr(755,root,root) %{_bindir}/ceph-authtool
%attr(755,root,root) %{_bindir}/ceph-clsinfo
%attr(755,root,root) %{_bindir}/ceph-conf
%attr(755,root,root) %{_bindir}/ceph-coverage
%attr(755,root,root) %{_bindir}/ceph-crush-location
%attr(755,root,root) %{_bindir}/ceph-debugpack
%attr(755,root,root) %{_bindir}/ceph-dencoder
%attr(755,root,root) %{_bindir}/ceph-mds
%attr(755,root,root) %{_bindir}/ceph-mon
%attr(755,root,root) %{_bindir}/ceph-osd
%attr(755,root,root) %{_bindir}/ceph-post-file
%attr(755,root,root) %{_bindir}/ceph-rbdnamer
%attr(755,root,root) %{_bindir}/ceph-rest-api
%attr(755,root,root) %{_bindir}/ceph-run
%attr(755,root,root) %{_bindir}/ceph-syn
%attr(755,root,root) %{_bindir}/ceph_filestore_dump
%attr(755,root,root) %{_bindir}/ceph_filestore_tool
%attr(755,root,root) %{_bindir}/ceph_mon_store_converter
%attr(755,root,root) %{_bindir}/cephfs
%attr(755,root,root) %{_bindir}/crushtool
%attr(755,root,root) %{_bindir}/librados-config
%attr(755,root,root) %{_bindir}/monmaptool
%attr(755,root,root) %{_bindir}/osdmaptool
%attr(755,root,root) %{_bindir}/rados
%attr(755,root,root) %{_bindir}/rbd
%attr(755,root,root) %{_bindir}/rbd-fuse
%attr(755,root,root) /sbin/ceph-create-keys
%attr(755,root,root) /sbin/ceph-disk
%attr(755,root,root) /sbin/ceph-disk-activate
%attr(755,root,root) /sbin/ceph-disk-prepare
%attr(755,root,root) /sbin/ceph-disk-udev
%attr(755,root,root) /sbin/mkcephfs
%attr(755,root,root) /sbin/mount.ceph
%attr(755,root,root) /sbin/mount.fuse.ceph
%dir %{_libdir}/ceph
%{_libdir}/ceph/ceph_common.sh
%dir %{_libdir}/ceph/erasure-code
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_example.so*
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_fail_to_initialize.so*
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_fail_to_register.so*
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_hangs.so*
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_jerasure.so*
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_missing_entry_point.so*
%dir %{_libdir}/rados-classes
%attr(755,root,root) %{_libdir}/rados-classes/libcls_hello.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_kvs.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_lock.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_log.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_rbd.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_refcount.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_replica_log.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_rgw.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_statelog.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_version.so*
%{_datadir}/ceph
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
%{_mandir}/man8/ceph-post-file.8*
%{_mandir}/man8/ceph-rbdnamer.8*
%{_mandir}/man8/ceph-rest-api.8*
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
%{_mandir}/man8/rbd-fuse.8*

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
%{py_sitescriptdir}/ceph_argparse.py[co]
%{py_sitescriptdir}/ceph_rest_api.py[co]
%{py_sitescriptdir}/cephfs.py[co]
%{py_sitescriptdir}/rados.py[co]
%{py_sitescriptdir}/rbd.py[co]

%if %{with java}
%files -n java-cephfs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcephfs_jni.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcephfs_jni.so.1
%attr(755,root,root) %{_libdir}/libcephfs_jni.so
%{_javadir}/libcephfs.jar
%endif

%files fuse
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ceph-fuse
%{_mandir}/man8/ceph-fuse.8*

%files radosgw
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/radosgw
%attr(755,root,root) %{_bindir}/radosgw-admin
%{_sysconfdir}/bash_completion.d/radosgw-admin

%files resource-agents
%defattr(644,root,root,755)
%dir %{_prefix}/lib/ocf/resource.d/ceph
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/ceph/ceph
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/ceph/mds
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/ceph/mon
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/ceph/osd
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/ceph/rbd
