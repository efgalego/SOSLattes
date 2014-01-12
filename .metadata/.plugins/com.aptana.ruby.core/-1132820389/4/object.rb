class Object < BasicObject
  include Kernel

  ARGF = ARGF
  ARGV = []
  ArgumentError = ArgumentError
  Array = Array
  BasicObject = BasicObject
  Bignum = Bignum
  Binding = Binding
  CROSS_COMPILING = nil
  Class = Class
  Comparable = Comparable
  Complex = Complex
  Config = RbConfig
  Data = Data
  Date = Date
  DateTime = DateTime
  Dir = Dir
  ENV = {"GNOME_KEYRING_CONTROL"=>"/run/user/eduardo/keyring-56Kdld", "XDG_SESSION_PATH"=>"/org/freedesktop/DisplayManager/Session0", "GTK_MODULES"=>"overlay-scrollbar", "SHLVL"=>"1", "SSH_AGENT_PID"=>"1306", "SESSION_MANAGER"=>"local/eduardo-notebook:@/tmp/.ICE-unix/1267,unix/eduardo-notebook:/tmp/.ICE-unix/1267", "GNOME_DESKTOP_SESSION_ID"=>"this-is-deprecated", "GDMSESSION"=>"ubuntu", "XDG_SESSION_COOKIE"=>"92e068c60ffd626710019727509411b5-1359891809.159376-1819038213", "COMPIZ_CONFIG_PROFILE"=>"ubuntu", "XDG_DATA_DIRS"=>"/usr/share/ubuntu:/usr/share/gnome:/usr/local/share/:/usr/share/", "MANDATORY_PATH"=>"/usr/share/gconf/ubuntu.mandatory.path", "PWD"=>"/home/eduardo/Desenvolvimento/Aptana_Studio_3", "LOGNAME"=>"eduardo", "GPG_AGENT_INFO"=>"/run/user/eduardo/keyring-56Kdld/gpg:0:1", "SSH_AUTH_SOCK"=>"/run/user/eduardo/keyring-56Kdld/ssh", "LD_LIBRARY_PATH"=>"/usr/lib/jvm/java-7-openjdk-i386/jre/lib/i386/client:/usr/lib/jvm/java-7-openjdk-i386/jre/lib/i386:", "DBUS_SESSION_BUS_ADDRESS"=>"unix:abstract=/tmp/dbus-CwLjRE1FtP,guid=92d3c1f3812c39ff45944936510e4d61", "SHELL"=>"/bin/bash", "LANGUAGE"=>"pt_BR:pt:en", "XDG_CURRENT_DESKTOP"=>"Unity", "XDG_CONFIG_DIRS"=>"/etc/xdg/xdg-ubuntu:/etc/xdg", "PATH"=>"/usr/lib/lightdm/lightdm:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games", "DESKTOP_SESSION"=>"ubuntu", "APTANA_VERSION"=>"3.3.1.1355795126", "DISPLAY"=>":0.0", "UBUNTU_MENUPROXY"=>"libappmenu.so", "USER"=>"eduardo", "HOME"=>"/home/eduardo", "XAUTHORITY"=>"/home/eduardo/.Xauthority", "DEFAULTS_PATH"=>"/usr/share/gconf/ubuntu.default.path", "XDG_SEAT_PATH"=>"/org/freedesktop/DisplayManager/Seat0", "XDG_RUNTIME_DIR"=>"/run/user/eduardo", "LANG"=>"pt_BR.UTF-8"}
  EOFError = EOFError
  Encoding = Encoding
  EncodingError = EncodingError
  Enumerable = Enumerable
  Enumerator = Enumerator
  Errno = Errno
  Etc = Etc
  Exception = Exception
  FALSE = false
  FalseClass = FalseClass
  Fiber = Fiber
  FiberError = FiberError
  File = File
  FileTest = FileTest
  FileUtils = FileUtils
  Fixnum = Fixnum
  Float = Float
  FloatDomainError = FloatDomainError
  GC = GC
  Gem = Gem
  Hash = Hash
  IO = IO
  IOError = IOError
  IndexError = IndexError
  Integer = Integer
  Interrupt = Interrupt
  Kernel = Kernel
  KeyError = KeyError
  LoadError = LoadError
  LocalJumpError = LocalJumpError
  Marshal = Marshal
  MatchData = MatchData
  Math = Math
  Method = Method
  Module = Module
  Mutex = Mutex
  NIL = nil
  NameError = NameError
  NilClass = NilClass
  NoMemoryError = NoMemoryError
  NoMethodError = NoMethodError
  NotImplementedError = NotImplementedError
  Numeric = Numeric
  OUTPUT_PATH = "/home/eduardo/Desenvolvimento/workspace/.metadata/.plugins/com.aptana.ruby.core/-1132820389/4/"
  Object = Object
  ObjectSpace = ObjectSpace
  Proc = Proc
  Process = Process
  Psych = Psych
  RUBY_COPYRIGHT = "ruby - Copyright (C) 1993-2012 Yukihiro Matsumoto"
  RUBY_DESCRIPTION = "ruby 1.9.3p194 (2012-04-20 revision 35410) [i686-linux]"
  RUBY_ENGINE = "ruby"
  RUBY_PATCHLEVEL = 194
  RUBY_PLATFORM = "i686-linux"
  RUBY_RELEASE_DATE = "2012-04-20"
  RUBY_REVISION = 35410
  RUBY_VERSION = "1.9.3"
  Random = Random
  Range = Range
  RangeError = RangeError
  Rational = Rational
  RbConfig = RbConfig
  Regexp = Regexp
  RegexpError = RegexpError
  RubyVM = RubyVM
  RuntimeError = RuntimeError
  STDERR = IO.new
  STDIN = IO.new
  STDOUT = IO.new
  ScanError = StringScanner::Error
  ScriptError = ScriptError
  SecurityError = SecurityError
  Signal = Signal
  SignalException = SignalException
  StandardError = StandardError
  StopIteration = StopIteration
  String = String
  StringIO = StringIO
  StringScanner = StringScanner
  Struct = Struct
  Syck = Syck
  Symbol = Symbol
  SyntaxError = SyntaxError
  SystemCallError = SystemCallError
  SystemExit = SystemExit
  SystemStackError = SystemStackError
  TOPLEVEL_BINDING = #<Binding:0x8100fec>
  TRUE = true
  TSort = TSort
  Thread = Thread
  ThreadError = ThreadError
  ThreadGroup = ThreadGroup
  Time = Time
  TrueClass = TrueClass
  TypeError = TypeError
  URI = URI
  UnboundMethod = UnboundMethod
  YAML = Psych
  ZeroDivisionError = ZeroDivisionError
  Zlib = Zlib

  def self.yaml_tag(arg0)
  end


  def psych_to_yaml(arg0, arg1, *rest)
  end

  def to_yaml(arg0, arg1, *rest)
  end

  def to_yaml_properties
  end


  protected


  private

  def dir_names(arg0)
  end

  def file_name(arg0)
  end

  def get_classes
  end

  def grab_instance_method(arg0, arg1)
  end

  def print_args(arg0)
  end

  def print_instance_method(arg0, arg1)
  end

  def print_method(arg0, arg1, arg2, arg3, arg4, *rest)
  end

  def print_type(arg0)
  end

  def print_value(arg0)
  end

end
