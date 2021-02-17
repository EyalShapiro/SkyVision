import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt

def hstack_images(image1,image2): # put image right of another image
    return np.hstack((image1, image2))

def hstack_array(images): # put all images to the right of each other
    stack = images[0]
    for image in images[1:]:
        stack = hstack_images(stack,image)
    return stack

def find_images(width,height):

    found = 0

    # take image from camera and convert to gray to use in processing
    right = cv2.VideoCapture(1)
    left = cv2.VideoCapture(0)
    rret, _ = right.read()
    lret, _ = left.read()

    if not rret:
        print("Could not read right camera!")
        exit()

    if not lret:
        print("Could not read left camera!")
        exit()

    while(True):
        _, rframe = right.read()
        _, rimg = right.read()

        rframe = cv2.flip(rframe,0)
        rimg = cv2.flip(rimg,0)

        _, lframe = left.read()
        _, limg = left.read()

        lframe = cv2.flip(lframe,0)
        limg = cv2.flip(limg,0)

        rgray = cv2.cvtColor(rimg,cv2.COLOR_BGR2GRAY)
        lgray = cv2.cvtColor(limg,cv2.COLOR_BGR2GRAY)

        # find corners
        rret, rcorners = cv2.findChessboardCorners(rgray,(height,width))
        lret, lcorners = cv2.findChessboardCorners(lgray,(height,width))

        # if found corners, add points ( after refining )
        if rret:
            # Draw and display the corners
            cv2.drawChessboardCorners(rimg, (height,width), rcorners,rret)
        
        if lret:

            # Draw and display the corners
            cv2.drawChessboardCorners(limg, (height,width), lcorners,lret)
        
        if lret and rret and cv2.waitKey(1) == ord('p'):
            found+= 1
            cv2.imwrite('temporary/calibration_images/r/' + str(found) + '.jpg', rframe)
            cv2.imwrite('temporary/calibration_images/l/' + str(found) + '.jpg', lframe)
            print("Written -",found)

        cv2.imshow('rimg', rimg)
        cv2.imshow('limg', limg)
        if(cv2.waitKey(1) == ord('q')):
            break

def calibrate(width,height,path = 'temporary/calibration_images/*.jpg',savepath = 'temporary',amount = 50):    
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    width = width - 1
    height = height - 1

    objp = np.zeros((width*height,3), np.float32)
    objp[:,:2] = np.mgrid[0:height,0:width].T.reshape(-1,2)


    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    
    images = sorted(glob.glob(path))

    counter = 0

    for imgname in images:
        if counter >= amount:
            break
        try:
            img = cv2.imread(imgname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (height,width), None)
            
            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
                imgpoints.append(corners)

                # Draw and display the corners
                cv2.drawChessboardCorners(img, (height,width), corners2, ret)

                counter += 1
                

                #cv2.imshow('img', img)
                #cv2.waitKey(1)
        except:
            pass

    print("FOUND -",counter)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    print("DONE CALIBRATING")
    np.savez(savepath + "/calibration.npz",ret = ret,mtx = mtx,dist = dist,rvecs = rvecs,tvecs = tvecs,objpoints = objpoints,imgpoints = imgpoints)
    print("SAVED")
    return ret,mtx,dist,rvecs,tvecs,objpoints,imgpoints

def undistort(img,mtx,dist,rvecs,tvecs):
    h,w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h)) # refine camera matrix

    #undistort
    dst = cv2.undistort(img,mtx,dist,None,newcameramtx)

    #crop
    x,y,w,h = roi
    dst = dst[y:y+h,x:x+w]

    #show
    return dst


