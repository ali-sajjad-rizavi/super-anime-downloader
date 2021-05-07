# Contributing to super-anime-downloader

Contributors are welcome! Read these instructions for contributing.

## Bug reports and feature requests

You can [create issues](https://github.com/ali-sajjad-rizavi/super-anime-downloader/issues) on GitHub with a nice title and description.

## Code contribution

This document will guide you through the contribution process.

### Step 1: Fork the project

- Fork the project on GitHub by clicking the *Fork* button at https://github.com/ali-sajjad-rizavi/super-anime-downloader
- Then clone it locally using:
```
git clone git@github.com:your_username/super-anime-downloader.git
cd super-anime-downloader
git remote add upstream git://github.com/ali-sajjad-rizavi/super-anime-downloader.git
```

### Step 2: Create a new branch

Create a feature branch and switch to it. Then start working on it.
```
git branch my-feature-branch
git checkout my-feature-branch
```
Make sure to add good commit messages! Push the changes from time to time using `git push` in your forked project's branch `my-feature-branch`. You can name your branch like you want, but it should be a good hint of what new feature or fix you intend to add.

### Step 3: Rebase if needed (Optional)

If you want to get latest changes from master, then use `git rebase` (not `git merge`).
```
git fetch upstream
git rebase upstream/master
```

### Step 4: Create a pull request

When you are done with the changes, create a pull request by going to https://github.com/your_username/super-anime-downloader.git and press the *Pull Request* button. There should be a good title and description as well!