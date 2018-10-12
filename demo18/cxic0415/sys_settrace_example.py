import sys

def print_trace(frame, event, arg):
  if (event in ("call", "return")):
    sys.stderr.flush()
    fc = frame.f_code
    print "%s(%d) %s %s" % (fc.co_filename, frame.f_lineno, event, fc.co_name)
    sys.stdout.flush()
  return print_trace

def start_print_trace():
  sys.settrace(print_trace)

def stop_print_trace():
  sys.settrace(None)

def get_answer():
  return 42

def inner_loop(n_inner):
  for i in xrange(n_inner):
    get_answer()

def middle_loop(n_middle, n_inner):
  for i in xrange(n_middle):
    inner_loop(n_inner)

def outer_loop(n_outer, n_middle, n_inner):
  for i in xrange(n_outer):
    middle_loop(n_middle, n_inner)

def example(n_outer, n_middle, n_inner):
  outer_loop(n_outer, n_middle, n_inner)
  start_print_trace()
  outer_loop(n_outer, n_middle, n_inner)
  stop_print_trace()
  outer_loop(n_outer, n_middle, n_inner)

if __name__ == '__main__':
  example(2, 3, 4)