def drawlines(img1src, img2src, lines, pts1src, pts2src): # Visualize epilines
    ''' img1 - image on which we draw the epilines for the points in img2
        lines - corresponding epilines '''
    r, c = img1src.shape
    img1color = cv2.cvtColor(img1src, cv2.COLOR_GRAY2BGR)
    img2color = cv2.cvtColor(img2src, cv2.COLOR_GRAY2BGR)
    # Edit: use the same random seed so that two images are comparable!
    np.random.seed(0)
    for r, pt1, pt2 in zip(lines, pts1src, pts2src):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int, [0, -r[2]/r[1]])
        x1, y1 = map(int, [c, -(r[2]+r[0]*c)/r[1]])
        img1color = cv2.line(img1color, (x0, y0), (x1, y1), color, 1)
        img1color = cv2.circle(img1color, tuple(pt1), 5, color, -1)
        img2color = cv2.circle(img2color, tuple(pt2), 5, color, -1)
    return img1color, img2color

def crop(img,cropWidth,cropHeight):
    height = imgL_rectified.shape[0]
    width = imgL_rectified.shape[1]

    centerY = int(height/2)
    centerX = int(width/2)

    return img[centerY-int(cropHeight/2):centerY+int(cropHeight/2),centerX-int(cropWidth/2):centerX+int(cropWidth/2)]

# find_images(6,9) # to create images for calibration


# print("Calibrating Right")
# calibrate(7,10,'temporary/calibration_images/r/*.jpg',amount=20,savepath="temporary/calibration_images/r") # only to find calibration params
# print("Calibrating Left")
# calibrate(7,10,'temporary/calibration_images/l/*.jpg',amount=20,savepath="temporary/calibration_images/l") # only to find calibration params
# print("Done calibrating")



R_loaded = np.load("temporary/R_Calibration.npz") # load calibration file
L_loaded = np.load("temporary/L_Calibration.npz") # load calibration file

R_ret = R_loaded["ret"]
R_mtx = R_loaded["mtx"]
R_dist = R_loaded["dist"]
R_rvecs = R_loaded["rvecs"]
R_tvecs = R_loaded["tvecs"]
R_objpoints = R_loaded["objpoints"]
R_imgpoints = R_loaded["imgpoints"]

imgR = cv2.imread('temporary/calibration_images/r/1.jpg')
# imgR = cv2.imread('temporary/tsukuba 2.png')

L_ret = L_loaded["ret"]
L_mtx = L_loaded["mtx"]
L_dist = L_loaded["dist"]
L_rvecs = L_loaded["rvecs"]
L_tvecs = L_loaded["tvecs"]
L_objpoints = L_loaded["objpoints"]
L_imgpoints = L_loaded["imgpoints"]

imgL = cv2.imread('temporary/calibration_images/l/1.jpg')
# imgL = cv2.imread('temporary/tsukuba 1.png')

imgL = undistort(imgL,L_mtx,L_dist,L_rvecs,L_tvecs)
imgL = cv2.cvtColor(imgL,cv2.COLOR_BGR2GRAY)
imgR = undistort(imgR,R_mtx,R_dist,R_rvecs,R_tvecs)
imgR = cv2.cvtColor(imgR,cv2.COLOR_BGR2GRAY)

width = imgL.shape[0]
height = imgL.shape[1]

cv2.imshow("L",imgL)
cv2.imshow("R",imgR)
cv2.waitKey(0)

