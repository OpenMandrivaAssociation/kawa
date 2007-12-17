%define gcj_support     1
%define build_free      1
%define section         free
%bcond_without          servlet

Name:           kawa
Version:        1.9.1
Release:        %mkrel 4
Epoch:          0
Summary:        Framework for implementing high-level and dynamic languages
License:        GPL
Group:          Development/Java
URL:            http://www.gnu.org/software/kawa/index.html
Source0:        ftp://ftp.gnu.org/pub/gnu/kawa/kawa-%{version}.tar.gz
Source1:        ftp://ftp.gnu.org/pub/gnu/kawa/kawa-%{version}.tar.gz.sig
Requires(post): info-install
Requires(preun): info-install
Requires:       jpackage-utils
%if %with servlet
Requires:       servletapi5
%endif
Requires:       xml-commons-jaxp-1.3-apis
BuildRequires:  java-devel
BuildRequires:  java-rpmbuild
BuildRequires:  libtool
%if %with servlet
BuildRequires:  servletapi5
%endif
BuildRequires:  xml-commons-jaxp-1.3-apis
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%endif

%description

Kawa is:
    * A framework written in Java for implementing high-level and
      dynamic languages, compiling them into Java bytecodes.
    * An implementation of Scheme, which is in the Lisp family of
      programming languages. Kawa is a featureful dialect in its own
      right, and additionally provides very useful integration with
      Java. It can be used as a "scripting" language, but includes a
      compiler and all the benefits of a "real" programming
      language, including optional static typing.
    * Implementations of other programming languages, including
      XQuery (Qexo) and Emacs Lisp (JEmacs).

%package        javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description    javadoc
Javadoc for %{name}.

%prep
%setup -q

%build
export CLASSPATH=$(build-classpath xml-commons-jaxp-1.3-apis)
export JAR=%{jar}
export JAVA=%{java}
export JAVAC=%{javac}
export JAVADOC=%{javadoc}
%{configure2_5x} \
  --without-gcj \
%if %with servlet
  --with-servlet=$(build-classpath servletapi5) \
%else
  --without-servlet \
%endif
%if !%{build_free}
  --with-swing \
%else
  --without-swing \
%endif
  --without-swt \
  --with-awt \
  --with-sax2 \
%if %{build_free}
  --with-java-source=1.4
%else
  --with-java-source=1.5
%endif
%{__make} LIBTOOL=%{_bindir}/libtool

%install
%{__rm} -rf %{buildroot}
%{makeinstall} LIBTOOL=%{_bindir}/libtool
%if !%with servlet
%{__rm} -f %{buildroot}%{_bindir}/cgi-servlet
%endif
%{make} JAVADOC_DIR=%{buildroot}%{_javadocdir}/%{name}-%{version} install-javadoc-html

# javadoc
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%post
%if %{gcj_support}
%{update_gcjdb}
%endif
%_install_info %{name}.info
%_install_info %{name}-tour.info

%preun
%_remove_install_info %{name}.info
%_remove_install_info %{name}-tour.info

%if %{gcj_support}
%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README TODO
%if %with servlet
%attr(0755,root,root) %{_bindir}/cgi-servlet
%endif
%attr(0755,root,root) %{_bindir}/kawa
%attr(0755,root,root) %{_bindir}/qexo
%{_infodir}/%{name}.info*
%{_infodir}/%{name}-tour.info*
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/%{name}-%{version}.jar.*
%endif
%{_mandir}/man1/kawa.1*
%{_mandir}/man1/qexo.1*

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
