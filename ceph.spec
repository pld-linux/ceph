# TODO:
# - thrift 0.13+ for jaeger
# - Could NOT find dml (missing: DML_LIBRARIES DML_INCLUDE_DIR DML_HL_LIBRARIES)
# - system arrow, parquet (WITH_SYSTEM_ARROW=ON, arrow>=4, parquet>=4)?
# - brotli? (WITH_BROTLI=ON, uses internal brotli as downloaded subproject)
# - proper init scripts if non-systemd boot is to be supported
#   (upstream scripts seem overcomplicated and hardly useful)
# - run as non-root user
# - build selinux policy (-DWITH_SELINUX=ON)
# - package sphinx docs (from doc/)
#
# Note on versioning: http://docs.ceph.com/docs/master/releases/
# Reef (18.1.2) is in RC stage currently
#
# Conditional build:
%bcond_without	java		# Java binding
%bcond_with	angular		# Angular-based mgr/dashboard frontend (built using npm, too outdated currently)
%bcond_without	bluefs		# BlueFS library
%bcond_with	dpdk		# DPDK messaging
%bcond_with	fio		# FIO engines support (16.x: downloads fio as internal subproject)
%bcond_with	jaeger		# jaegertracing support (NFY, BR: thrift >= 0.13)
%bcond_with	kerberos	# GSSAPI/KRB5 support
%bcond_without	pmem		# PMDK (persistent memory) support
%bcond_without	qat		# QAT driver
%bcond_without	qatzip		# QATZIP
%bcond_without	rdma		# RDMA transport support
%bcond_with	seastar		# seastar components (64-bit pointers required)
%bcond_with	spdk		# Ceph SPDK support (DPDK based)
%bcond_without	system_rocksdb	# system RocksDB storage support
%bcond_without	zbd		# ZBD bluestore backend
# 15.2.x/16.2.x: "fallthrough" define from OpenZFS's spl breaks "[[fallthrough]]" in src/include/blobhash.h
%bcond_with	zfs		# ZFS support [not ready for zfs 0.8.x]
%bcond_without	lttng		# LTTng tracing
%bcond_without	babeltrace	# Babeltrace traces support
%bcond_without	tcmalloc	# tcmalloc allocator
%bcond_with	tests		# build tests

%ifarch x32
%undefine	with_tcmalloc
%endif
%ifnarch %{x8664}
%undefine	with_qat
%undefine	with_qatzip
%endif
%ifnarch %{x8664} aarch64
%undefine	with_pmem
%endif
%ifnarch %{x8664} aarch64 mips64 ppc64 sparc64 s390x
%undefine	with_seastar
%endif

