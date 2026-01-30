@echo off
setlocal enabledelayedexpansion

:: --- Argument Parsing ---
set "MSG="
set "NOPUSH=0"
set "CHECK_ONLY=0"
set "SHOW_HELP=0"

:parse
if "%~1"=="" goto endparse
set "PARAM=%~1"
set "VAL=%~2"

if /i "!PARAM!"=="--help"   set "SHOW_HELP=1" & shift & goto parse
if /i "!PARAM!"=="-h"       set "SHOW_HELP=1" & shift & goto parse
if /i "!PARAM!"=="--check"  set "CHECK_ONLY=1" & shift & goto parse
if /i "!PARAM!"=="--nopush" set "NOPUSH=1" & shift & goto parse
if /i "!PARAM!"=="-m" (
    :: Safety check: is the next arg a message or another flag?
    if "!VAL!"=="" (
        set "MSG="
    ) else (
        set "FIRST_CHAR=!VAL:~0,1!"
        if "!FIRST_CHAR!"=="-" (
            echo Warning: -m expects a message, but found "!VAL!". Prompting later...
            set "MSG="
        ) else (
            set "MSG=!VAL!"
            shift
        )
    )
    shift
    goto parse
)
shift
goto parse
:endparse

:: --- Help ---
if "%SHOW_HELP%"=="1" (
    echo BlueGemini Automation Script (do.bat^)
    echo -------------------------------------
    echo Usage:
    echo   do [options]
    echo.
    echo Options:
    echo   --check       Update README index and print it (No Git operations^)
    echo   --nopush      Commit changes but do not push; shows commit diff
    echo   -m "msg"      Specify commit message (optional^)
    echo   --help        Show this brief help message
    echo.
    echo Examples:
    echo   do --nopush -m "Fix bug"
    echo   do -m "New feature" --check
    exit /b 0
)

:: --- 1. Index Generation ---
echo [-] Parameters: CHECK=%CHECK_ONLY%, NOPUSH=%NOPUSH%, MSG=!MSG!
echo [-] Scanning and updating README index...
python .gemini\scripts\generate_root_index.py
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python index script failed.
    exit /b 1
)
echo     README.md updated successfully.

echo [-] Generating Knowledge Base JSON index...
python .gemini\scripts\generate_kb_index.py
if %ERRORLEVEL% NEQ 0 (
    echo Error: Knowledge Base JSON index generation failed.
    exit /b 1
)
echo     Knowledge_Base/index.json updated successfully.

:: --- 2. Check Mode Exit ---
if "%CHECK_ONLY%"=="1" (
    echo.
    echo [v] Check mode: Displaying updated README.md...
    echo ---------------------------------------------------
    type README.md
    echo ---------------------------------------------------
    echo [v] Check mode complete. No git operations performed.
    exit /b 0
)

:: --- 3. Git Status & Review ---
echo.
echo [-] Checking Git status...
git status -s

:: Check if there are changes
for /f "tokens=*" %%i in ('git status --porcelain') do set "GIT_CHANGES=%%i"
if "!GIT_CHANGES!"=="" (
    echo.
    echo [v] No changes to commit. Working tree clean.
    exit /b 0
)

echo.
echo [-] Pending Changes Summary:
git diff --name-status

:: --- 4. User Confirmation ---
echo.
set /p "CONFIRM=Do you want to stage ALL changes, commit and push? (y/n): "
if /i "!CONFIRM!" NEQ "y" (
    echo Operation cancelled by user.
    exit /b 0
)

:: --- 5. Git Execution ---
echo [-] Staging all files (git add .)...
git add .
if %ERRORLEVEL% NEQ 0 (
    echo Error: Git add failed.
    exit /b 1
)

if "!MSG!"=="" (
    set /p "MSG=Enter commit message (Default: 'Update knowledge base'): "
)
if "!MSG!"=="" set "MSG=Update knowledge base"

echo [-] Committing (git commit -m "!MSG!")...
git commit -m "!MSG!"
if %ERRORLEVEL% NEQ 0 (
    echo Error: Git commit failed.
    exit /b 1
)

if "%NOPUSH%"=="1" (
    echo [-] Skipping push (--nopush^).
    echo.
    echo [v] Commit File List:
    echo ---------------------------------------------------
    git show --name-only --format="Commit: %%h %%s" HEAD | powershell -NoProfile -Command "$input | Select-Object -First 20"
    echo ---------------------------------------------------
) else (
    echo [-] Pushing to remote (git push^)...
    git push
    if %ERRORLEVEL% NEQ 0 (
        echo Error: Git push failed.
        exit /b 1
    ) else (
        echo [v] Push successful.
    )
)

echo.
echo [v] Workflow completed.
exit /b 0
