shellscript commands to implement
=================================


v0.1
~~~~
date
----
-d
-f
-I
-r
-R
--rfc-3339
-s
-u

hostname
--------
-a
-d
-f
-A
-i
-I
-s
-y
-b
-F

mv
--
--backup
-b
-f
-i
-n
--strip-trailing-slashes
-S
-t
-T
-u
-v
-Z

rm
--
-f
-i
-I
--interactive
--one-file-system
--no-preserve-root
--preserve-root
-r
-d
-v
sleep
-----

tee
---
-a

touch
-----
-a
-c
-d
-h
-m
-r
-t

uname
-----
-a
-s
-n
-r
-v
-m
-p
-i
-o

wc
--
-c
-m
-l
-L
-w

which
-----
-a

whoami
------

yes
---


v0.2
~~~~
diff
----
--normal
-q
-s
-c
-u
-e
-n
-y
-W
--left-column
--suppress-common-lines
-p
-F
--label
-t
-T
--tabsize
--suppress-blank-empty
-l
-r
-N
--unidirectional-new-file
--ignore-file-name-case
--no-ignore-file-name-case
-x
-X
-S
--from-file
--to-file
-i
-E
-Z
-b
-W
-B
-I
-a
--strip-trailing-cr
-D
-GTYPE
--line-format
--LTYPE
-d
--horizon-lines
--speed-large-files

du
--
-0
-a
--apparent-size
-B
-b
-c
-D
-d
-H
-h
--inodes
-k
-L
-l
-m
-P
-S
-si
-s
-t
--time
-X
--exclude
-x

find 
----
-P
-L
-H
-O
-d
--daystart
--depth
-maxdepth
-mindepth
-mount
-noleaf
-warn
-xdef
+n
-n
n
-amin
-anewer
-atime
-cmin
-cnewer
-ctime
-empty
-exectuable
-false
-fstype
-gid
-group
-ilname
-iname
-inum
-ipath
-iregexp
-iwholename
-links
-lname
-mmin
-mtime
-name
-newer
-newerXY
-nogroup
-nouser
-path
-perm
-readable
-regex
-samefile
-size
-true
-type
-uid
-used
-user
-wholename
-writeable
-xtype
-delete
-exec
-execdir
-fls
-fprint
-ls
-ok
-okdir
-print
-print0
-prune
-quit

head
----
-c
-n
-q
-v

kill
----
-0123456789
-s
--signal
-l
-L

less
----

mkdir
-----
-m
-p
-v
-Z

ping
----
-a
-A
-b
-B
-d
-D
-f
-h
-L
-n
-O
-q
-r
-R
-U
-v
-V
-c
-F
-i
-I
-l
-m
-M
-N
-w
-W
-p
-Q
-s
-S
-t
-T

sed
---
-n
-e
-i
-f
-l
--posix
-r
-s
-u
-z

sort
----
-b
-d
-f
-g
-i
-M
-h
-n
-R
--random-source
-r
--sort
-V
-c
-C
-k
-m
-o
-s
-S
-t
-T
--parallel
-u
-z

stat
----
-L
-f
-c
--printf
-t

tail
----
-c
-F
-f
-n
-q
--retry
-s
-v

timeout
-------
-k
-s

time
----

umask
-----

uniq
----
-c
-d
-D
-f
--group
-i
-s
-u
-z
-w

v0.3
~~~~
chgrp
-----
-c
-f
-v
--dereference
--no-preserve-root
--preserve-root
-R
-H
-L
-P

chmod
-----
-c
-f
-v
--no-preserve-root
--preserve-root
-R

chown
-----
-c
-f
-v
--dereference
-h
-from
--no-preserve-root
--preserve-root
--reference
-R
-H
-L
-P

clear
-----

history
-------

man
---


Future versions
~~~~~~~~~~~~~~~
awk
---

cat
---
-n
-E
-s
-T 

bzip2
-----
-c
-d
-f
-k
-q
-s
-t
-v
-z
-V
-L
-123456789 

cp
--
-a
--attributes-only
--backup
-b
--copy-contents
-d
-f
-i
-H
-l
-L
-n
-P
-p (only timestamp and mode supported)
--preserve (only timestamp and mode supported)
--no-preserve
--parents
-reflink
--remove-destination
--sparse
--strip-trailing-slashes
-s
-S
-t
-T
-u
-x
-z
--context


curl
----

dd
--
bs
cbs
conv
count
ibs
if
iflag
obs
of
oflag
seek
skip
status

df
--
-a
-B
--total
-h
-H
-i
-k
-l
--no-sync
--output
-P
--sync
-t
-T
-x

