import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# import cv2
# from ultralytics import solutions
# import cx_Oracle  # 用于 Oracle 数据库连接
#
# # Open video file
# cap = cv2.VideoCapture(r"D:\py_xiangm\学生行为\测试视频2.mp4")
# assert cap.isOpened(), "Error reading video file"
# w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
#
# # Define region points
# region_points = {
#     "region-01": [(0, 0), (950, 0), (950, 500), (0, 500)]
# }
#
# # Video writer
# video_writer = cv2.VideoWriter("region_counting.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
#
# # DB config (remove this if not using database)
# db_config = {
#     'user': 'C##YUANWEIHUA',
#     'password': 'root',
#     'dsn': 'localhost:1521/XE',  # 确保 DSN 格式正确
#     'encoding': 'UTF-8'
# }
#
# # Database connection test
# def test_db_connection():
#     try:
#         conn = cx_Oracle.connect(**db_config)
#         print("Database connected successfully!")
#         conn.close()  # 关闭连接
#     except cx_Oracle.DatabaseError as e:
#         print(f"Error connecting to Oracle database: {e}")
#
# test_db_connection()
#
# # Initialize RegionCounter
# region = solutions.RegionCounter(
#     show=True,
#     region=region_points,
#     model=r"D:\py_xiangm\学生行为\runs\detect\train6\weights\best.pt",
#     iou=0.3,
#     device='cuda',  #启用 GPU
#     db_config=db_config,  # Pass db_config if you are using database
# )
#
# # Process video
# while cap.isOpened():
#     success, im0 = cap.read()
#     if not success:
#         print("Video frame is empty or video processing has been successfully completed.")
#         break
#     im0 = region.count(im0)
#     video_writer.write(im0)
#
# cap.release()
# video_writer.release()
# cv2.destroyAllWindows()
#
# # Ensure database connection is closed properly
# if hasattr(region, 'close'):  # 如果 RegionCounter 类有 close 方法
#     region.close()
#
# print("Video processing completed.")


import cv2
from ultralytics import solutions
from DatabaseConnector import DatabaseConnector
# 初始化视频流
cap = cv2.VideoCapture(r"D:\py_xiangm\学生行为\测试视频2.mp4")
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# 定义区域点
region_points = {
    "region-01": [(0, 0), (950, 0), (950, 500), (0, 500)]  # Example region
}

# 视频写入器
video_writer = cv2.VideoWriter("region_counting.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# 创建数据库连接
db_connector = DatabaseConnector(
    host="localhost",  # 数据库主机
    user="C##YUANWEIHUA",     # 用户名
    password="root",   # 密码
    database="XE"      # 数据库名
)

# 初始化 RegionCounter
region = solutions.RegionCounter(
    db_connector=db_connector,  # 将数据库连接传递给 RegionCounter
    show=True,
    region=region_points,
    model=r"D:\py_xiangm\学生行为\runs\detect\train6\weights\best.pt",
    iou=0.3,
    device='cuda'  # 启用 GPU
)

# 处理视频
while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("视频帧为空或视频处理已完成.")
        break
    im0 = region.count(im0)  # 计数并处理图像
    video_writer.write(im0)  # 写入视频

cap.release()
video_writer.release()
cv2.destroyAllWindows()

# 关闭数据库连接
db_connector.close()
