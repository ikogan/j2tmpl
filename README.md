# Jinja 2 Command Line Template Renderer

[![Build Status](https://travis-ci.org/ikogan/j2tmpl.svg?branch=master)](https://travis-ci.org/ikogan/j2tmpl)

Jinja2 command line renderer that converts environment variables
into objects on the context. For example:

```
DATABASE_MAIN_URI=mysql:3306
DATABASE_MAIN_USERNAME=app
DATABASE_CACHE_URI=redis:6379
DATABASE_CACHE_USERNAME=app
```

Becomes:

```json
{
    "database": {
        "main": {
            "uri": "mysql:3306",
            "username": "app"
        },
        "cache": {
            "uri": "redis:6379",
            "username": "app"
        }
    }
}
```

This allows using things like iterations and others for more
dynamic templates.

While [there](https://sudo.isl.co/shinto-cli/)
[are](https://github.com/kolypto/j2cli)
[several](https://github.com/mattrobenolt/jinja2-cli) command line
Jinja2 template renderers, they all share a single property that this
attempts to solve.

Of those that support environment variables (for Docker, typically),
those environment variables are presented to the template verbatum.
That is, given this environment:

```
DATABASE_MAIN_URI=mysql:3306
DATABASE_MAIN_USERNAME=app
DATABASE_CACHE_URI=redis:6379
DATABASE_CACHE_USERNAME=app
```

A template would have to use them in the following way:

```jinja
databases: {
    main: {
        uri: {{ DATABASE_MAIN_URI }}
        username: {{ DATABASE_MAIN_USERNAME }}
    cache: {
        uri: {{ DATABASE_CACHE_URI }}
        username {{ DATABASE_CACHE_USERNAME }}
```

Suppose, though, that you don't necessarily know how many databases
your container will have? This construct makes it diffcult in those
instances where you have to define *N* things differently depending
on a container deployment, or for base images.

```jinja
databases: {
    {% for name,definition in databases.items() %}
    {{ name }}: {
        uri: {{ definition.uri }},
        username: {{ definition.username }}
    },
    {% endfor %}
```

### Handling Collisions

Environment variables can sometimes cause interesting
problems when building a tree structure. A `ValueError` will
be thrown if a variable is defined twice. Howver, the following
is a valid set of environment variables:

```
AUTH_LDAP=true
AUTH_LDAP_USERNAME=app
```

In the template context, `{{ auth.ldap }}` has to be an object as
`username` is a key inside of it. In this case, the value of
`AUTH_LDAP` will be moved down into a special `_` key. The two
variables would then be:

```jinja
{{ auth.ldap._ }}=true
{{ auth.ldap.username }}=app
```

For this to work, almost all `_` in environment keys are removed.
So, `AUTH__LDAP_` is still translated to `{{ auth.ldap }}`. The only
exception is a variable with *just* underscores. In this case, a '_'
is added to the root of the context with that value. Note that all
of the following would create this single underscore value:

- `_`
- `___`
- `____________________`

If multiple solely-underscore environment variables exist, a `ValueError`
is thrown.

## Installation

This can be installed in two ways:

1. `pip3 install j2tmpl`
2. Download the prebuilt binaries.

Note that the prebuilt binaries include the entire Python interpreter
so they can be used just as easily as
[confd](https://github.com/kelseyhightower/confd).

## Usage

This can be used in two ways: processing a single file, or an entire directory.

When a directory path is passed as the template file,
`j2tmpl` will scan the directory for any files with
an extension matching `template-extensions`, an argument that
defaults to `tmpl,jinja,jinja2,j2,jnj`.

> Note that it will _still_ output to stdout unless `-o` is used.
> If it is, then make sure it's a directory as well. If the
> target directory doesn't exist, it will be created.

In addition to files matching that pattern, any _directory_
that matches that pattern and also ends with `.d` will be
scanned for template fragments. Template files as well
as files in `.d` directories that end in those extensions will
all be concatenated together and rendered into one output file
that matches the name of the directory without the template
extension and without `.d`.

For example, given the following directory structure:

```
foo.conf.jinja.d/
    foo-1.jinja
    foo-2.jinja
bar.conf.jinja.d/
    bar-1.jinja
    bar-2.jinja
foo.conf.jinja
baz.conf.jinja
```

The output directory will contain the following:

```
bar.conf
baz.conf
foo.conf
```

## Built-In Filters and extensions

Jinja's [do](http://jinja.pocoo.org/docs/2.10/extensions/#expression-statement)
and [loopcontrols](http://jinja.pocoo.org/docs/2.10/extensions/#loop-controls)
extensions are enabled by default as are
the [trim_blocks](http://jinja.pocoo.org/docs/2.10/api/#jinja2.Environment)
and [lstrip_blocks](http://jinja.pocoo.org/docs/2.10/api/#jinja2.Environment)

Finally, the following additionals filters are avilable:

**readfile(str)**:
    Read in the contents of the file represented by `str`. This is particularly
    useful for container secrets.

**boolean(str)**:
    Convert the argument into a boolean. A case insensitive comparison to
    "true", "yes", "on", and "1" will return `True`. Everything else is false.

**b64encode(str)**:
    Base 64 encode the value.

**b64decode(str)**:
    Base 64 decode the value.

## Why not confd?

Speaking of confd, why not just use it? While confd is great, it can
be a bit too verbose. Having to define a series of config files with
all keys enurmated for every single key can be daunting. For certain
projects, it probably makes sense, but I would often like to just
barf some environment variables into a configuration file with only
a tiny amount complexity.

confd is a 5.5mb or so binary and this is still less than 15mb. There are likely
ways to make this smaller that I would love to explore.