%{?with_java:%{?use_default_jdk}}
#
Summary:	User space components of the Ceph file system
Summary(pl.UTF-8):	Działające w przestrzeni użytkownika elementy systemu plików Ceph
Name:		ceph
Version:	19.2.0
Release:	1
License:	LGPL v2.1 (libraries), GPL v2 (some programs)
Group:		Base
Source0:	http://download.ceph.com/tarballs/%{name}-%{version}.tar.gz
# Source0-md5:	876d7144df5c7061ddbd5bc5c3709a35
Source1:	%{name}.sysconfig
Source3:	%{name}.tmpfiles
Patch0:		%{name}-python.patch
Patch1:		%{name}-fio.patch
Patch2:		%{name}-cmake-static.patch
Patch3:		%{name}-arrow-pld.patch
Patch4:		no-virtualenvs.patch
Patch5:		%{name}-libdir.patch
Patch6:		types.patch
Patch7:		use-provided-cpu-flag-values.patch
Patch8:		ix86-no-asm.patch
Patch9:		long-int-time_t.patch
Patch10:	%{name}-system-rocksdb.patch
# https://src.fedoraproject.org/rpms/ceph/blob/rawhide/f/0020-src-arrow-cpp-cmake_modules-ThirdpartyToolchain.cmake.patch
Patch11:	%{name}-system-xsimd.patch
Patch12:	%{name}-gcc14.patch
Patch13:	boost-1.86.patch
Patch14:	boost-1.87.patch
Patch15:	x32.patch
URL:		https://ceph.io/
%{?with_qatzip:BuildRequires:	QATzip-devel}
%{?with_babeltrace:BuildRequires:	babeltrace-devel}
BuildRequires:	boost-devel >= 1.79
BuildRequires:	boost-python3-devel >= 1.79
%{?with_seastar:BuildRequires:	c-ares-devel >= 1.13.0}
BuildRequires:	cmake >= 3.22.2
%{?with_seastar:BuildRequires:	cryptopp-devel >= 5.6.5}
BuildRequires:	cryptsetup-devel >= 2.0.5
BuildRequires:	curl-devel >= 7.32
%if %{with dpdk} || %{with spdk}
# also seastar with dpdk support
BuildRequires:	dpdk-devel
%endif
BuildRequires:	doxygen
BuildRequires:	expat-devel >= 1.95
%{?with_fio:BuildRequires:	fio-devel >= 3.15}
BuildRequires:	gdbm-devel
%{?with_seastar:BuildRequires:	gnutls-devel >= 3.3.26}
BuildRequires:	gperf
%{?with_tcmalloc:BuildRequires:	gperftools-devel >= 2.6.2}
%{?with_kerberos:BuildRequires:	heimdal-devel}
%{?with_seastar:BuildRequires:	hwloc-devel >= 1.11.2}
%if %{with java}
%buildrequires_jdk
BuildRequires:	%{?use_jdk:%{use_jdk}-jre-base-X11}%{!?use_jdk:jre-X11}
%endif
BuildRequires:	keyutils-devel
BuildRequires:	leveldb-devel >= 1.23-2
BuildRequires:	libaio-devel
BuildRequires:	libatomic_ops
BuildRequires:	libblkid-devel >= 2.17
BuildRequires:	libcap-ng-devel
BuildRequires:	libedit-devel >= 2.11
BuildRequires:	libfmt-devel >= 6.0.0
BuildRequires:	libfuse3-devel >= 3
%{?with_rdma:BuildRequires:	libibverbs-devel}
BuildRequires:	libicu-devel >= 52.0
BuildRequires:	libltdl-devel
BuildRequires:	libnl-devel >= 3.2
BuildRequires:	librdkafka-devel >= 0.9.2
%{?with_rdma:BuildRequires:	librdmacm-devel}
%{?with_seastar:BuildRequires:	libsctp-devel}
BuildRequires:	libstdc++-devel >= 6:11
%{?with_tcmalloc:BuildRequires:	libtcmalloc-devel >= 2.6.2}
BuildRequires:	libtool >= 2:1.5
BuildRequires:	liburing-devel
BuildRequires:	libutf8proc-devel >= 2.2.0
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel >= 2.0
%{?with_zbd:BuildRequires:	libzbd-devel}
BuildRequires:	lmdb-devel
%{?with_lttng:BuildRequires:	lttng-ust-devel}
BuildRequires:	lua-devel >= 5.3
BuildRequires:	lz4-devel >= 1:1.7.3
BuildRequires:	ncurses-devel
%{?with_angular:BuildRequires:	npm}
BuildRequires:	nspr-devel >= 4
BuildRequires:	nss-devel >= 3
%{?with_seastar:BuildRequires:	numactl-devel}
BuildRequires:	oath-toolkit-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel >= 1.1
BuildRequires:	perl-base
BuildRequires:	pkgconfig
%{?with_pmem:BuildRequires:	pmdk-devel >= 1.10.0}
BuildRequires:	python3 >= 1:3.6.0
BuildRequires:	python3-Cython
BuildRequires:	python3-PyYAML
BuildRequires:	python3-devel >= 1:3.6.0
BuildRequires:	python3-jinja2 >= 3.1.2
BuildRequires:	python3-markupsafe >= 2.1.3
BuildRequires:	python3-modules >= 1:3.6.0
%{?with_tests:BuildRequires:	python3-tox >= 2.9.1}
%{?with_qat:BuildRequires:	qatlib-devel}
BuildRequires:	rabbitmq-c-devel
%{?with_seastar:BuildRequires:	ragel >= 6.10}
BuildRequires:	re2-devel
%{?with_system_rocksdb:BuildRequires:	rocksdb-devel >= 5.14}
BuildRequires:	rpmbuild(macros) >= 2.021
BuildRequires:	sed >= 4.0
BuildRequires:	snappy-devel
BuildRequires:	sphinx-pdg >= 4.4.0
BuildRequires:	sqlite3-devel >= 3
# >= 0.13.0 wanted, but seems to build with 0.11.0 when jaeger is disabled
BuildRequires:	thrift-devel
BuildRequires:	udev-devel
BuildRequires:	xfsprogs-devel
%{?with_dpdk:BuildRequires:	xorg-lib-libpciaccess-devel}
BuildRequires:	xsimd-devel
%{?with_seastar:BuildRequires:	yaml-cpp-devel >= 0.5.1}
%ifarch %{x8664}
BuildRequires:	yasm
%endif
%{?with_zfs:BuildRequires:	zfs-devel >= 0.8.0}
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel >= 1.4.4
Requires(post,preun):	/sbin/chkconfig
Requires(preun):	rc-scripts
Requires:	%{name}-libs = %{version}-%{release}
Requires:	lz4 >= 1:1.7.3
Requires:	python3-%{name} = %{version}-%{release}
%{?with_system_rocksdb:Requires:	rocksdb >= 5.14}
Requires:	systemd-units >= 38
Requires:	zstd >= 1.4.4
Obsoletes:	gcephtool < 0.51
Obsoletes:	hadoop-cephfs < 0.71
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	libceph_crypto_isal.so.* libceph_crypto_qat.so.* libceph_lz4.so.* libceph_snappy.so.* libceph_zlib.so.* libceph_zstd.so.* libcls_.*.so.* libec_.*.so.*

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
Requires:	libfmt >= 6.0.0
Requires:	librdkafka >= 0.9.2
Requires:	openssl >= 1.1

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
Requires:	boost-devel >= 1.79
Requires:	curl-devel >= 7.32
Requires:	expat-devel >= 1.95
Requires:	leveldb-devel >= 1.23-2
Requires:	libatomic_ops
Requires:	libblkid-devel >= 2.17
Requires:	libstdc++-devel >= 6:11
Requires:	libuuid-devel
%{?with_lttng:Requires: lttng-ust-devel}
Requires:	nss-devel >= 3
Requires:	openldap-devel
Obsoletes:	ceph-static < 12

