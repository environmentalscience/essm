set -e # exit with nonzero exit code if anything fails

# clear and re-create the docs directory
# rm -rf build/sphinx/html || exit 0;

# compile docs
# python setup.py sphinx_build

# go to the docs directory and create a *new* Git repo
git clone -b gh-pages --single-branch https://${GH_TOKEN}@${GH_REF} gh-pages
rm -rf gh-pages/*.html gh-pages/styles gh-pages/scripts
cp -r docs/_build/html/* gh-pages
cd gh-pages

# set the user to invenio-developer
git config user.name "Stan Schymanski"
git config user.email "stan.schymanski@env.ethz.ch"

# add and commit
git add .
git commit -m "docs: deployment to github pages"

# push the docs to gh-pages
# git push --quiet origin gh-pages > /dev/null 2>&1
git push origin gh-pages
