FROM ubuntu
MAINTAINER Denis Krienbühl, denis.krienbuehl@seantis.ch

# avoid errors during docker build
ENV DEBIAN_FRONTEND noninteractive

# update the base
RUN apt-get update

# get the basics
RUN apt-get install -y python2.7 python2.7-dev git curl

# required by lxml
RUN apt-get install -y libxml2 libxml2-dev libxslt1.1 libxslt1-dev

# required by python image library
RUN apt-get install -y libjpeg62-dev zlib1g-dev libfreetype6-dev liblcms1-dev

# required for mime type checking
RUN apt-get install libmagic1

# add the user for the plone instance
RUN adduser onegov

# prepare the folders
RUN mkdir /onegov
RUN chown onegov:onegov /onegov

# get source
RUN su onegov -c "git clone https://github.com/OneGov/onegov.municipality /onegov"

# speed up plone install
RUN su onegov -c "curl -L https://launchpad.net/plone/4.3/4.3.3/+download/Plone-4.3.3-UnifiedInstaller.tgz > /tmp/installer.tar.gz"
RUN su onegov -c "mkdir /tmp/installer"
RUN su onegov -c "cd /tmp/installer && tar -xf /tmp/installer.tar.gz --strip-components 1"
RUN su onegov -c "cd /onegov && tar -xf /tmp/installer/packages/buildout-cache.tar.bz2"

ADD demo.cfg /onegov/demo.cfg

# config
EXPOSE 8080

# bootstrap our instance
RUN su onegov -c "cd /onegov && python bootstrap.py"
RUN su onegov -c "cd /onegov && bin/buildout -c demo.cfg"

USER onegov
ENTRYPOINT ["/onegov/bin/instance"]
