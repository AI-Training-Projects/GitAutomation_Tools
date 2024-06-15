@echo off

REM List of local repo directories
set "repos[0]=C:\Users\PowerUser\Documents\Github_Repos_RSL\Ask_My_PDF"
set "repos[1]=C:\Users\PowerUser\Documents\Github_Repos_RSL\Ask_Multiple_PDFs"
set "repos[2]=C:\Users\PowerUser\Documents\Github_Repos_RSL\Streamlit_Cancer_Prediction"
REM Add more repo directories if needed

REM Loop through the repos
for %%i in (0 1 2) do (
    REM Change to the repo directory
    cd /d "%repos[%%i]%" || exit /b

    REM Commit and push
    git add .
    git commit -m "Automated initial commit"
    git push

    REM Optional: Verify the push was successful
    REM git status

    echo Processed repo: %repos[%%i]%
)
