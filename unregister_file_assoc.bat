@echo off
chcp 65001 >nul 2>&1
echo ============================================
echo   HTML 演示放映器 - 取消文件关联
echo ============================================
echo.

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [错误] 需要管理员权限！
    echo 请右键本文件，选择"以管理员身份运行"
    echo.
    pause
    exit /b 1
)

echo 正在删除 .slidehtml 文件关联...

reg delete "HKCR\.slidehtml" /f >nul 2>&1
reg delete "HKCR\SlideHTMLFile" /f >nul 2>&1

if %errorLevel% equ 0 (
    echo.
    echo 文件关联已取消。
) else (
    echo.
    echo 操作完成（可能之前未注册）。
)

echo.
pause
