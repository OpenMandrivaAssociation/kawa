%define gcj_support 0
%define build_free 1
%define section free
%bcond_without servlet

Name:           kawa
Version:        1.8
Release:        %mkrel 5
Epoch:          0
Summary:        Framework for implementing high-level and dynamic languages
License:        GPL
Group:          Development/Java
#Vendor:         JPackage Project
#Distribution:   JPackage
Source0:        ftp://ftp.gnu.org/pub/gnu/kawa/kawa-1.8-src.tar.bz2
URL:            http://www.gnu.org/software/kawa/index.html
Requires:       jpackage-utils
%if %with servlet
Requires:       servletapi5
%endif
Requires:       xml-commons-apis
BuildRequires:  java-devel
BuildRequires:  jpackage-utils
BuildRequires:  libtool
%if %with servlet
BuildRequires:  servletapi5
%endif
BuildRequires:  xml-commons-apis
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

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
export CLASSPATH=$(build-classpath xml-commons-apis)
export JAR=%{jar}
export JAVA=%{java}
export JAVAC=%{javac}
export JAVADOC=%{javadoc}
%configure2_5x \
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
%makeinstall LIBTOOL=%{_bindir}/libtool
%if !%with servlet
%{__rm} -f %{buildroot}%{_bindir}/cgi-servlet
%endif
%make JAVADOC_DIR=%{buildroot}%{_javadocdir}/%{name}-%{version} install-javadoc-html

# javadoc
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name} # ghost symlink

%if %{gcj_support}
RPM_OPT_FLAGS=`echo %{optflags} | %{__sed} 's|-O[0-9]*|-O0|'` \
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

%postun
%if %{gcj_support}
%{clean_gcjdb}
%endif
%_remove_install_info %{name}.info
%_remove_install_info %{name}-tour.info

%post javadoc
%{__rm} -f %{_javadocdir}/%{name}
%{__ln_s} %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ $1 -eq 0 ]; then
  %{__rm} -f %{_javadocdir}/%{name}
fi

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
%ghost %doc %{_javadocdir}/%{name}
