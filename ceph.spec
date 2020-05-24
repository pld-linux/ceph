# TODO:
# - SPDK (libpciaccess dpdk/rte_config.h -lrte_eal -lrte_mempool -lrte_ring)
# - proper init scripts if non-systemd boot is too be supported
#   (upstream scripts seem overcomplicated and hardly useful)
# - run as non-root user
#
# Note on versioning: http://docs.ceph.com/docs/master/releases/
#
# Conditional build:
%bcond_without	java		# Java binding
%bcond_with	accelio		# Accelio transport support [needs update for internal API changes]
%bcond_with	kinetic		# Kinetic storage support [needs update for internal API changes]
%bcond_without	rocksdb		# RocksDB storage support
%bcond_with	zfs		# ZFS support [not ready for zfs 0.8.x]
%bcond_without	lttng		# LTTng tracing
%bcond_without	babeltrace	# Babeltrace traces support
%bcond_without	tcmalloc	# tcmalloc allocator

%ifarch x32
%undefine	with_tcmalloc
%endif
#
Summary:	User space components of the Ceph file system
Summary(pl.UTF-8):	Działające w przestrzeni użytkownika elementy systemu plików Ceph
Name:		ceph
Version:	10.2.11
Release:	1
License:	LGPL v2.1 (libraries), GPL v2 (some programs)
Group:		Base
Source0:	http://download.ceph.com/tarballs/%{name}-%{version}.tar.gz
# Source0-md5:	09d18eb8d8d06893e9496657f03427a0
Source1:	ceph.sysconfig
Source2:	cephctl
Source3:	ceph.tmpfiles
Patch0:		%{name}-init-fix.patch
Patch1:		%{name}.logrotate.patch
Patch2:		%{name}-link.patch
Patch3:		boost.patch
Patch4:		%{name}-assert.patch
Patch5:		%{name}-python.patch
URL:		https://ceph.io/
%{?with_accelio:BuildRequires:	accelio-devel}
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
%{?with_babeltrace:BuildRequires:	babeltrace-devel}
BuildRequires:	boost-devel >= 1.34
BuildRequires:	curl-devel
BuildRequires:	expat-devel >= 1.95
BuildRequires:	fcgi-devel
BuildRequires:	gdbm-devel
%if %{with java}
BuildRequires:	jdk
%endif
BuildRequires:	keyutils-devel
%{?with_kinetic:BuildRequires:	kinetic-cpp-client}
BuildRequires:	leveldb-devel >= 1.2
BuildRequires:	libaio-devel
BuildRequires:	libatomic_ops
BuildRequires:	libblkid-devel >= 2.17
BuildRequires:	libedit-devel >= 2.11
BuildRequires:	libfuse-devel
%{?with_accelio:BuildRequires:	libibverbs-devel}
BuildRequires:	libltdl-devel
%{?with_accelio:BuildRequires:	librdmacm-devel}
BuildRequires:	libstdc++-devel >= 6:4.7
%{?with_tcmalloc:BuildRequires:	libtcmalloc-devel}
BuildRequires:	libtool >= 2:1.5
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel >= 2.0
%{?with_lttng:BuildRequires:	lttng-ust-devel}
BuildRequires:	nss-devel >= 3
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	python >= 1:2.7
BuildRequires:	python-Cython
%{?with_rocksdb:BuildRequires:	rocksdb-devel}
BuildRequires:	rpmbuild(macros) >= 1.671
BuildRequires:	sed >= 4.0
BuildRequires:	snappy-devel
BuildRequires:	sphinx-pdg-2 >= 1.0
BuildRequires:	udev-devel
#BuildRequires:	virtualenv  disabled in python patch
BuildRequires:	xfsprogs-devel
%ifarch %{x8664}
BuildRequires:	yasm
%endif
%{?with_zfs:BuildRequires:	zfs-devel}
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(preun):	rc-scripts
Requires:	%{name}-libs = %{version}-%{release}
Requires:	python-%{name} = %{version}-%{release}
Requires:	systemd-units >= 38
Obsoletes:	gcephtool
Obsoletes:	hadoop-cephfs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	libceph_example.so.* libceph_snappy.so.* libceph_zlib.so.* libcls_.*.so.* libec_.*.so.*

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
Requires:	curl-devel
Requires:	expat-devel
Requires:	fcgi-devel
Requires:	nss-devel >= 3
Requires:	leveldb-devel
Requires:	libatomic_ops
Requires:	libblkid-devel >= 2.17
Requires:	libstdc++-devel >= 6:4.7
Requires:	libuuid-devel
%{?with_lttng:Requires:	lttng-ust-devel}
Requires:	openldap-devel

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
%patch2 -p1
%patch3 -p0
%patch4 -p1
%patch5 -p1

