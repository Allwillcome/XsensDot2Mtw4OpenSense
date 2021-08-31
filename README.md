**This document contains both English and 中文 descriptions**

The purpose of this code is to convert Xsens Dot data into Xsens MVN data, and then into OpenSim readable data for human body modeling
The data output by Xsens MVN includes: meter header, time stamp, acceleration data, rotation matrix, UT Time and other data without specific values
The output of Xsens Dot is only meter head, free acceleration, quaternion or Euler angle.Therefore, it is necessary to convert the quaternion in Xsens Dot into a rotation matrix, convert the header of the acceleration data, and supplement information such as UT Time

The following will show the data and differences between Xsens Dot and Xsens MVN, and finally perform the corresponding conversion
- Original_XsensDot_Data                The original data of the data exported by Xsens Dot
- OpenSenseExampleIMUData               The data in the OpenSenseExampleIMUData folder is the IMU data officially provided by OpenSim, which is exported using Xsens MVN software
- Transformed_XsensDot_Data             Which is the data converted by Xsens Dot

**Note:**

This document is only suitable for converting the real-time data collected by Xsens Dot into a form acceptable to OpenSense.

If you need to convert the data collected by Xsens Dot offline into a form acceptable to OpenSense, you need to convert Euler angles into a rotation matrix.

## 中文说明
本代码的目的是将 Xsens Dot 的数据转换成 Xsens MVN 数据，进而转换成 OpenSim 可读的数据，进行人体建模
Xsens MVN 输出的数据包含：表头、时间戳、加速度数据、旋转矩阵以及UT Time 等不含具体数值的数据
而 Xsens Dot 输出的只有表头、自由加速度、四元数或者欧拉角。
因此，需要将 Xsens Dot 中的四元数转换为旋转矩阵，将加速度数据的表头进行转换，补充 UT Time 等信息
下面将展示下 Xsens Dot 和 Xsens MVN 的数据以及差异，最后进行对应的转换
- Original_XsensDot_Data                      Xsens Dot 导出的数据原始数据
- OpenSenseExampleIMUData  文件夹内数据为      OpenSim 官方提供的 IMU 数据，使用 Xsens MVN 软件导出
- Transformed_XsensDot_Data                   为 Xsens Dot 转换后的数据

**注意：**
本文档只适合将 Xsens Dot 实时采集的数据转换为 OpenSense 可以接受的形式。
如果需要将 Xsens Dot 离线采集的数据转换为 OpenSense 可以接受的形式，需要将 欧拉角转换成旋转矩阵。

