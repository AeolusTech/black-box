import time
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
import bmp280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

mpu = MPU9250(
    address_ak=AK8963_ADDRESS,
    address_mpu_master=MPU9050_ADDRESS_68,  # In 0x68 Address
    address_mpu_slave=None,
    bus=1,
    gfs=GFS_1000,
    afs=AFS_8G,
    mfs=AK8963_BIT_16,
    mode=AK8963_MODE_C100HZ)

mpu.configure()  # Apply the settings to the registers.

# Initialise the BMP280 (0x77 address)
bus = SMBus(1)
bmp280 = bmp280.BMP280(i2c_addr=bmp280.I2C_ADDRESS_VCC, i2c_dev=bus)

while True:

    print("|.....MPU9250 in 0x68 Address.....|")
    print("Accelerometer", mpu.readAccelerometerMaster())
    print("Gyroscope", mpu.readGyroscopeMaster())
    print("Magnetometer", mpu.readMagnetometerMaster())
    print("Temperature", mpu.readTemperatureMaster())
    print("\n")

    print("|.....BMP280 in 0x77 Address.....|")
    print('{:05.2f}*C {:05.2f}hPa'.format(bmp280.get_temperature(),
          bmp280.get_pressure()))
    print("\n")

    time.sleep(1)