%{__sed} -i -e '1s,/usr/bin/env python$,%{__python},' \
	src/{ceph-create-keys,ceph-rest-api} \
	src/brag/client/ceph-brag \
	src/ceph-disk/ceph_disk/main.py

# adjust rule used to create ceph from ceph.in
%{__sed} -i -e 's,|/usr/bin/env python|,|%{__python}|,' src/Makefile-client.am

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
# required by xfs headers (for off64_t)
CPPFLAGS="%{rpmcppflags} -D_FILE_OFFSET_BITS=64"
# ac_cv_prog_uudecode_base64=no is a hack to compile Test.class instead of
# using included one which fails with Sun/Oracle JDK 1.6
%configure \
	%{?with_java:JAVAC=/usr/bin/javac} \
	%{?with_zfs:LIBZFS_CFLAGS="-I/usr/include/libzfs -I/usr/include/libspl"} \
	PYTHON=%{__python} \
	SPHINX_BUILD=/usr/bin/sphinx-build-2 \
	ac_cv_prog_uudecode_base64=no \
	--sbindir=/sbin \
	%{!?with_babeltrace:--without-babeltrace} \
	--without-cryptopp \
	--with-nss \
	%{!?with_tcmalloc:--without-tcmalloc} \
	%{?with_kinetic:--with-kinetic} \
	%{?with_rocksdb:--with-librocksdb} \
	--without-librocksdb-static \
	%{?with_zfs:--with-libzfs} \
	%{!?with_lttng:--without-lttng} \
	--with-ocf \
	--with-radosgw \
	--with-system-leveldb \
	--with-systemd-unit-dir=%{systemdunitdir} \
	%{?with_java:--enable-cephfs-java --with-jdk-dir=%{_jvmdir}/java} \
	--disable-silent-rules \
	%{?with_accelio:--enable-xio}

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_localstatedir}/{lib/ceph/{tmp,mon,osd,mds},log/ceph/stat,run/ceph} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{ceph,bash_completion.d,logrotate.d,rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT{%{systemdunitdir},%{systemdtmpfilesdir},/etc/systemd/system/ceph.target.wants}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	javadir=%{_javadir}

install -p src/init-ceph $RPM_BUILD_ROOT/etc/rc.d/init.d/ceph
install -p src/logrotate.conf $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/ceph

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/ceph
install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}
ln -sf /dev/null $RPM_BUILD_ROOT%{systemdunitdir}/ceph.service
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/ceph.conf

# loadable modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ceph/compressor/*.{a,la}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ceph/erasure-code/*.la
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

# actual services are to be enabled on cluster deployment
%systemd_post %{name}.target

%preun
if [ "$1" = "0" ] ; then
	%service ceph stop
	/sbin/chkconfig --del ceph
fi
%systemd_preun %{name}.target

