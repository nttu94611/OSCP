Source: https://gist.github.com/willurd/5720255

Author: William Bowers (willurd)

Additions: Oleg Mitrofanov (reider-roque)

Each of these commands will run an ad hoc http static server in your current (or specified) directory, available at http://localhost:[8000].

Check source page comments for more ideas!

### Python <= 2.3

```shell
$ python -c "import SimpleHTTPServer as s; s.test();" 8000
```

### Python >= 2.4

```shell
$ python -m SimpleHTTPServer 8000
```

### Python 3.x

```shell
$ python -m http.server 8000
```

### Python (Twisted)

```shell
$ # pip install twisted # install dependency if not already present
$ twistd -n web -p 8000 --path .
```

Or:

```shell
$ # pip install twisted # install dependency if not already present
$ python -c 'from twisted.web.server import Site; from twisted.web.static import File; 
from twisted.internet import reactor; reactor.listenTCP(8000, Site(File("."))); 
reactor.run()'
```

### Ruby 1.9.2+

```shell
$ ruby -run -e httpd . -p8000
```

Credit: [nobu](https://gist.github.com/willurd/5720255#comment-855952)

### Ruby (webrick)

```shell
$ # gem install webrick # install dependency for Ruby < 1.9.3
$ ruby -r webrick -e 'WEBrick::HTTPServer.new(:Port => 8000, :DocumentRoot => Dir.pwd).start'

$ # To kill it on Linux command line: ^Z + kill -9 %%1
```

Webrick is a part of standard library from [Ruby 1.9.3](https://en.wikipedia.org/wiki/WEBrick)

Credit: [Barking Iguana](http://barkingiguana.com/2010/04/11/a-one-line-web-server-in-ruby/)

### Ruby (adsf)

```shell
$ gem install adsf   # install dependency
$ adsf -p 8000
```

*No directory listings.*

Credit: [twome](https://gist.github.com/willurd/5720255/#comment-841393)

### Ruby (Sinatra)

```shell
$ gem install sinatra   # install dependency
$ ruby -r sinatra -e 'set :public_folder, "."; set :port, 8000'
```

*No directory listings.*

### Perl

```shell
$ # cpan HTTP::Daemon # install dependency if not already present
$ perl -MHTTP::Daemon -e '$d = HTTP::Daemon->new(LocalPort => 8000) or  +die $!; while 
($c = $d->accept) { while ($r = $c->get_request) { +$c->send_file_response(".".$r->url->path)
} }'
```
HTTP::Daemon comes preinstalled on many Linux distribution and thus works out of the box.

*No Directory listings.*

Credit: [Anonymous Monk](http://www.perlmonks.org/?node_id=865148)

### Perl (HTTP::Server::Brick)

```shell
$ cpan HTTP::Server::Brick   # install dependency
$ perl -MHTTP::Server::Brick -e '$s=HTTP::Server::Brick->new(port=>8000); 
$s->mount("/"=>{path=>"."}); $s->start'
```

Credit: [Anonymous Monk](http://www.perlmonks.org/?node_id=865239)

### Perl (IO::All)

```shell
$ cpan IO::All   # install dependency
$ perl -MIO::All -e 'io(":8080")->fork->accept->(sub { $_[0] < io(-x $1 ? "./$1 |" : $1) 
if /^GET \/(.*) / })'
```

Credit: [Anonymous Monk](http://www.perlmonks.org/?node_id=865148)

### Perl (Plack)

```shell
$ cpan Plack   # install dependency
$ plackup -MPlack::App::Directory -e 'Plack::App::Directory->new(root=>".");' -p 8000
```

Credit: [miyagawa](http://advent.plackperl.org/2009/12/day-5-run-a-static-file-web-server-with-plack.html)

### Perl (Mojolicious)

```shell
$ cpan Mojolicious::Lite   # install dependency
$ perl -MMojolicious::Lite -MCwd -e 'app->static->paths->[0]=getcwd; app->start' 
daemon -l http://*:8000
```

*No directory listings.*

### Node.js (http-server)

```shell
$ npm install -g http-server   # install dependency
$ http-server -p 8000
```

*Note: This server does funky things with relative paths. For example, if you have a file `/tests/index.html`, it will load `index.html` if you go to `/test`, but will treat relative paths as if they were coming from `/`.*

### Node.js (node-static)

```shell
$ npm install -g node-static   # install dependency
$ static -p 8000
```

*No directory listings.*

### PHP >= 5.4

```shell
$ php -S 127.0.0.1:8000
```

*No directory listings.*

Credit: [/u/prawnsalad](http://www.reddit.com/r/webdev/comments/1fs45z/list_of_ad_hoc_http_server_oneliners/cad9ew3) and [MattLicense](https://gist.github.com/willurd/5720255#comment-841131)

### Erlang

```shell
$ erl -s inets -eval 'inets:start(httpd,[{server_name,"NAME"},{document_root, "."},
{server_root, "."},{port, 8000},{mime_types,[{"html","text/html"},{"htm","text/html"},
{"js","text/javascript"},{"css","text/css"},{"gif","image/gif"},{"jpg","image/jpeg"},
{"jpeg","image/jpeg"},{"png","image/png"}]}]).'
```

Credit: [nivertech](https://gist.github.com/willurd/5720255/#comment-841166) (with the addition of some basic mime types)

*No directory listings.*

### busybox httpd

```shell
$ busybox httpd -f -p 8000
```

Credit: [lvm](https://gist.github.com/willurd/5720255#comment-841915)

### webfs

```shell
$ webfsd -F -p 8000
```

Depends on [webfs](http://linux.bytesex.org/misc/webfs.html).

### IIS Express

```shell
C:\> "C:\Program Files (x86)\IIS Express\iisexpress.exe" /path:C:\MyWeb /port:8000
```

*Depends on [IIS Express](http://www.iis.net/learn/extensions/introduction-to-iis-express/iis-express-overview).*

Credit: [/u/fjantomen](http://www.reddit.com/r/webdev/comments/1fs45z/list_of_ad_hoc_http_server_oneliners/cada8no)

*No directory listings. `/path` must be an absolute path.*

## Meta

If you have any suggestions to add to this list, a solution must:

1. Serve static files using your current directory (or a specified directory) as the server root.
2. Be able to be run with a single, one line command (dependencies are fine if they're a one-time thing).
3. Require no configuration (from files or otherwise) beyond the command itself (no framework-specific servers, etc)
