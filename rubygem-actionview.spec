%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name actionview
%global bootstrap 1

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 4.2.6
Release: 1%{?dist}
Summary: Rendering framework putting the V in MVC (part of Rails)
Group: Development/Languages
License: MIT
URL: http://www.rubyonrails.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone http://github.com/rails/rails.git
# cd rails/actionview/
# git checkout v4.2.6
# tar czvf actionview-4.2.6-tests.tgz test/
Source1: %{gem_name}-%{version}-tests.tgz

Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(activesupport) = %{version}
Requires: %{?scl_prefix}rubygem(builder) >= 3.1
Requires: %{?scl_prefix}rubygem(builder) < 4
Requires: %{?scl_prefix}rubygem(erubis) >= 2.7.0
Requires: %{?scl_prefix}rubygem(erubis) < 2.8
Requires: %{?scl_prefix}rubygem(rails-dom-testing) >= 1.0.5
Requires: %{?scl_prefix}rubygem(rails-dom-testing) < 2
Requires: %{?scl_prefix}rubygem(rails-html-sanitizer) >= 1.0.2
Requires: %{?scl_prefix}rubygem(rails-html-sanitizer) < 2
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
%if 0%{bootstrap} < 1
BuildRequires: %{?scl_prefix}rubygem(activesupport) = %{version}
BuildRequires: %{?scl_prefix}rubygem(activerecord) = %{version}
BuildRequires: %{?scl_prefix}rubygem(actionpack) = %{version}
BuildRequires: %{?scl_prefix}rubygem(railties) = %{version}
BuildRequires: %{?scl_prefix}rubygem(sqlite3)
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildRequires: %{?scl_prefix}rubygem(mocha) >= 0.9.8
%endif
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

# Explicitly require runtime subpackage, as long as older scl-utils do not generate it
Requires: %{?scl_prefix}runtime

%description
Simple, battle-tested conventions and helpers for building web pages.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}


%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%if 0%{bootstrap} < 1

%check
pushd .%{gem_instdir}

tar xzvf %{SOURCE1} -C .

# This requires rails git structure and only requires bundler in the end
sed -i "s|require File.expand_path('../../../load_paths', __FILE__)||" ./test/abstract_unit.rb
sed -i '16,18d' ./test/active_record_unit.rb

# Run separately as we need to avoid superclass mismatch errors
%{?scl:scl enable %{scl} - << \EOF}
ruby -Ilib:test -e "Dir.glob('./test/{actionpack,activerecord,lib}/*_test.rb').each {|t| require t}"
ruby -Ilib:test -e "Dir.glob('./test/template/*_test.rb').each {|t| require t}"
%{?scl:EOF}

popd
%endif

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/MIT-LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/CHANGELOG.md

%changelog
* Mon Apr 04 2016 Pavel Valena <pvalena@redhat.com> - 4.2.6-1
- Update to 4.2.6

* Wed Feb 17 2016 Pavel Valena <pvalena@redhat.com> - 4.2.5.1-5
- Update to actionview 4.2.5.1

* Thu Feb 11 2016 Pavel Valena <pvalena@redhat.com> - 4.1.5-4
- Fix Possible Information Leak Vulnerability - rhbz#1301963
  - Resolves: CVE-2016-0752

* Tue Jan 27 2015 Josef Stribny <jstribny@redhat.com> - 4.1.5-3
- Enable tests

* Thu Jan 22 2015 Josef Stribny <jstribny@redhat.com> - 4.1.5-2
- Convert to SCL

* Mon Aug 25 2014 Josef Stribny <jstribny@redhat.com> - 4.1.5-1
- Update to actionview 4.1.5

* Fri Jul 04 2014 Josef Stribny <jstribny@redhat.com> - 4.1.4-1
- Update to actionview 4.1.4

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Josef Stribny <jstribny@redhat.com> - 4.1.1-1
- Update to ActionView 4.1.1

* Tue Apr 15 2014 Josef Stribny <jstribny@redhat.com> - 4.1.0-2
- Unpack test suite in %%check
- Adjust tests to run with all dependencies

* Thu Apr 10 2014 Josef Stribny <jstribny@redhat.com> - 4.1.0-1
- Initial package