%postun
%systemd_reload

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	-n java-cephfs -p /sbin/ldconfig
%postun	-n java-cephfs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# COPYING specifies licenses of individual parts
%doc AUTHORS COPYING README src/sample.ceph.conf src/sample.fetch_config
%attr(754,root,root) /etc/rc.d/init.d/ceph
%config(noreplace) /etc/sysconfig/ceph
%dir /etc/systemd/system/ceph.target.wants
%{systemdunitdir}/ceph.service
%{systemdunitdir}/ceph.target
%{systemdunitdir}/ceph-create-keys@.service
%{systemdunitdir}/ceph-disk@.service
%{systemdunitdir}/ceph-mds.target
%{systemdunitdir}/ceph-mds@.service
%{systemdunitdir}/ceph-mon.target
%{systemdunitdir}/ceph-mon@.service
%{systemdunitdir}/ceph-osd.target
%{systemdunitdir}/ceph-osd@.service
%{systemdunitdir}/ceph-rbd-mirror.target
%{systemdunitdir}/ceph-rbd-mirror@.service
%{systemdunitdir}/rbdmap.service
%{systemdtmpfilesdir}/ceph.conf
%dir %{_sysconfdir}/ceph
%attr(755,root,root) %{_bindir}/ceph
%attr(755,root,root) %{_bindir}/ceph-authtool
%attr(755,root,root) %{_bindir}/ceph-bluefs-tool
%attr(755,root,root) %{_bindir}/ceph-brag
%attr(755,root,root) %{_bindir}/ceph-clsinfo
%attr(755,root,root) %{_bindir}/ceph-conf
%attr(755,root,root) %{_bindir}/ceph-coverage
%attr(755,root,root) %{_bindir}/ceph-crush-location
%attr(755,root,root) %{_bindir}/ceph-debugpack
%attr(755,root,root) %{_bindir}/ceph-dencoder
%attr(755,root,root) %{_bindir}/ceph-detect-init
%attr(755,root,root) %{_bindir}/ceph-mds
%attr(755,root,root) %{_bindir}/ceph-mon
%attr(755,root,root) %{_bindir}/ceph-objectstore-tool
%attr(755,root,root) %{_bindir}/ceph-osd
%attr(755,root,root) %{_bindir}/ceph-post-file
%attr(755,root,root) %{_bindir}/ceph-rbdnamer
%attr(755,root,root) %{_bindir}/ceph-rest-api
%attr(755,root,root) %{_bindir}/ceph-run
%attr(755,root,root) %{_bindir}/ceph-syn
%attr(755,root,root) %{_bindir}/cephctl
%attr(755,root,root) %{_bindir}/cephfs
%attr(755,root,root) %{_bindir}/cephfs-data-scan
%attr(755,root,root) %{_bindir}/cephfs-journal-tool
%attr(755,root,root) %{_bindir}/cephfs-table-tool
%attr(755,root,root) %{_bindir}/crushtool
%attr(755,root,root) %{_bindir}/librados-config
%attr(755,root,root) %{_bindir}/monmaptool
%attr(755,root,root) %{_bindir}/osdmaptool
%attr(755,root,root) %{_bindir}/rados
%attr(755,root,root) %{_bindir}/rbd
%attr(755,root,root) %{_bindir}/rbd-fuse
%attr(755,root,root) %{_bindir}/rbd-mirror
%attr(755,root,root) %{_bindir}/rbd-nbd
%attr(755,root,root) %{_bindir}/rbd-replay
%attr(755,root,root) %{_bindir}/rbd-replay-many
%attr(755,root,root) %{_bindir}/rbd-replay-prep
%attr(755,root,root) %{_bindir}/rbdmap
%attr(755,root,root) %{_sbindir}/ceph-disk
%attr(755,root,root) /sbin/ceph-create-keys
%attr(755,root,root) /sbin/ceph-disk-udev
%attr(755,root,root) /sbin/mount.ceph
%attr(755,root,root) /sbin/mount.fuse.ceph
%if "%{_libexecdir}" != "%{_libdir}"
%dir %{_libexecdir}/ceph
%endif
%attr(755,root,root) %{_libexecdir}/ceph/ceph-monstore-update-crush.sh
%attr(755,root,root) %{_libexecdir}/ceph/ceph-osd-prestart.sh
%dir %{_libdir}/ceph
%{_libdir}/ceph/ceph_common.sh
%dir %{_libdir}/ceph/compressor
%attr(755,root,root) %{_libdir}/ceph/compressor/libceph_example.so*
%attr(755,root,root) %{_libdir}/ceph/compressor/libceph_snappy.so*
%attr(755,root,root) %{_libdir}/ceph/compressor/libceph_zlib.so*
%dir %{_libdir}/ceph/erasure-code
%ifarch %{x8664}
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_isa.so*
%endif
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_jerasure.so*
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_jerasure_generic.so*
%ifarch %{arm}
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_jerasure_neon.so*
%endif
%ifarch %{ix86} %{x8664} x32
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_jerasure_sse3.so*
%endif
%ifarch %{x8664} x32
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_jerasure_sse4.so*
%endif
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_lrc.so*
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_shec.so*
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_shec_generic.so*
%ifarch %{ix86} %{x8664} x32
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_shec_sse3.so*
%endif
%dir %{_libdir}/rados-classes
%attr(755,root,root) %{_libdir}/rados-classes/libcls_cephfs.so
%attr(755,root,root) %{_libdir}/rados-classes/libcls_hello.so
%attr(755,root,root) %{_libdir}/rados-classes/libcls_journal.so
%attr(755,root,root) %{_libdir}/rados-classes/libcls_kvs.so
%attr(755,root,root) %{_libdir}/rados-classes/libcls_lock.so
%attr(755,root,root) %{_libdir}/rados-classes/libcls_log.so
%attr(755,root,root) %{_libdir}/rados-classes/libcls_numops.so
%attr(755,root,root) %{_libdir}/rados-classes/libcls_rbd.so
%attr(755,root,root) %{_libdir}/rados-classes/libcls_refcount.so
%attr(755,root,root) %{_libdir}/rados-classes/libcls_replica_log.so
%attr(755,root,root) %{_libdir}/rados-classes/libcls_rgw.so
%attr(755,root,root) %{_libdir}/rados-classes/libcls_statelog.so
%attr(755,root,root) %{_libdir}/rados-classes/libcls_timeindex.so
%attr(755,root,root) %{_libdir}/rados-classes/libcls_user.so
%attr(755,root,root) %{_libdir}/rados-classes/libcls_version.so
%{_datadir}/ceph
%config(noreplace) /etc/logrotate.d/ceph
%config(noreplace) %{_sysconfdir}/bash_completion.d/rados
%config(noreplace) %{_sysconfdir}/bash_completion.d/ceph
%config(noreplace) %{_sysconfdir}/bash_completion.d/rbd
%{_mandir}/man8/ceph.8*
%{_mandir}/man8/ceph-authtool.8*
%{_mandir}/man8/ceph-clsinfo.8*
%{_mandir}/man8/ceph-conf.8*
%{_mandir}/man8/ceph-create-keys.8*
%{_mandir}/man8/ceph-debugpack.8*
%{_mandir}/man8/ceph-dencoder.8*
%{_mandir}/man8/ceph-deploy.8*
%{_mandir}/man8/ceph-detect-init.8*
%{_mandir}/man8/ceph-disk.8*
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
%{_mandir}/man8/monmaptool.8*
%{_mandir}/man8/mount.ceph.8*
%{_mandir}/man8/osdmaptool.8*
%{_mandir}/man8/rados.8*
%{_mandir}/man8/radosgw.8*
%{_mandir}/man8/radosgw-admin.8*
%{_mandir}/man8/rbd.8*
%{_mandir}/man8/rbd-fuse.8*
%{_mandir}/man8/rbd-mirror.8*
%{_mandir}/man8/rbd-nbd.8*
%{_mandir}/man8/rbd-replay.8*
%{_mandir}/man8/rbd-replay-many.8*
%{_mandir}/man8/rbd-replay-prep.8*
%{_mandir}/man8/rbdmap.8*

