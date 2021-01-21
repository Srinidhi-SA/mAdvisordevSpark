from fabric.api import local

def prepare_UI():
    #local("curl -sL https://deb.nodesource.com/setup_8.x | bash -")
    local("apt-get install nodejs -y")
    local("node -v")
    local("npm -v")
    local("npm install")
    local("npm audit fix")
    local("npm run buildLinux")
