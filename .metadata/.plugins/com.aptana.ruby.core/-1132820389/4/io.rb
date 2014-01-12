class IO < Object
  include File::Constants
  include Enumerable

  SEEK_CUR = 1
  SEEK_END = 2
  SEEK_SET = 0
  WaitReadable = IO::WaitReadable
  WaitWritable = IO::WaitWritable

  def self.binread(arg0, arg1, *rest)
  end

  def self.binwrite(arg0, arg1, *rest)
  end

  def self.copy_stream(arg0, arg1, *rest)
  end

  def self.for_fd(arg0, arg1, *rest)
  end

  def self.foreach(arg0, arg1, *rest)
  end

  def self.new(arg0, arg1, *rest)
  end

  def self.open(arg0, arg1, *rest)
  end

  def self.pipe(arg0, arg1, *rest)
  end

  def self.popen(arg0, arg1, *rest)
  end

  def self.read(arg0, arg1, *rest)
  end

  def self.readlines(arg0, arg1, *rest)
  end

  def self.select(arg0, arg1, *rest)
  end

  def self.sysopen(arg0, arg1, *rest)
  end

  def self.try_convert(arg0)
  end

  def self.write(arg0, arg1, *rest)
  end


  def <<
  end

  def advise
  end

  def autoclose=
  end

  def autoclose?
  end

  def binmode
  end

  def binmode?
  end

  def bytes
  end

  def chars
  end

  def close
  end

  def close_on_exec=
  end

  def close_on_exec?
  end

  def close_read
  end

  def close_write
  end

  def closed?
  end

  def codepoints
  end

  def each
  end

  def each_byte
  end

  def each_char
  end

  def each_codepoint
  end

  def each_line
  end

  def eof
  end

  def eof?
  end

  def external_encoding
  end

  def fcntl
  end

  def fdatasync
  end

  def fileno
  end

  def flush
  end

  def fsync
  end

  def getbyte
  end

  def getc
  end

  def gets
  end

  def inspect
  end

  def internal_encoding
  end

  def ioctl
  end

  def isatty
  end

  def lineno
  end

  def lineno=
  end

  def lines
  end

  def pid
  end

  def pos
  end

  def pos=
  end

  def print
  end

  def printf
  end

  def putc
  end

  def puts
  end

  def read
  end

  def read_nonblock
  end

  def readbyte
  end

  def readchar
  end

  def readline
  end

  def readlines
  end

  def readpartial
  end

  def reopen
  end

  def rewind
  end

  def seek
  end

  def set_encoding
  end

  def stat
  end

  def sync
  end

  def sync=
  end

  def sysread
  end

  def sysseek
  end

  def syswrite
  end

  def tell
  end

  def to_i
  end

  def to_io
  end

  def tty?
  end

  def ungetbyte
  end

  def ungetc
  end

  def write
  end

  def write_nonblock
  end


  protected


  private

  def initialize
  end

  def initialize_copy
  end

end
