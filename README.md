Node.js
=======

This role makes Node.js available on a server.

Configuration
--------------

* `nvm_version`: Version of NVM to install. Default: `v0.25.4`.
* `node_version`: Version of node.js to install. Default: `v0.12.4`.
* `npm_version`: Version of NPM to install.
  Default: Use the version shipped with node.js.
* `nvm_system_wide_install`: When set to `false`, only the current user will have its `.bashrc` update to laod `nvm`.
  By default, all the users will load `nvm` when starting a new shell.

See also
---------

* [NVM](https://github.com/creationix/nvm)
* [Node.js](https://nodejs.org/)
