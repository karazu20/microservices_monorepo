#!/bin/bash

echo "RULE # 1: Checking the commit message format..."
if [[ ! "${CI_COMMIT_MESSAGE}" =~ "bugfix: "*|"feature: "*|"architecture: "*|"documentation: "*|"refactor: "*|"dependency: "*|"quality: "* ]];
then
    echo "❌ Invalid commit message format!"
    echo "Only valid messages bugfix, feature, documentation, refactor, dependency, quality, architecture"
    exit 1
else
    echo "✅ Commit message format"
fi

REMOTE_REF=`[ $CI ] && echo "upstream/" || echo ""`

LATEST_MASTER_HASH=$(git rev-parse upstream/main)
LATEST_SHARED_HASH=$(git merge-base upstream/main ${REMOTE_REF}${CI_COMMIT_REF_NAME})

echo "RULE # 2: Checking rebase with main..."
if [[ ! $LATEST_MASTER_HASH == $LATEST_SHARED_HASH ]];
then
    echo "❌ You need to rebase with main! git rebase upstream/main"
    exit 1
else
    echo "✅ Rebase with upstream main"
fi

MODIFICATIONS=$(git diff --shortstat upstream/main ${REMOTE_REF}${CI_COMMIT_REF_NAME} --ignore-blank-lines -w -- ":(exclude)*.yml" ':(exclude)*.rst' ':(exclude)*.html'  ':(exclude)tests/*')

INSERTIONS=$(if [[ $MODIFICATIONS =~ "insertion" ]] ;then echo $MODIFICATIONS ; else echo ", 0 insertions"; fi | sed -E "s/.* ([0-9]+) insertion.*/\1/")

DELETIONS=$(if [[ $MODIFICATIONS =~ "deletion" ]] ;then echo $MODIFICATIONS ; else echo ", 0 deletions"; fi | sed -E "s/.* ([0-9]+) deletion.*/\1/")

TOTAL_LINES=$(($INSERTIONS + $DELETIONS))

echo "RULE # 3: Checking number of insertions and deletes..."
if (( $TOTAL_LINES > 500 ));
then
    echo "❌ You exceeded the insertions and deletes limit with $TOTAL_LINES lines!"
    exit 1
else
    echo "✅ $TOTAL_LINES lines"
fi

