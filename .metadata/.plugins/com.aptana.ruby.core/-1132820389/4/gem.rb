module Gem

  Builder = Gem::Builder
  Cache = Gem::SourceIndex
  CommandLineError = Gem::CommandLineError
  ConfigFile = Gem::ConfigFile
  ConfigMap = {:ruby_version=>"1.9.1"}
  Dependency = Gem::Dependency
  DependencyError = Gem::DependencyError
  DependencyList = Gem::DependencyList
  DependencyRemovalException = Gem::DependencyRemovalException
  Deprecate = Gem::Deprecate
  DocumentError = Gem::DocumentError
  EndOfYAMLException = Gem::EndOfYAMLException
  Exception = Gem::Exception
  FilePermissionError = Gem::FilePermissionError
  FormatException = Gem::FormatException
  GEM_PRELUDE_SUCKAGE = nil
  GemNotFoundException = Gem::GemNotFoundException
  GemNotInHomeException = Gem::GemNotInHomeException
  GemPathSearcher = Gem::GemPathSearcher
  InstallError = Gem::InstallError
  InvalidSpecificationException = Gem::InvalidSpecificationException
  LoadError = Gem::LoadError
  MARSHAL_SPEC_DIR = "quick/Marshal.4.8/"
  OperationNotSupportedError = Gem::OperationNotSupportedError
  PathSupport = Gem::PathSupport
  Platform = Gem::Platform
  QUICKLOADER_SUCKAGE = nil
  RUBYGEMS_DIR = "/usr/lib/ruby/1.9.1"
  RbConfigPriorities = ["EXEEXT", "RUBY_SO_NAME", "arch", "bindir", "datadir", "libdir", "ruby_install_name", "ruby_version", "rubylibprefix", "sitedir", "sitelibdir", "vendordir", "vendorlibdir"]
  RemoteError = Gem::RemoteError
  RemoteInstallationCancelled = Gem::RemoteInstallationCancelled
  RemoteInstallationSkipped = Gem::RemoteInstallationSkipped
  RemoteSourceException = Gem::RemoteSourceException
  Requirement = Gem::Requirement
  RubyGemsPackageVersion = "1.8.23"
  RubyGemsVersion = "1.8.23"
  SourceIndex = Gem::SourceIndex
  SpecFetcher = Gem::SpecFetcher
  Specification = Gem::Specification
  SystemExitException = Gem::SystemExitException
  VERSION = "1.8.23"
  VerificationError = Gem::VerificationError
  Version = Gem::Version
  WIN_PATTERNS = [/bccwin/i, /cygwin/i, /djgpp/i, /mingw/i, /mswin/i, /wince/i]

  def self._deprecated_activate(arg0, arg1, arg2, *rest)
  end

  def self._deprecated_activate_dep(arg0, arg1, arg2, *rest)
  end

  def self._deprecated_activate_spec(arg0)
  end

  def self._deprecated_all_load_paths
  end

  def self._deprecated_available?(arg0, arg1, arg2, *rest)
  end

  def self._deprecated_cache
  end

  def self._deprecated_cache_dir(arg0, arg1, *rest)
  end

  def self._deprecated_cache_gem(arg0, arg1, arg2, *rest)
  end

  def self._deprecated_default_system_source_cache_dir
  end

  def self._deprecated_default_user_source_cache_dir
  end

  def self._deprecated_latest_load_paths
  end

  def self._deprecated_promote_load_path(arg0, arg1)
  end

  def self._deprecated_required_location(arg0, arg1, arg2, arg3, *rest)
  end

  def self._deprecated_searcher
  end

  def self._deprecated_source_index
  end

  def self.activate(arg0, arg1, *rest)
  end

  def self.activate_dep(arg0, arg1, *rest)
  end

  def self.activate_spec(arg0, arg1, *rest)
  end

  def self.all_load_paths(arg0, arg1, *rest)
  end

  def self.all_partials(arg0, arg1, *rest)
  end

  def self.available?(arg0, arg1, *rest)
  end

  def self.bin_path(arg0, arg1, arg2, *rest)
  end

  def self.binary_mode
  end

  def self.bindir(arg0, arg1, *rest)
  end

  def self.cache(arg0, arg1, *rest)
  end

  def self.cache_dir(arg0, arg1, *rest)
  end

  def self.cache_gem(arg0, arg1, *rest)
  end

  def self.clear_paths
  end

  def self.config_file
  end

  def self.configuration
  end

  def self.configuration=(arg0)
  end

  def self.datadir(arg0)
  end

  def self.default_bindir
  end

  def self.default_dir
  end

  def self.default_exec_format
  end

  def self.default_path
  end

  def self.default_rubygems_dirs
  end

  def self.default_sources
  end

  def self.default_system_source_cache_dir(arg0, arg1, *rest)
  end

  def self.default_user_source_cache_dir(arg0, arg1, *rest)
  end

  def self.deflate(arg0)
  end

  def self.dir
  end

  def self.ensure_gem_subdirectories(arg0, arg1, *rest)
  end

  def self.find_files(arg0, arg1, arg2, *rest)
  end

  def self.gunzip(arg0)
  end

  def self.gzip(arg0)
  end

  def self.host
  end

  def self.host=(arg0)
  end

  def self.inflate(arg0)
  end

  def self.latest_load_paths(arg0, arg1, *rest)
  end

  def self.latest_rubygems_version
  end

  def self.latest_spec_for(arg0)
  end

  def self.latest_version_for(arg0)
  end

  def self.load_env_plugins
  end

  def self.load_path_insert_index
  end

  def self.load_plugin_files(arg0)
  end

  def self.load_plugins
  end

  def self.load_yaml
  end

  def self.loaded_path?(arg0)
  end

  def self.loaded_specs
  end

  def self.location_of_caller
  end

  def self.marshal_version
  end

  def self.path
  end

  def self.paths
  end

  def self.paths=(arg0)
  end

  def self.platforms
  end

  def self.platforms=(arg0)
  end

  def self.post_build
  end

  def self.post_build_hooks
  end

  def self.post_install
  end

  def self.post_install_hooks
  end

  def self.post_reset
  end

  def self.post_reset_hooks
  end

  def self.post_uninstall
  end

  def self.post_uninstall_hooks
  end

  def self.pre_install
  end

  def self.pre_install_hooks
  end

  def self.pre_reset
  end

  def self.pre_reset_hooks
  end

  def self.pre_uninstall
  end

  def self.pre_uninstall_hooks
  end

  def self.prefix
  end

  def self.promote_load_path(arg0, arg1, *rest)
  end

  def self.read_binary(arg0)
  end

  def self.refresh
  end

  def self.report_activate_error(arg0, arg1, *rest)
  end

  def self.required_location(arg0, arg1, *rest)
  end

  def self.ruby
  end

  def self.ruby_engine
  end

  def self.ruby_version
  end

  def self.searcher(arg0, arg1, *rest)
  end

  def self.source_index(arg0, arg1, *rest)
  end

  def self.sources
  end

  def self.sources=(arg0)
  end

  def self.suffix_pattern
  end

  def self.suffixes
  end

  def self.time(arg0, arg1, arg2, *rest)
  end

  def self.try_activate(arg0)
  end

  def self.ui
  end

  def self.unresolved_deps
  end

  def self.use_paths(arg0, arg1, arg2, *rest)
  end

  def self.user_dir
  end

  def self.user_home
  end

  def self.win_platform?
  end



  protected


  private

end
