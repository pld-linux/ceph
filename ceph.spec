Summary:	User space components of the Ceph file system
Name:		ceph
Version:	0.51
Release:	2
License:	LGPLv2
Group:		Base
Source0:	http://ceph.newdream.net/download/%{name}-%{version}.tar.bz2
# Source0-md5:	e4d07eccd79c9a4a9eeee4066f2a13a3
Patch0:		%{name}-init-fix.patch
Patch1:		%{name}.logrotate.patch
Patch2:		%{name}-link.patch
URL:		http://ceph.newdream.net/
BuildRequires:	boost-devel
BuildRequires:	cryptopp-devel
BuildRequires:	curl-devel
BuildRequires:	expat-devel
BuildRequires:	fcgi-devel
BuildRequires:	gdbm-devel
BuildRequires:	google-perftools-devel
BuildRequires:	gtk+2-devel
BuildRequires:	gtkmm-devel
BuildRequires:	keyutils-devel
BuildRequires:	libatomic_ops
BuildRequires:	libedit-devel
BuildRequires:	libfuse-devel
BuildRequires:	libltdl-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtcmalloc-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	perl
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires(preun):	rc-scripts
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	gcephtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	libcls_.*.so.*

%description
Ceph is a distributed network file system designed to provide
excellent performance, reliability, and scalability.

%package libs
Summary:	Ceph shared libraries
Group:		Libraries

%description libs
Ceph shared libraries.

%package -n python-ceph
Summary:	Ceph python bindings
Group:		Development/Languages/Python
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-ceph
Ceph python bindings.

%package fuse
Summary:	Ceph fuse-based client
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description fuse
FUSE based client for Ceph distributed network file system

%package devel
Summary:	Ceph headers
License:	LGPLv2
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains the headers needed to develop programs that use
Ceph.

%package static
Summary:	Ceph static libraries
License:	LGPLv2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static Ceph libraries.

%package radosgw
Summary:	rados REST gateway
Group:		Development/Libraries
#Requires:	apache-mod_fcgid

%description radosgw
radosgw is an S3 HTTP REST gateway for the RADOS object store. It is
implemented as a FastCGI module using libfcgi, and can be used in
conjunction with any FastCGI capable web server.

%package obsync
Summary:	synchronize data between cloud object storage providers or a local directory
License:	LGPLv2
Group:		Applications/Networking
Requires:	python
Requires:	python-boto

%description obsync
obsync is a tool to synchronize objects between cloud object storage
providers, such as Amazon S3 (or compatible services), a Ceph RADOS
cluster, or a local directory.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--sbindir=/sbin \
	--without-hadoop \
	--with-radosgw \
	--with-gtk2

%{__make} V=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_localstatedir}/{lib/ceph/tmp,log/ceph/stat} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{ceph,bash_completion.d,logrotate.d,rc.d/init.d}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -p src/init-ceph $RPM_BUILD_ROOT/etc/rc.d/init.d/ceph
install -p src/logrotate.conf $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/ceph

%{__rm} $RPM_BUILD_ROOT%{_libdir}/rados-classes/*.{a,la}

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

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README src/sample.ceph.conf src/sample.fetch_config
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

%files -n python-ceph
%defattr(644,root,root,755)
%{py_sitescriptdir}/rados.py*
%{py_sitescriptdir}/rbd.py*

%files fuse
%defattr(644,root,root,755)
%doc COPYING
%attr(755,root,root) %{_bindir}/ceph-fuse
%{_mandir}/man8/ceph-fuse.8*

%files devel
%defattr(644,root,root,755)
%{_includedir}/cephfs
%{_includedir}/rados
%{_includedir}/rbd
%attr(755,root,root) %{_libdir}/libcephfs.so
%attr(755,root,root) %{_libdir}/librados.so
%attr(755,root,root) %{_libdir}/librbd.so
%{_libdir}/libcephfs.la
%{_libdir}/librados.la
%{_libdir}/librbd.la

%files static
%defattr(644,root,root,755)
%{_libdir}/libcephfs.a
%{_libdir}/librados.a
%{_libdir}/librbd.a

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
