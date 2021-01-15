@set temp_dir=D:\temp\env
@set temp_file=%temp_dir%\env_%random%.bat
@python %~dp0init.py %* %temp_file%
@IF EXIST %temp_file% (call %temp_file%) ELSE (echo %temp_file% does not exists ...)
@set temp_dir=
@set temp_file=