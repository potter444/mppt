::Э���ļ�·��, ���Ҫ����\������
set SOURCE_FOLDER=F:\20210226\projects\server\proto
::����ļ��������˱��proto�ļ���IMP_FOLDER�����õ�proto�ļ���Ŀ¼
set IMP_FOLDER=F:\20210226\projects\server\proto
::python������·��
set PY_COMPILER_PATH=C:\python36.4\protoc.exe
::python�ļ�����·��, ���Ҫ����\������
set PY_TARGET_PATH=F:\20210226\projects\server\proto_py
::ɾ��֮ǰ�������ļ�
del %PY_TARGET_PATH%\*.* /f /s /q


::���������ļ�
for /f "delims=" %%i in ('dir /b "%SOURCE_FOLDER%\*.proto"') do (
    
    echo %PY_COMPILER_PATH% -I=%SOURCE_FOLDER%  --python_out=%PY_TARGET_PATH% %SOURCE_FOLDER%\%%i
    %PY_COMPILER_PATH% -I=%IMP_FOLDER%  --python_out=%PY_TARGET_PATH% %SOURCE_FOLDER%\%%i
    
)
pause