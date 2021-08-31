# 要添加一个新单元，输入 '# %%'
# 要添加一个新的标记单元，输入 '# %% [markdown]'
# %%
"""
The purpose of this code is to convert Xsens Dot data into Xsens MVN data, 
and then into OpenSim readable data for human modeling Xsens MVN output data includes: header timestamp acceleration data rotation matrix and UT Time Xsens Dot outputs only the quaternion of the free acceleration of the header or euler Angle. Therefore, it is necessary to convert the quaternion in Xsens Dot to the rotation matrix, and convert the header of the acceleration data to supplement UT Time and other information.
Xsens will be shown below Dot and Xsens MVN data and differences, and finally the corresponding transformation
"""

# %% [markdown]
# 
# - csv 文件                                    Xsens Dot 导出的数据$$
# - OpenSenseExampleIMUData  文件夹内数据为      OpenSim 官方提供的 IMU 数据，使用 Xsens MVN 软件导出
# - Transformed_XsensDot_Data                   为 Xsens Dot 转换后的数据，不包含表头

# %%
# Import the related software package 导入相关的软件包
import os               #Performing system operations 进行系统操作
import re               #To Extract the IMU ID from the file name 提取文件名中 IMU ID
import numpy as np      #Perform operations 进行运算操作
import pandas as pd     #Excel data reading and writing 进行 Excel 数据的读写
from scipy.spatial.transform import Rotation as R #Converts quaternions to Euler angles 将四元数转换成欧拉角


# %%
#Show current directory 展示当前目录
path_cwd = os.getcwd()
print("The current path is：", path_cwd)
#Show Xsens MVN data, namely OpenSense IMU data 展示 Xsens MVN 数据，即 OpenSense IMU 数据
pd.set_option("display.max_columns",None)
file_Example = r"MT_012005D6_009-001_00B421E6.txt" 
path_xsens_dot = os.path.join(path_cwd, "OpenSenseExampleIMUData",file_Example)
df = pd.read_csv(path_xsens_dot)
print("The table header data is😎：")
print(df.head(7))
OpenSenseExampleIMUData_df = pd.read_csv(path_xsens_dot,skiprows=5,sep="\t")
print("Xsens MVN data is💫:")
OpenSenseExampleIMUData_df.head()


# %%
def transformed_Xsens_dot_data_Offline(filename): 
       regex = r"(.*)_.*_(.*_).*.csv"
       mysearch = re.search(regex,filename)
       IMU_ID =  mysearch.group(1) 
       prefix_IMU = mysearch.group(2)
       new_filename = "XSDot" + "_" + prefix_IMU + IMU_ID + ".txt"
       path_new_filename = os.path.join(path_new_file, new_filename)
       
       #Read File 读取文件
       df = pd.read_csv(filename,skiprows=6)                  
       df_euler = df[["Euler_X","Euler_Y","Euler_Z"]]                  #Select the column in which euler Angle is located 选择欧拉角所在的列

       #Make a quaternion conversion 进行四元数的转换
       r = R.from_euler("xyz",df_euler,degrees=True)           #Initialize a quaternion 初始化四元数
       matrix = r.as_matrix()                                  #Converts a quaternion to a rotation matrix 将四元数转换为旋转矩阵
       (matrix_rows,b,c) = matrix.shape                        #The rotation matrix is (n,3,3) and there is no way to convert to Datafram 旋转矩阵是（n,3,3)没有办法转换为 Datafram
       matrix_reshpae = matrix.reshape(matrix_rows,9)          #Convert to n rows and 9 columns of data 转换为 n 行 9 列的数据
       
       #Write the converted data to Excel 将转换好的数据写入到 Excel 当中
       header_list = ["Mat[1][1]","Mat[1][2]","Mat[1][3]",
                     "Mat[2][1]","Mat[2][2]","Mat[2][3]",
                     "Mat[3][1]","Mat[3][2]","Mat[3][3]"]     #According to the results of Xsens rotation matrix, the corresponding columns are assigned table headers 对照 Xsens 旋转矩阵结果，为对应列赋予表头
       df_matrix = pd.DataFrame(matrix_reshpae,columns=header_list)
       
       #Align the Xsens MVN built with Dot data 将 Dot 数据构建的 Xsens MVN 一致
       PacketCounter = df['PacketCounter'] 
       SampleTimeFine = df["SampleTimeFine"]
       Acc = df[["Acc_X","Acc_Y","Acc_Z"]]                     #the difference of offline and realtime
       Acc.columns = ["Acc_X","Acc_Y","Acc_Z"]                 #Name the free acceleration acceleration, keeping the same format as the Xsens MVN data将自由加速度命名为加速度，保持和 Xsens MVN 数据格式相同
       Year = [] 
       Month = []
       Day = []
       Second = []
       UTC_Nano = []
       UTC_Year = []
       UTC_Month = []
       UTC_Day = []
       UTC_Hour = []
       UTC_Minute = []
       UTC_Second = []
       UTC_Valid = []
       df_othercolumns = pd.DataFrame({'Year':Year, 'Month':Month, 'Day':Day, 'Second':Second,
              'UTC_Nano':UTC_Nano, 'UTC_Year':UTC_Year, 'UTC_Month':UTC_Month, 'UTC_Day':UTC_Day, 'UTC_Hour':UTC_Hour,
              'UTC_Minute':UTC_Minute, 'UTC_Second':UTC_Second, 'UTC_Valid':UTC_Valid})

       #The structure of the splice transformation 拼接转换的结构
       frame = [PacketCounter,SampleTimeFine,df_othercolumns,Acc,df_matrix]
       transformed_df = pd.concat(frame,axis=1)                              #Splice multiple Dataframs horizontally axis=1 横向拼接多个 DataFram
       transformed_df.to_csv(path_new_filename,
                            index=False,sep="\t",float_format='%.6f') 

       with open(path_new_filename,"r+") as f:
           content = f.read()
           f.seek(0,0)
           f.write("// Start Time: Unknown\n// Update Rate: 100.0Hz\n//Filter Profile: human (46.1)\n// Option Flags: AHS Disabled ICC Disabled\n// Firmware Version: 4.0.2\n"+content)
       print(new_filename,",Done😎")                                      #报告转换完成的文件


# %%
new_file = "Transformed_XsensDot_Data_Offline"
path_new_file = os.path.join(path_cwd,new_file)

os.chdir(path_cwd)
path_original_Xsens_dot = os.chdir(".\\Original_XsensDot_Data_Offline")
print(os.getcwd())
for file in os.listdir():
    #Filter out all.csv files to avoid folder processing; otherwise, the system will report errors
    #筛选出所有的 .csv 文件，避免对文件夹进行处理，否则系统会报错
    if ".csv" in file: 
        transformed_Xsens_dot_data_Offline(file)
print("🎃All Xsens Dot original files have been converted")


