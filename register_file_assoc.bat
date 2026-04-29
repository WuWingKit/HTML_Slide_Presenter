@echo off
chcp 65001 >nul 2>&1
echo ============================================
echo   HTML 演示放映器 - 文件关联注册工具
echo ============================================
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [错误] 需要管理员权限！
    echo 请右键本文件，选择"以管理员身份运行"
    echo.
    pause
    exit /b 1
)

:: 获取 Python 路径和脚本路径
for /f "delims=" %%i in ('where python') do set "PYTHON_PATH=%%i"
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_PATH=%SCRIPT_DIR%player.py"

:: 检查播放器是否存在
if not exist "%SCRIPT_PATH%" (
    echo [错误] 找不到播放器: %SCRIPT_PATH%
    echo 请确保本文件和 player.py 在同一目录
    echo.
    pause
    exit /b 1
)

echo Python: %PYTHON_PATH%
echo 脚本:   %SCRIPT_PATH%
echo.

:: 写入注册表
echo 正在注册 .slidehtml 文件关联...

:: 文件扩展名关联
reg add "HKCR\.slidehtml" /ve /d "SlideHTMLFile" /f >nul 2>&1

:: 文件类型描述
reg add "HKCR\SlideHTMLFile" /ve /d "HTML 幻灯片" /f >nul 2>&1

:: 文件图标（使用 Python 图标）
reg add "HKCR\SlideHTMLFile\DefaultIcon" /ve /d "%PYTHON_PATH%,0" /f >nul 2>&1

:: 打开命令
reg add "HKCR\SlideHTMLFile\shell\open\command" /ve /d "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\" \"%%1\"" /f >nul 2>&1

if %errorLevel% equ 0 (
    echo.
    echo ============================================
    echo   注册成功！
    echo ============================================
    echo.
    echo 现在可以双击 .slidehtml 文件直接打开放映器
    echo.
    echo 如需取消关联，请运行"unregister_file_assoc.bat"
) else (
    echo.
    echo [错误] 注册表写入失败，请检查权限
)

echo.
pause
