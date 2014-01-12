class RubyVM < Object

  Env = RubyVM::Env
  INSTRUCTION_NAMES = ["nop", "getlocal", "setlocal", "getspecial", "setspecial", "getdynamic", "setdynamic", "getinstancevariable", "setinstancevariable", "getclassvariable", "setclassvariable", "getconstant", "setconstant", "getglobal", "setglobal", "putnil", "putself", "putobject", "putspecialobject", "putiseq", "putstring", "concatstrings", "tostring", "toregexp", "newarray", "duparray", "expandarray", "concatarray", "splatarray", "checkincludearray", "newhash", "newrange", "pop", "dup", "dupn", "swap", "reput", "topn", "setn", "adjuststack", "defined", "trace", "defineclass", "send", "invokesuper", "invokeblock", "leave", "finish", "throw", "jump", "branchif", "branchunless", "getinlinecache", "onceinlinecache", "setinlinecache", "opt_case_dispatch", "opt_checkenv", "opt_plus", "opt_minus", "opt_mult", "opt_div", "opt_mod", "opt_eq", "opt_neq", "opt_lt", "opt_le", "opt_gt", "opt_ge", "opt_ltlt", "opt_aref", "opt_aset", "opt_length", "opt_size", "opt_succ", "opt_not", "opt_regexpmatch1", "opt_regexpmatch2", "opt_call_c_function", "bitblt", "answer"]
  InstructionSequence = RubyVM::InstructionSequence
  OPTS = ["direct threaded code", "inline method cache"]
  USAGE_ANALYSIS_INSN = {}
  USAGE_ANALYSIS_INSN_BIGRAM = {}
  USAGE_ANALYSIS_REGS = {}



  protected


  private

end