%dir %{_localstatedir}/lib/ceph
%dir %{_localstatedir}/lib/ceph/mds
%dir %{_localstatedir}/lib/ceph/mon
%dir %{_localstatedir}/lib/ceph/osd
%dir %{_localstatedir}/lib/ceph/tmp
%dir %{_localstatedir}/log/ceph
%dir %{_localstatedir}/run/ceph

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcephfs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcephfs.so.1
%attr(755,root,root) %{_libdir}/libos_tp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libos_tp.so.1
%attr(755,root,root) %{_libdir}/libosd_tp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libosd_tp.so.1
%attr(755,root,root) %{_libdir}/librados.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librados.so.2
%attr(755,root,root) %{_libdir}/librados_tp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librados_tp.so.2
%attr(755,root,root) %{_libdir}/libradosstriper.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libradosstriper.so.1
%attr(755,root,root) %{_libdir}/librbd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librbd.so.1
%attr(755,root,root) %{_libdir}/librbd_tp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librbd_tp.so.1
%attr(755,root,root) %{_libdir}/librgw.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librgw.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcephfs.so
%attr(755,root,root) %{_libdir}/libos_tp.so
%attr(755,root,root) %{_libdir}/libosd_tp.so
%attr(755,root,root) %{_libdir}/librados.so
%attr(755,root,root) %{_libdir}/librados_tp.so
%attr(755,root,root) %{_libdir}/libradosstriper.so
%attr(755,root,root) %{_libdir}/librbd.so
%attr(755,root,root) %{_libdir}/librbd_tp.so
%attr(755,root,root) %{_libdir}/librgw.so
%{_libdir}/libcephfs.la
%{_libdir}/libos_tp.la
%{_libdir}/libosd_tp.la
%{_libdir}/librados.la
%{_libdir}/librados_tp.la
%{_libdir}/libradosstriper.la
%{_libdir}/librbd.la
%{_libdir}/librbd_tp.la
%{_libdir}/librgw.la
%{_includedir}/cephfs
%{_includedir}/rados
%{_includedir}/radosstriper
%{_includedir}/rbd