%description devel
This package contains the headers needed to develop programs that use
Ceph.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia programów
wykorzystujących Cepha.

%package -n python3-ceph
Summary:	Ceph Python 3 bindings
Summary(pl.UTF-8):	Wiązania Pythona 3 do bibliotek Cepha
Group:		Development/Languages/Python
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	python-ceph < 15

%description -n python3-ceph
Ceph Python 3 bindings.

%description -n python3-ceph -l pl.UTF-8
Wiązania Pythona 3 do bibliotek Cepha.

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

%package test
Summary:	Ceph benchmarks and test tools
Summary(pl.UTF-8):	Narzędzia testowe oraz do mierzenia wydajności dla Ceph
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description test
Ceph benchmarks and test tools.

%description test -l pl.UTF-8
Narzędzia testowe oraz do mierzenia wydajności dla Ceph.

%package -n fio-ceph-objectstore
Summary:	FIO engine module for Ceph ObjectStore
Summary(pl.UTF-8):	Moduł silnika FIO do używania Ceph ObjectStore
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
%if %{with fio}
%requires_ge_to	fio fio-devel
%endif

%description -n fio-ceph-objectstore
This FIO engine allows you to mount and use a ceph object store
directly, without having to build a ceph cluster or start any daemons.

%description -n fio-ceph-objectstore -l pl.UTF-8
Ten silnik FIO pozwala na bezpośrednie montowanie i używanie
przestrzeni obiektów ceph, bez potrzeby budowania klastra ceph czy
uruchamiania demonów.

%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1
%patch -P 4 -p1
%patch -P 5 -p1
%patch -P 6 -p1
%patch -P 7 -p1
%patch -P 8 -p1
%ifarch %{ix86}
%patch -P 9 -p1
%endif
%patch -P 10 -p1
%patch -P 11 -p1
%patch -P 12 -p1
%patch -P 13 -p1
%patch -P 14 -p1
%patch -P 15 -p1

%{__sed} -i -e '1s,/usr/bin/env bash,/bin/bash,' \
	src/{ceph-post-file.in,rbd-replay-many,rbdmap} \
	src/rgw/{rgw-gap-list,rgw-orphan-list,rgw-restore-bucket-index}

%{__sed} -i -e '1s,/usr/bin/awk,/bin/awk,' \
	src/rgw/rgw-gap-list-comparator