file
----
-b
-c
-E
-h
-i
-k
-l
-L
-N
-n
-p
-r
-s
-v
-z
-Z
-0
--apple
--extension
--mime-encoding
--mime-type
-e
-F
-f
-m
-P 
-C
-m

grep
----
-E
-F
-G
-P
-e
-f
-i
-v
-w
-x
-y
-c
--color
-L
-l
-m
-o
-p
-s
-b
-H
-h
--label
-n
-T
-u
-Z
-A
-B
-C
-a
--binary-files
-D
-d
--exclude
-I
--include
-r
-R
--line-buffered
-U
-z

gzip
----
-a
-c
-d
-f
-h
-k
-l
-L
-n
-N
-r
-t
-v
-V
-1
-9
--rsyncable
-S

gunzip
------
-a
-c
-f
-h
-k
-l
-L
-n
-N
-r
-t
-v
-V
-S

ifconfig
--------
-v
-a
-s

killall
-------
-
--co
-e
-g
-i
-o
-q
-r
-s
-u
-v
-w
-y
-I
-V

ls
--
-a
-A
--author
-b
--block-size
-B
-c
-C
--color
-d
-D
-f
-F
--file-type
--format
--full-time
-g
--group
-G
-h
-si
-H
--hide
--indicator-style
-i
-I
-k
-l
-L
-m
-n
-N
-o
-p
-q
--show-control-chars
-Q
--quoting-style
-r
-R
-s
-S
--sort
--time
--time-style
-t
-T
-u
-U
-v
-w
-X
-x
-Z
-1

lsof
----
-?
-a
-b
-C
-h
-K
-l
-n
-N
-O
-P
-R
-t
-U
-v
-V
-X
-A
-c
-d
-D
-e
-E
-f
-k
-L
-m
-M
-o
-p
-r
-s
-S
-T
-u
-w
-x
-z
-Z

mount
-----
-l
-h
-V
-a
-f
-F
-n
-r
-s
-v
-w
-t
-O
-f
-n
-r
-s
-v
-w
-o
-t
-o

popd
----
-n
+n
-0-9

ps
--
-A
-a
-d
--deselect
-e
-g
-N
-T
-r
-x
-123
-C
-G
-g
--Group
--group
p
-p 
--pid
--ppid
q
-q
--quick-pid
-s
--sid
t
-t
--tty
U
-U
-u
--User
--user
-c
--context
-f
-F
--format
j
-j
l
-l
-M
O
-O
o
-o
s
u
v
x
X
-y
Z
c
--cols
--columns
--cumulative
e
f
--forest
h
-H
--headers
k
--lines
-n
n
N
--no-headers
O
--rows
S
--sort
w
-w
--width
H
-L
m
-m
-T


pushd
-----
-n
+n
-0-9

scp
---
-12346
-B
-C
-p
-q
-r
-v
-c
-f
-F
-i
-l
-o
-S

shutdown
--------
-H
-P
-r
-h
-k
--no-wall
-c

ssh
---
-1246
-A
-a
-C
-f
-G
-g
-K
-k
-M
-N
-n
-q
-s
-T
-t
-V
-v
-X
-x
-Y
-y
-b
-c
-D
-E
-e
-F
-I
-i
-L
-l
-m
-O
-o
-p
-Q
-R
-S
-W
-w

tar
---

top
---
-b
-c
-d
-H
-i
-n
-o
-O
-p
-s
-S
-u
-w

umount
------
-a
-A
-c
-d
--fake
-f
-i
-l
-n
-O
-R
-r
-t
-v

uptime
------
-p
-s

who
---
-a
-b
-d
-H
-l
--lookup
-m
-p
-q
-r
-s
-t
-T
-u

xz
--
-q
-v
-T
--fast
--best
-e
-0123456789
-c
--files
-S
-k
-f
-s
-l
-t
-d
-z

zip
---
-a
-A
-B
-c
-d
-D
-e
-E
-f
-F
-g
-j
-k
-l
-L
-m
-o
-q
-r
-R
-S
-T
-u
-v
-V
-w
-X
-y
-z
-!
-@
-$

Done
~~~~
alias
-----

cd
--

pwd
---

To be provided by Python
~~~~~~~~~~~~~~~~~~~~~~~~
basename
--------
Use os.path.basename.

cut
---
Use Python string operations.

dirname
-------
Use os.path.dirname.

more
----
We only need less.

printf
------
Use the python print statement.

source
------
Use Python means (exec, import ...).

tr
--
Python string operations.

wget
----
Replaced by curl.

xargs
-----
Not needed in Python.


Unknown
~~~~~~~
bg
--

fg
--

ftp
---

link
----

ln
--

locate
------

logout
------

mkisofs
-------

netstat
-------

nice
----

sftp
----

strace
------

su
--

sync
----

wait
----

unrar
-----




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

