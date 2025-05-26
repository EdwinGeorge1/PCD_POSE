#!/usr/bin/env python3
import open3d as o3d
import numpy as np
from scipy.spatial.transform import Rotation as R

# Load the point cloud
pcd = o3d.io.read_point_cloud("cup.pcd")
pcd.estimate_normals()

# Compute oriented bounding box (OBB)
obb = pcd.get_oriented_bounding_box()

# Get position (center of OBB)
position = obb.center

# Get orientation (rotation matrix from OBB)
rotation_matrix = obb.R

# Convert rotation matrix to RPY (Euler angles)
rpy = R.from_matrix(rotation_matrix).as_euler('xyz', degrees=True)

# Print pose information
print("Estimated Pose of the Cup:")
print(f"Position: x={position[0]:.3f}, y={position[1]:.3f}, z={position[2]:.3f}")
print(f"Orientation (RPY degrees): roll={rpy[0]:.2f}, pitch={rpy[1]:.2f}, yaw={rpy[2]:.2f}")

# Create coordinate frame at estimated pose
frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=10.0)
frame.translate(position)
frame.rotate(rotation_matrix, center=position)

# Convert OBB to red LineSet for visualization
obb_lines = o3d.geometry.LineSet.create_from_oriented_bounding_box(obb)
obb_lines.paint_uniform_color([1.0, 0.0, 0.0])  # red

# Visualize
o3d.visualization.draw_geometries([pcd, obb_lines, frame])