%if %{with angular}
# stub virtualenv with npm for src/pybind/mgr/dashboard bootstrapping
install -d build/src/pybind/mgr/dashboard/node-env/bin
ln -sf /usr/bin/npm build/src/pybind/mgr/dashboard/node-env/bin/npm
cat >build/src/pybind/mgr/dashboard/node-env/bin/activate <<EOF
deactivate() {
    unset -f deactivate
}
EOF
%endif

%build
install -d build
cd build
%cmake .. \
%ifarch %{x8664} %{ix86} x32
	-DHAVE_INTEL_SSE=1 \
%endif
%ifarch %{x8664} x32
	-DHAVE_INTEL_SSE2=1 \
	-DHAVE_INTEL_SSE3=1 \
	-DHAVE_INTEL_SSSE3=1 \
	-DHAVE_INTEL_PCLMUL=1 \
	-DHAVE_INTEL_SSE4_1=1 \
	-DHAVE_INTEL_SSE4_2=1 \
%endif
	-DALLOCATOR="%{?with_tcmalloc:tcmalloc}%{!?with_tcmalloc:libc}" \
	-DFIO_INCLUDE_DIR=/usr/include/fio \
	%{cmake_on_off java JAVA_HOME:PATH} \
	-DLUA_INCLUDE_DIR=%{_includedir}/lua \
	-DPYTHON=%{__python3} \
	-DSPHINX_BUILD=/usr/bin/sphinx-build \
%if %{with pmem}
	-DWITH_BLUESTORE_PMEM=ON \
	-DWITH_SYSTEM_PMDK:BOOL=ON \
%endif
	-DWITH_LZ4=ON \
	-DWITH_OCF=ON \
	-DWITH_PYTHON3=%{py3_ver} \
	-DWITH_RADOSGW_SELECT_PARQUET=OFF \
	-DWITH_RADOSGW_ARROW_FLIGHT=OFF \
	-DWITH_REENTRANT_STRSIGNAL=ON \
	-DWITH_SYSTEM_BOOST=ON \
	-DWITH_SYSTEM_LIBURING=ON \
	-DWITH_SYSTEM_ZSTD=ON \
	-DWITH_SYSTEMD=ON \
	%{cmake_on_off babeltrace WITH_BABELTRACE} \
	%{cmake_on_off bluefs WITH_BLUEFS} \
	%{cmake_on_off java WITH_CEPHFS_JAVA} \
	%{cmake_on_off dpdk WITH_DPDK} \
	%{cmake_on_off fio WITH_FIO} \
	%{cmake_on_off kerberos WITH_GSSAPI} \
	%{cmake_on_off jaeger WITH_JAEGER} \
	%{cmake_on_off lttng WITH_LTTNG} \
	%{cmake_on_off angular WITH_MGR_DASHBOARD_FRONTEND} \
	%{cmake_on_off rdma WITH_RDMA} \
	%{cmake_on_off qat WITH_QATLIB} \
	%{cmake_on_off qatzip WITH_QATZIP} \
	%{cmake_on_off seastar WITH_SEASTAR} \
	%{cmake_on_off spdk WITH_SPDK} \
	%{cmake_on_off angular WITH_SYSTEM_NPM} \
	%{cmake_on_off system_rocksdb WITH_SYSTEM_ROCKSDB} \
	%{cmake_on_off tests WITH_TESTS} \
	%{cmake_on_off zbd WITH_ZBD} \
	%{cmake_on_off zfs WITH_ZFS}

# some object files have missing dependencies on these, pregenerate to avoid global -j1
%{__make} legacy-option-headers

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_localstatedir}/{lib/ceph/{tmp,mon,osd,mds,mgr,radosgw,bootstrap-{osd,mds,rgw,mgr,rbd}},log/ceph/stat,run/ceph} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{ceph,bash_completion.d,logrotate.d,rc.d,sysconfig} \
	$RPM_BUILD_ROOT{%{systemdunitdir},%{systemdtmpfilesdir},/etc/systemd/system/ceph.target.wants,/sbin}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# sanitize paths; no config options for cmake
%{__mv} $RPM_BUILD_ROOT/etc/init.d $RPM_BUILD_ROOT/etc/rc.d
%{__mv} $RPM_BUILD_ROOT%{_sbindir}/mount.* $RPM_BUILD_ROOT/sbin

cp -p src/logrotate.conf $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/ceph

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/ceph
ln -sf /dev/null $RPM_BUILD_ROOT%{systemdunitdir}/ceph.service
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/ceph.conf

