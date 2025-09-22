
from camera3D import Camera_3D
from face_detection import Roba_Faces_recognition

roba_cam = Camera_3D()

#roba_face_rec = Roba_Faces_recognition()

#roba_cam.display_all()
br=0
depimg=[]
colorimg=[]
while True:

    img,ver =roba_cam.get_2d_img_get_defth_xyz_len(roba_cam.xy[0],roba_cam.xy[1])
    depimg=ver
    colorimg=ver
    roba_cam.display_all_set_p(img,ver)
    if roba_cam.break_loop :
        break

try:
    roba_cam.clean_cam()
except:
    print(ver)
