::协议文件路径, 最后不要跟“\”符号
set SOURCE_FOLDER=F:\20210226\projects\server\proto
::如果文件中引用了别的proto文件，IMP_FOLDER是引用的proto文件的目录
set IMP_FOLDER=F:\20210226\projects\server\proto
::python编译器路径
set PY_COMPILER_PATH=C:\python36.4\protoc.exe
::python文件生成路径, 最后不要跟“\”符号
set PY_TARGET_PATH=F:\20210226\projects\server\proto_py
::删除之前创建的文件
del %PY_TARGET_PATH%\*.* /f /s /q


::遍历所有文件
for /f "delims=" %%i in ('dir /b "%SOURCE_FOLDER%\*.proto"') do (
    
    echo %PY_COMPILER_PATH% -I=%SOURCE_FOLDER%  --python_out=%PY_TARGET_PATH% %SOURCE_FOLDER%\%%i
    %PY_COMPILER_PATH% -I=%IMP_FOLDER%  --python_out=%PY_TARGET_PATH% %SOURCE_FOLDER%\%%i
    
)
pause