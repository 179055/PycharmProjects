import cv2

from ultralytics import solutions

cap = cv2.VideoCapture(r"D:\py_xiangm\学生行为\测试视频2.mp4")
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# 定义区域点
region_points = [(210, 530), (400, 280)]


video_writer = cv2.VideoWriter("object_counting_output.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))


counter = solutions.ObjectCounter(
    show=True,  # 显示输出
    region=region_points, # 传递区域积分
    model=r"D:\py_xiangm\学生行为\runs\detect\train6\weights\best.pt", # 模型路径
    line_width=1
    # device='cuda'  # 启用 GPU
)


while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("视频帧为空或视频处理已成功完成.")
        break
    im0 = counter.count(im0)
    video_writer.write(im0)

cap.release()
video_writer.release()
cv2.destroyAllWindows()