if(R_ret and L_ret):
    # if(False):



    # Initiate SIFT detector
    sift = cv2.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(imgL, None)
    kp2, des2 = sift.detectAndCompute(imgR, None)

    # Match keypoints in both images
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # Keep good matches: calculate distinctive image features
    matchesMask = [[0, 0] for i in range(len(matches))]
    good = []
    pts1 = []
    pts2 = []

    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            # Keep this keypoint pair
            matchesMask[i] = [1, 0]
            good.append(m)
            pts2.append(kp2[m.trainIdx].pt)
            pts1.append(kp1[m.queryIdx].pt)

    samples = 50

    # Draw the keypoint matches between both pictures
    draw_params = dict(matchColor=(0, 255, 0),
                    singlePointColor=(255, 0, 0),
                    matchesMask=matchesMask[500-samples:500],
                    flags=cv2.DrawMatchesFlags_DEFAULT)

    # ------------------------------------------------------------
    # STEREO RECTIFICATION

    # Calculate the fundamental matrix for the cameras
    pts1 = np.int32(pts1)
    pts2 = np.int32(pts2)
    fundamental_matrix, inliers = cv2.findFundamentalMat(pts1, pts2, cv2.FM_RANSAC)

    # We select only inlier points
    pts1 = pts1[inliers.ravel() == 1]
    pts2 = pts2[inliers.ravel() == 1]

    # Find epilines corresponding to points in right image (second image) and
    # drawing its lines on left image
    lines1 = cv2.computeCorrespondEpilines(pts2.reshape(-1, 1, 2), 2, fundamental_matrix)
    lines1 = lines1.reshape(-1, 3)
    img5, img6 = drawlines(imgL, imgR, lines1, pts1, pts2)

    # Find epilines corresponding to points in left image (first image) and
    # drawing its lines on right image
    lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1, 1, 2), 1, fundamental_matrix)
    lines2 = lines2.reshape(-1, 3)
    img3, img4 = drawlines(imgR, imgL, lines2, pts2, pts1)

        
    # Stereo rectification (uncalibrated variant)
    h1, w1 = imgL.shape
    h2, w2 = imgR.shape
    _, H1, H2 = cv2.stereoRectifyUncalibrated(np.float32(pts1), np.float32(pts2), fundamental_matrix, imgSize=(w1, h1))

    # Undistort (rectify) the images and save them
    imgL_rectified = cv2.warpPerspective(imgL, H1, (w1, h1))
    imgR_rectified = cv2.warpPerspective(imgR, H2, (w2, h2))
    cv2.imshow("rectified_1.png", imgL_rectified)
    # cv2.imshow("rectified_2.png", imgR_rectified)
    # cv2.waitKey(0)

    # ------------------------------------------------------------
    # CALCULATE DISPARITY (DEPTH MAP)

    # Matched block size. It must be an odd number >=1 . Normally, it should be somewhere in the 3..11 range.
    block_size = 11
    min_disp = -128
    max_disp = 128
    # Maximum disparity minus minimum disparity. The value is always greater than zero.
    # In the current implementation, this parameter must be divisible by 16.
    num_disp = max_disp - min_disp
    # Margin in percentage by which the best (minimum) computed cost function value should "win" the second best value to consider the found match correct.
    # Normally, a value within the 5-15 range is good enough
    uniquenessRatio = 5
    # Maximum size of smooth disparity regions to consider their noise speckles and invalidate.
    # Set it to 0 to disable speckle filtering. Otherwise, set it somewhere in the 50-200 range.
    speckleWindowSize = 200
    # Maximum disparity variation within each connected component.
    # If you do speckle filtering, set the parameter to a positive value, it will be implicitly multiplied by 16.
    # Normally, 1 or 2 is good enough.
    speckleRange = 2
    disp12MaxDiff = 0

    stereo = cv2.StereoSGBM_create(
        minDisparity=min_disp,
        numDisparities=num_disp,
        blockSize=block_size,
        uniquenessRatio=uniquenessRatio,
        speckleWindowSize=speckleWindowSize,
        speckleRange=speckleRange,
        disp12MaxDiff=disp12MaxDiff,
        P1=8 * 1 * block_size * block_size,
        P2=32 * 1 * block_size * block_size,
    )

    imgL_rectified = crop(imgL_rectified,500,300)
    imgR_rectified = crop(imgR_rectified,500,300)

    print(imgR_rectified.shape[1])

    disparity_SGBM = stereo.compute(imgL_rectified, imgR_rectified)

    # Normalize the values to a range from 0..255 for a grayscale image
    disparity_SGBM = cv2.normalize(disparity_SGBM, disparity_SGBM, alpha=255,beta=0, norm_type=cv2.NORM_MINMAX)
    disparity_SGBM = np.uint8(disparity_SGBM)
    cv2.imshow("Disparity", disparity_SGBM)

    white = np.zeros([300,500,1],dtype=np.uint8)
    white.fill(255) # or img[:] = 255

    hsv = cv2.merge((disparity_SGBM,white,white))
    color_disp = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

    cv2.imshow('color_disp',color_disp)
    cv2.waitKey(0)