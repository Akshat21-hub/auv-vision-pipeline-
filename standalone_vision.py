#!/usr/bin/env python3
import os
import cv2
import numpy as np

# ==========================================================
# IMPORTING THE EXACT DREADNOUGHT VISION LOGIC
# ==========================================================
from bp_vision.contour import _getFinalContours
from bp_vision.rect_fix import correct_rectangle_contour
from bp_vision.geometry import find_rectangle_corners

def main():
    print("🚀 Starting Dreadnought Standalone Vision Pipeline...")

    # File paths
    video_path = "bp_vision/test.MP4" 
    calib_path = "bp_vision/optimized_calib.npz"
    gate_real_width_meters = 1.5 
    
    # 1. Load Calibration
    is_calibrated = False
    camera_matrix = None
    dist_coeffs = None
    focal_length_px = 600.0

    if os.path.exists(calib_path):
        try:
            data = np.load(calib_path) 
            camera_matrix = data["mtx"]
            dist_coeffs = data["dist"]
            focal_length_px = camera_matrix[0, 0] 
            is_calibrated = True
            print(f"✅ Calibration loaded! Real focal length: {focal_length_px:.2f}px")
        except Exception as e:
            print(f"⚠️ Error loading calibration: {e}")
    else:
        print(f"⚠️ Calibration file not found at '{calib_path}'. Running uncalibrated.")

    # 2. Open Video
    cap = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
    
    if not cap.isOpened():
        print(f"❌ Failed to open video file: {video_path}")
        return
    else:
        print("✅ Video opened successfully! Press 'q' to quit.")

    # 3. Main Processing Loop
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("🎬 Video ended. Looping back to start...")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        if is_calibrated:
            frame = cv2.undistort(frame, camera_matrix, dist_coeffs, None, camera_matrix)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        gate_pixel_width = 0.0
        lateral_error_px = 0.0
        center_x, center_y = 0, 0

        # ==========================================================
        # EXECUTE YOUR VISION CHAIN
        # ==========================================================
        try:
            # Step 1: Get raw contours (handles split gates)
            final_contours = _getFinalContours(gray, frame, quality=255, viz=False)

            if final_contours and len(final_contours) > 0:
                
                # Step 2: Merge split contours and fix warped 90-degree corners
                corrected_rect_contour = correct_rectangle_contour(final_contours)
                
                if corrected_rect_contour is not None and len(corrected_rect_contour) > 0:
                    # Flatten the array for geometry processing
                    points = corrected_rect_contour.reshape(-1, 2)
                    
                    # Step 3: Extract exact corners
                    corners_dict = find_rectangle_corners(points)
                    
                    # Extract precise width using top corners
                    tl = corners_dict['top_left']
                    tr = corners_dict['top_right']
                    gate_pixel_width = float(np.linalg.norm(tr - tl))
                    
                    # Calculate center point for lateral error
                    center_x = int(np.mean([p[0] for p in points]))
                    center_y = int(np.mean([p[1] for p in points]))
                    
                    image_center_x = frame.shape[1] / 2.0
                    lateral_error_px = image_center_x - center_x

                    # --- Visualizations ---
                    # Draw the corrected 4-point polygon
                    cv2.polylines(frame, [corrected_rect_contour], isClosed=True, color=(0, 255, 0), thickness=2)
                    
                    # Draw corner markers
                    for name, pt in corners_dict.items():
                        cv2.circle(frame, (int(pt[0]), int(pt[1])), 5, (0, 0, 255), -1)
                    
                    # Draw center point
                    cv2.circle(frame, (center_x, center_y), 4, (255, 165, 0), -1)
                    
                    # Put text on screen
                    cv2.putText(frame, f"Width: {int(gate_pixel_width)}px", (int(tl[0]), int(tl[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    cv2.putText(frame, f"Lat Err: {lateral_error_px:.1f}px", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)

        except Exception as e:
            print(f"Vision processing bypassed: {e}")

        # Calculate Real-World Distance
        if gate_pixel_width > 0:
            distance = (focal_length_px * gate_real_width_meters) / gate_pixel_width
            cv2.putText(frame, f"Dist: {distance:.2f}m", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        # Show the frame
        cv2.imshow("Dreadnought Standalone Vision Test", frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            print("🛑 Exiting video test...")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