%files static
%defattr(644,root,root,755)
%{_libdir}/libcephfs.a
%{_libdir}/libos_tp.a
%{_libdir}/libosd_tp.a
%{_libdir}/librados.a
%{_libdir}/librados_tp.a
%{_libdir}/libradosstriper.a
%{_libdir}/librbd.a
%{_libdir}/librbd_tp.a
%{_libdir}/librgw.a

%files -n python-ceph
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/cephfs.so
%attr(755,root,root) %{py_sitedir}/rados.so
%attr(755,root,root) %{py_sitedir}/rbd.so
%{py_sitedir}/ceph_detect_init
%{py_sitedir}/ceph_disk
%{py_sitedir}/ceph_detect_init-1.0.1-py*.egg-info
%{py_sitedir}/ceph_disk-1.0.0-py*.egg-info
%{py_sitedir}/cephfs-0-py*.egg-info
%{py_sitedir}/rados-0-py*.egg-info
%{py_sitedir}/rbd-0-py*.egg-info
%{py_sitescriptdir}/ceph_argparse.py[co]
%{py_sitescriptdir}/ceph_daemon.py[co]
%{py_sitescriptdir}/ceph_rest_api.py[co]
%{py_sitescriptdir}/ceph_volume_client.py[co]

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
%attr(755,root,root) %{_bindir}/radosgw-object-expirer
%attr(755,root,root) %{_bindir}/radosgw-token
%{systemdunitdir}/ceph-radosgw.target
%{systemdunitdir}/ceph-radosgw@.service
%{_sysconfdir}/bash_completion.d/radosgw-admin

%files resource-agents
%defattr(644,root,root,755)
%dir %{_prefix}/lib/ocf/resource.d/ceph
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/ceph/rbd
