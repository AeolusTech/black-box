from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
import bmp280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus


class IMU:
    keeprunning = True

    def __init__(self):
        self.mpu = MPU9250(
            address_ak=AK8963_ADDRESS,
            address_mpu_master=MPU9050_ADDRESS_68,  # In 0x68 Address
            address_mpu_slave=None,
            bus=1,
            gfs=GFS_1000,
            afs=AFS_8G,
            mfs=AK8963_BIT_16,
            mode=AK8963_MODE_C100HZ)

        self.bmp280 = bmp280.BMP280(i2c_addr=bmp280.I2C_ADDRESS_VCC,  # 0x77 address
                                    i2c_dev=SMBus(1))

        self.mpu.configure()  # Apply the settings to the registers.

        all_data_labels = self.mpu.getAllDataLabels()
        self.mpu_filtered_data_labels = self.__mpu_filter_redundant_data__(all_data_labels)
        self.bmp_data_labels = ["temperature2", "pressure"]

    def __mpu_filter_redundant_data__(self, data_array):
        master_acc = data_array[1:4]
        master_gyro = data_array[4:7]
        magnetometer = data_array[13:16]
        temperature = data_array[16:17]
        return master_acc + master_gyro + magnetometer + temperature

    def get_labels(self):
        return self.mpu_filtered_data_labels + self.bmp_data_labels

    def get_data(self):
        try:
            all_data = self.mpu.getAllData()
            filtered_data = self.__mpu_filter_redundant_data__(all_data)
            data = []
            for i in range(len(filtered_data)):
                data.append(filtered_data[i])

            temperature2 = self.bmp280.get_temperature()
            pressure =  self.bmp280.get_pressure()

            data.append(temperature2)
            data.append(pressure)
        except Exception:
            data = [0] * len(self.get_labels())

        return data

