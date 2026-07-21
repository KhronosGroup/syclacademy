# How to update Revealjs and its dependencies

SYLC Academy uses `Revealjs` for it's lesson slide shows. For portability reasons `Revealjs` and it's revelant plugins are tracked inside the repo, so that you can 
simply clone the repo and open the lesson without installing any dependencies. Keeping the vendored code inside of node modules enables us to easily update `Revealjs` 
and its plugins. Updating dependencies requires `npm` to be installed on your system, but accessing slide content or even modifying slides does not. Other than CVEs and
new features there isn't much point to updating `Revealjs`.

## How to update Revealjs

Requires [npm](https://www.npmjs.com/) be installed on your system.

### Install the latest version via npm 

Run this command from the project root (where `package.json` and `package-lock.json` live):

```bash
npm i reveal.js@latest 
```
Can also tag specific versions like reveal.js@6.0.1

### Add any changes for Revealjs in node_modules
```bash
  git add node_modules/reveal.js/*
```

`.gitignore` is already set up to only include the needed files from the module. **Do not force include anything else from the module.** 

### Commit changes 

Thats it, fairly painless update proceedure.