%if %{without tests}
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/{ceph,ceph_volume}/tests
%endif

%py3_comp $RPM_BUILD_ROOT%{py3_sitescriptdir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitescriptdir}

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/sample.ceph.conf

%if %{with angular}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ceph/mgr/dashboard/HACKING.rst
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ceph/mgr/{.gitignore,dashboard/static/AdminLTE-2.3.7/{.gitignore,.jshintrc,README.md}}
%endif

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
%doc AUTHORS COPYING PendingReleaseNotes README.md src/sample.ceph.conf doc/releases
%attr(754,root,root) /etc/rc.d/init.d/ceph
%config(noreplace) /etc/sysconfig/ceph
%dir /etc/systemd/system/ceph.target.wants
%{systemdunitdir}/ceph.service
%{systemdunitdir}/ceph.target
%{systemdunitdir}/ceph-crash.service
%{systemdunitdir}/ceph-fuse.target
%{systemdunitdir}/ceph-fuse@.service
%{systemdunitdir}/ceph-immutable-object-cache.target
%{systemdunitdir}/ceph-immutable-object-cache@.service
%{systemdunitdir}/ceph-mds.target
%{systemdunitdir}/ceph-mds@.service
%{systemdunitdir}/ceph-mgr.target
%{systemdunitdir}/ceph-mgr@.service
%{systemdunitdir}/ceph-mon.target
%{systemdunitdir}/ceph-mon@.service
%{systemdunitdir}/ceph-osd.target
%{systemdunitdir}/ceph-osd@.service
%{systemdunitdir}/ceph-rbd-mirror.target
%{systemdunitdir}/ceph-rbd-mirror@.service
%{systemdunitdir}/ceph-volume@.service
%{systemdunitdir}/cephfs-mirror.target
%{systemdunitdir}/cephfs-mirror@.service
%{systemdunitdir}/rbdmap.service
%{systemdtmpfilesdir}/ceph.conf
%dir %{_sysconfdir}/ceph
%attr(755,root,root) %{_bindir}/ceph
%attr(755,root,root) %{_bindir}/ceph-authtool
%attr(755,root,root) %{_bindir}/ceph-bluestore-tool
%attr(755,root,root) %{_bindir}/ceph-clsinfo
%attr(755,root,root) %{_bindir}/ceph-conf
%attr(755,root,root) %{_bindir}/ceph-crash
%attr(755,root,root) %{_bindir}/ceph-dencoder
%attr(755,root,root) %{_bindir}/ceph-diff-sorted
%attr(755,root,root) %{_bindir}/ceph-erasure-code-tool
%attr(755,root,root) %{_bindir}/ceph-exporter
%attr(755,root,root) %{_bindir}/ceph-immutable-object-cache
%attr(755,root,root) %{_bindir}/ceph-kvstore-tool
%attr(755,root,root) %{_bindir}/ceph-mds
%attr(755,root,root) %{_bindir}/ceph-mgr
%attr(755,root,root) %{_bindir}/ceph-mon
%attr(755,root,root) %{_bindir}/ceph-monstore-tool
%attr(755,root,root) %{_bindir}/ceph-objectstore-tool
%attr(755,root,root) %{_bindir}/ceph-osd
%attr(755,root,root) %{_bindir}/ceph-osdomap-tool
%attr(755,root,root) %{_bindir}/ceph-post-file
%attr(755,root,root) %{_bindir}/ceph-rbdnamer
%attr(755,root,root) %{_bindir}/ceph-run
%attr(755,root,root) %{_bindir}/ceph-syn
%attr(755,root,root) %{_bindir}/cephfs-data-scan
%attr(755,root,root) %{_bindir}/cephfs-journal-tool
%attr(755,root,root) %{_bindir}/cephfs-mirror
%attr(755,root,root) %{_bindir}/cephfs-table-tool
%attr(755,root,root) %{_bindir}/cephfs-top
%if %{with seastore}
%attr(755,root,root) %{_bindir}/crimson-osd
%attr(755,root,root) %{_bindir}/crimson-store-nbd
%endif
%attr(755,root,root) %{_bindir}/crushdiff
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
%attr(755,root,root) %{_bindir}/rgw-gap-list
%attr(755,root,root) %{_bindir}/rgw-gap-list-comparator
%attr(755,root,root) %{_bindir}/rgw-orphan-list
%attr(755,root,root) %{_bindir}/rgw-restore-bucket-index
%attr(755,root,root) %{_sbindir}/cephadm
%attr(755,root,root) %{_sbindir}/ceph-create-keys
%attr(755,root,root) %{_sbindir}/ceph-node-proxy
%attr(755,root,root) %{_sbindir}/ceph-volume
%attr(755,root,root) %{_sbindir}/ceph-volume-systemd
%attr(755,root,root) /sbin/mount.ceph
%attr(755,root,root) /sbin/mount.fuse.ceph
%if "%{_libexecdir}" != "%{_libdir}"
%dir %{_libexecdir}/ceph
%endif
%{_libexecdir}/ceph/ceph_common.sh
%attr(755,root,root) %{_libexecdir}/ceph/ceph-osd-prestart.sh
%dir %{_libdir}/ceph/compressor
%attr(755,root,root) %{_libdir}/ceph/compressor/libceph_lz4.so*
%attr(755,root,root) %{_libdir}/ceph/compressor/libceph_snappy.so*
%attr(755,root,root) %{_libdir}/ceph/compressor/libceph_zlib.so*
%attr(755,root,root) %{_libdir}/ceph/compressor/libceph_zstd.so*
%dir %{_libdir}/ceph/crypto
%ifarch %{x8664}
%attr(755,root,root) %{_libdir}/ceph/crypto/libceph_crypto_isal.so*
%endif
%attr(755,root,root) %{_libdir}/ceph/crypto/libceph_crypto_openssl.so*
%if %{with qat}
%attr(755,root,root) %{_libdir}/ceph/crypto/libceph_crypto_qat.so*
%endif
%dir %{_libdir}/ceph/denc
%attr(755,root,root) %{_libdir}/ceph/denc/denc-mod-cephfs.so
%attr(755,root,root) %{_libdir}/ceph/denc/denc-mod-common.so
%attr(755,root,root) %{_libdir}/ceph/denc/denc-mod-osd.so
%attr(755,root,root) %{_libdir}/ceph/denc/denc-mod-rbd.so
%attr(755,root,root) %{_libdir}/ceph/denc/denc-mod-rgw.so
%dir %{_libdir}/ceph/erasure-code
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_clay.so*
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
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_jerasure_sse4.so*
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_shec_sse3.so*
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_shec_sse4.so*
%endif
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_lrc.so*
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_shec.so*
%attr(755,root,root) %{_libdir}/ceph/erasure-code/libec_shec_generic.so*
%dir %{_libdir}/ceph/extblkdev
%attr(755,root,root) %{_libdir}/ceph/extblkdev/libceph_ebd_vdo.so*
%dir %{_libdir}/ceph/librbd
%attr(755,root,root) %{_libdir}/ceph/librbd/libceph_librbd_parent_cache.so*
%dir %{_libdir}/rados-classes
%attr(755,root,root) %{_libdir}/rados-classes/libcls_2pc_queue.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_cas.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_cephfs.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_cmpomap.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_fifo.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_hello.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_journal.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_lock.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_log.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_lua.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_numops.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_otp.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_queue.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_rbd.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_refcount.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_rgw.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_rgw_gc.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_sdk.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_test_remote_reads.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_timeindex.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_user.so*
%attr(755,root,root) %{_libdir}/rados-classes/libcls_version.so*
%{_datadir}/ceph
%config(noreplace) /etc/logrotate.d/ceph
%config(noreplace) %{_sysconfdir}/bash_completion.d/rados
%config(noreplace) %{_sysconfdir}/bash_completion.d/ceph
%config(noreplace) %{_sysconfdir}/bash_completion.d/rbd
%{_mandir}/man8/ceph.8*
%{_mandir}/man8/ceph-authtool.8*
%{_mandir}/man8/ceph-bluestore-tool.8*
%{_mandir}/man8/ceph-clsinfo.8*
%{_mandir}/man8/ceph-conf.8*
%{_mandir}/man8/ceph-create-keys.8*
%{_mandir}/man8/ceph-dencoder.8*
%{_mandir}/man8/ceph-diff-sorted.8*
%{_mandir}/man8/ceph-immutable-object-cache.8*
%{_mandir}/man8/ceph-kvstore-tool.8*
%{_mandir}/man8/ceph-mds.8*
%{_mandir}/man8/ceph-mon.8*
%{_mandir}/man8/ceph-osd.8*
%{_mandir}/man8/ceph-post-file.8*
%{_mandir}/man8/ceph-rbdnamer.8*
%{_mandir}/man8/ceph-run.8*
%{_mandir}/man8/ceph-syn.8*
%{_mandir}/man8/ceph-volume.8*
%{_mandir}/man8/ceph-volume-systemd.8*
%{_mandir}/man8/cephadm.8*
%{_mandir}/man8/cephfs-mirror.8*
%{_mandir}/man8/cephfs-top.8*
%{_mandir}/man8/crushdiff.8*
%{_mandir}/man8/crushtool.8*
%{_mandir}/man8/librados-config.8*
%{_mandir}/man8/monmaptool.8*
%{_mandir}/man8/mount.ceph.8*
%{_mandir}/man8/mount.fuse.ceph.8*
%{_mandir}/man8/osdmaptool.8*
%{_mandir}/man8/rados.8*
%{_mandir}/man8/rbd.8*
%{_mandir}/man8/rbd-fuse.8*
%{_mandir}/man8/rbd-mirror.8*
%{_mandir}/man8/rbd-nbd.8*
%{_mandir}/man8/rbd-replay.8*
%{_mandir}/man8/rbd-replay-many.8*
%{_mandir}/man8/rbd-replay-prep.8*
%{_mandir}/man8/rbdmap.8*
%{_mandir}/man8/rgw-orphan-list.8*
%{_mandir}/man8/rgw-restore-bucket-index.8*

