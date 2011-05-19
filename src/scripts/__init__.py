__import__("pkg_resources").declare_namespace(__name__)

from sys import argv
from subprocess import Popen
from platform import system

def build(argv = ' '.join(argv[1:])):
    command = './bin/buildout -c buildout-build.cfg %s' % argv
    if system() == 'Darwin':
        command = './bin/buildout -c buildout-build-osx.cfg %s' % argv
    if system() == 'Windows':
        command = './bin/buildout -c buildout-build-windows.cfg %s' % argv
    print 'executing "%s"' % command
    process = Popen(command.split())
    stdout, stderr = process.communicate()
    exit(process.returncode)

def pack(argv = ' '.join(argv[1:])):
    command = './bin/buildout -c buildout-pack.cfg %s' % argv
    print 'executing "%s"' % command
    process = Popen(command.split())
    stdout, stderr = process.communicate()
    exit(process.returncode)

def clean(argv = ' '.join(argv[1:])):
    from os.path import abspath, curdir, sep, pardir
    from os import mkdir, remove
    from glob import glob
    from shutil import rmtree, move

    base = abspath(sep.join([__file__, pardir, pardir, pardir]))
    dist = sep.join([base, 'dist'])
    parts = sep.join([base, 'parts'])

    print "base = %s" % repr(base)

    for tar_gz in glob(sep.join([base, '*tar.gz'])):
        print "rm %s" % tar_gz
        remove(tar_gz)

    print "rm -rf %s" % repr(dist)
    _catch_and_print(rmtree, *[dist])

    src = sep.join([parts, 'buildout'])
    dst = sep.join([base ,'buildout'])
    print "mv %s %s" % (repr(src), repr(dst))
    _catch_and_print(move, *[src, dst])

    print "rm -rf %s" % repr(parts)
    _catch_and_print(rmtree, *[parts])

    print "mkdir %s" % repr(parts)
    _catch_and_print(mkdir, *[parts])

    dst = sep.join([parts, 'buildout'])
    src = sep.join([base ,'buildout'])
    print "mv %s %s" % (repr(src), repr(dst))
    _catch_and_print(move, *[src, dst])

def _catch_and_print(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except (OSError, IOError), e:
        print e

