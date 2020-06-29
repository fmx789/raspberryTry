



Structure

faceRecognition/

|——clientnew.py(人脸识别及socket通信client端)

new/

|——mfrc522(RFID辅助函数)

​			|——MFRC522.py

​			|——SimpleMFRC522.py

|——tem(测温函数)

​			|——HDC1080.py

​			|——testHDC1080.py

|——cam.py（摄像头自启动脚本）

|——LED.py（LED控制函数）

|——modifykey.py（RFID卡写入key用于区分用户权限）

|——read.py（RFID读卡）

|——server.py（主程序，完成socket通信server端及硬件信息采集、上报，控制执行器）

|——stu_management1.py（硬件上报API函数）

|——write.py（RFID写卡）