%dir %{_localstatedir}/lib/ceph
%dir %{_localstatedir}/lib/ceph/bootstrap-mds
%dir %{_localstatedir}/lib/ceph/bootstrap-mgr
%dir %{_localstatedir}/lib/ceph/bootstrap-osd
%dir %{_localstatedir}/lib/ceph/bootstrap-rbd
%dir %{_localstatedir}/lib/ceph/bootstrap-rgw
%dir %{_localstatedir}/lib/ceph/mds
%dir %{_localstatedir}/lib/ceph/mgr
%dir %{_localstatedir}/lib/ceph/mon
%dir %{_localstatedir}/lib/ceph/osd
%dir %{_localstatedir}/lib/ceph/tmp
%dir %{_localstatedir}/log/ceph
%dir %{_localstatedir}/run/ceph

%files libs
%defattr(644,root,root,755)
%if %{with bluefs}
%attr(755,root,root) %{_libdir}/libbluefs.so
%endif
%attr(755,root,root) %{_libdir}/libcephfs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcephfs.so.2
%attr(755,root,root) %{_libdir}/libmgr_op_tp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmgr_op_tp.so.1
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
%attr(755,root,root) %{_libdir}/librgw_op_tp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librgw_op_tp.so.2
%attr(755,root,root) %{_libdir}/librgw_rados_tp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librgw_rados_tp.so.2
%attr(755,root,root) %{_libdir}/libcephsqlite.so
%dir %{_libdir}/ceph
%attr(755,root,root) %{_libdir}/ceph/libceph-common.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcephfs.so
%attr(755,root,root) %{_libdir}/libmgr_op_tp.so
%attr(755,root,root) %{_libdir}/libos_tp.so
%attr(755,root,root) %{_libdir}/libosd_tp.so
%attr(755,root,root) %{_libdir}/librados.so
%attr(755,root,root) %{_libdir}/librados_tp.so
%attr(755,root,root) %{_libdir}/libradosstriper.so
%attr(755,root,root) %{_libdir}/librbd.so
%attr(755,root,root) %{_libdir}/librbd_tp.so
%attr(755,root,root) %{_libdir}/librgw.so
%attr(755,root,root) %{_libdir}/librgw_op_tp.so
%attr(755,root,root) %{_libdir}/librgw_rados_tp.so
%{_includedir}/cephfs
%{_includedir}/rados
%{_includedir}/radosstriper
%{_includedir}/rbd
%{_includedir}/libcephsqlite.h

