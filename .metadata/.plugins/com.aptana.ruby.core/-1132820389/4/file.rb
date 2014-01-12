class File < IO
  include File::Constants
  include Enumerable

  ALT_SEPARATOR = nil
  Constants = File::Constants
  PATH_SEPARATOR = ":"
  SEPARATOR = "/"
  Separator = "/"
  Stat = File::Stat

  def self.absolute_path(arg0, arg1, *rest)
  end

  def self.atime(arg0)
  end

  def self.basename(arg0, arg1, *rest)
  end

  def self.blockdev?(arg0)
  end

  def self.chardev?(arg0)
  end

  def self.chmod(arg0, arg1, *rest)
  end

  def self.chown(arg0, arg1, *rest)
  end

  def self.ctime(arg0)
  end

  def self.delete(arg0, arg1, *rest)
  end

  def self.directory?(arg0)
  end

  def self.dirname(arg0)
  end

  def self.executable?(arg0)
  end

  def self.executable_real?(arg0)
  end

  def self.exist?(arg0)
  end

  def self.exists?(arg0)
  end

  def self.expand_path(arg0, arg1, *rest)
  end

  def self.extname(arg0)
  end

  def self.file?(arg0)
  end

  def self.fnmatch(arg0, arg1, *rest)
  end

  def self.fnmatch?(arg0, arg1, *rest)
  end

  def self.ftype(arg0)
  end

  def self.grpowned?(arg0)
  end

  def self.identical?(arg0, arg1)
  end

  def self.join(arg0, arg1, *rest)
  end

  def self.lchmod
  end

  def self.lchown(arg0, arg1, *rest)
  end

  def self.link(arg0, arg1)
  end

  def self.lstat(arg0)
  end

  def self.mtime(arg0)
  end

  def self.owned?(arg0)
  end

  def self.path(arg0)
  end

  def self.pipe?(arg0)
  end

  def self.readable?(arg0)
  end

  def self.readable_real?(arg0)
  end

  def self.readlink(arg0)
  end

  def self.realdirpath(arg0, arg1, *rest)
  end

  def self.realpath(arg0, arg1, *rest)
  end

  def self.rename(arg0, arg1)
  end

  def self.setgid?(arg0)
  end

  def self.setuid?(arg0)
  end

  def self.size(arg0)
  end

  def self.size?(arg0)
  end

  def self.socket?(arg0)
  end

  def self.split(arg0)
  end

  def self.stat(arg0)
  end

  def self.sticky?(arg0)
  end

  def self.symlink(arg0, arg1)
  end

  def self.symlink?(arg0)
  end

  def self.truncate(arg0, arg1)
  end

  def self.umask(arg0, arg1, *rest)
  end

  def self.unlink(arg0, arg1, *rest)
  end

  def self.utime(arg0, arg1, *rest)
  end

  def self.world_readable?(arg0)
  end

  def self.world_writable?(arg0)
  end

  def self.writable?(arg0)
  end

  def self.writable_real?(arg0)
  end

  def self.zero?(arg0)
  end


  def atime
  end

  def chmod
  end

  def chown
  end

  def ctime
  end

  def flock
  end

  def lstat
  end

  def mtime
  end

  def path
  end

  def size
  end

  def to_path
  end

  def truncate
  end


  protected


  private

  def initialize
  end

end