%files -n python3-ceph
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/cephfs.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/rados.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/rbd.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/rgw.cpython-*.so
%{py3_sitedir}/cephfs-2.0.0-py*.egg-info
%{py3_sitedir}/rados-2.0.0-py*.egg-info
%{py3_sitedir}/rbd-2.0.0-py*.egg-info
%{py3_sitedir}/rgw-2.0.0-py*.egg-info
%{py3_sitescriptdir}/ceph_*.py
%{py3_sitescriptdir}/__pycache__/ceph_*.py*
%{py3_sitescriptdir}/ceph
%{py3_sitescriptdir}/ceph-1.0.0-py*.egg-info
%{py3_sitescriptdir}/ceph_node_proxy
%{py3_sitescriptdir}/ceph_node_proxy-1.0.0-py*.egg-info
%{py3_sitescriptdir}/ceph_volume
%{py3_sitescriptdir}/ceph_volume-1.0.0-py*.egg-info
%{py3_sitescriptdir}/cephfs_top-0.0.1-py*.egg-info

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
%attr(755,root,root) %{_bindir}/radosgw-es
%attr(755,root,root) %{_bindir}/radosgw-object-expirer
%attr(755,root,root) %{_bindir}/radosgw-token
%attr(755,root,root) %{_bindir}/rgw-policy-check
%{systemdunitdir}/ceph-radosgw.target
%{systemdunitdir}/ceph-radosgw@.service
%{_sysconfdir}/bash_completion.d/radosgw-admin
%dir %{_localstatedir}/lib/ceph/radosgw
%{_mandir}/man8/radosgw.8*
%{_mandir}/man8/radosgw-admin.8*
%{_mandir}/man8/rgw-policy-check.8*

%files resource-agents
%defattr(644,root,root,755)
%dir %{_prefix}/lib/ocf/resource.d/ceph
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/ceph/rbd

%if %{with tests}
%files test
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ceph-client-debug
%attr(755,root,root) %{_bindir}/ceph-coverage
%attr(755,root,root) %{_bindir}/ceph-debugpack
%attr(755,root,root) %{_bindir}/ceph-kvstore-tool
%attr(755,root,root) %{_bindir}/ceph-monstore-tool
%attr(755,root,root) %{_bindir}/ceph-osdomap-tool
%attr(755,root,root) %{_bindir}/ceph_bench_log
%attr(755,root,root) %{_bindir}/ceph_erasure_code
%attr(755,root,root) %{_bindir}/ceph_erasure_code_benchmark
%attr(755,root,root) %{_bindir}/ceph_kvstorebench
%attr(755,root,root) %{_bindir}/ceph_multi_stress_watch
%attr(755,root,root) %{_bindir}/ceph_objectstore_bench
%attr(755,root,root) %{_bindir}/ceph_omapbench
%attr(755,root,root) %{_bindir}/ceph_perf_local
%attr(755,root,root) %{_bindir}/ceph_perf_msgr_client
%attr(755,root,root) %{_bindir}/ceph_perf_msgr_server
%attr(755,root,root) %{_bindir}/ceph_perf_objectstore
%attr(755,root,root) %{_bindir}/ceph_psim
%attr(755,root,root) %{_bindir}/ceph_radosacl
%attr(755,root,root) %{_bindir}/ceph_rgw_jsonparser
%attr(755,root,root) %{_bindir}/ceph_rgw_multiparser
%attr(755,root,root) %{_bindir}/ceph_scratchtool
%attr(755,root,root) %{_bindir}/ceph_scratchtoolpp
%attr(755,root,root) %{_bindir}/ceph_smalliobench
%attr(755,root,root) %{_bindir}/ceph_smalliobenchdumb
%attr(755,root,root) %{_bindir}/ceph_smalliobenchfs
%attr(755,root,root) %{_bindir}/ceph_smalliobenchrbd
%attr(755,root,root) %{_bindir}/ceph_test_*
%attr(755,root,root) %{_bindir}/ceph_tpbench
%attr(755,root,root) %{_bindir}/ceph_xattr_bench
%attr(755,root,root) %{_libdir}/ceph/ceph-monstore-update-crush.sh
%{py3_sitedir}/ceph/tests
%{py3_sitedir}/ceph_volume/tests
%if %{with java}
%{_javadir}/libcephfs-test.jar
%endif
%{_mandir}/man8/ceph-debugpack.8*
%{_mandir}/man8/ceph-kvstore-tool.8*
%endif

%if %{with fio}
%files -n fio-ceph-objectstore
%defattr(644,root,root,755)
%doc src/test/fio/{README.md,ceph-*.conf,ceph-*.fio}
%attr(755,root,root) %{_libdir}/libfio_ceph_objectstore.so
%endif
