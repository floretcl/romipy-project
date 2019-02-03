#!/usr/bin/python3
# -*- coding:Utf-8 -*-

import smbus
from time import sleep

#__________________QMC5883L_REGISTERS__________________________#

###ADRESSES###
QMC5883L_ADDRESS = 0x0D
QMC5883L_WRITE = 0x1A
QMC5883L_READ = 0x1B

###REGISTERS_LIST###
#READ_DATA_X_Y_Z#
QMC5883L_X_LSB = 0x00
QMC5883L_X_MSB = 0x01
QMC5883L_Y_LSB = 0x02
QMC5883L_Y_MSB = 0x03
QMC5883L_Z_LSB = 0x04
QMC5883L_Z_MSB = 0x05
#READ_STATUS#
QMC5883L_STATUS = 0x06
#READ_TEMP#
QMC5883L_TEMP_LSB = 0x07
QMC5883L_TEMP_MSB = 0x08
#CONFIG#
QMC5883L_CONFIG_A = 0x09
QMC5883L_CONFIG_B = 0x0A
QMC5883L_SET_RESET = 0x0B

###CONFIGA###
#STATUS#
QMC5883L_STATUS_DRDY = 0x01
QMC5883L_STATUS_OVL = 0x02
QMC5883L_STATUS_DOR = 0x04
#MODE#
QMC5883L_MODE_STANDBY = 0x00
QMC5883L_MODE_CONTIN = 0x01
#ODR# OutputDateRate
QMC5883L_ODR_10HZ = 0x00
QMC5883L_ODR_50HZ = 0x04
QMC5883L_ODR_100HZ = 0x08
QMC5883L_ODR_200HZ = 0x0C
#RNG# Range
QMC5883L_RNG_2G = 0x00
QMC5883L_RNG_8G = 0x10
#OSR# OverSampleRatio
QMC5883L_OSR_512 = 0x00
QMC5883L_OSR_256 = 0x40
QMC5883L_OSR_128 = 0x80
QMC5883L_OSR_64 = 0xC0

###CONFIGB###
QMC5883L_INT_N_ENB = 0x01
QMC5883L_ROL_PNT = 0x40
QMC5883L_SOFT_RST = 0x80
###SET-RESET###
QMC5883L_RESET = 0x01

QMC5883L_TEMP_CORR = 47

#______________QMC5883L__CLASS_____________________________________#

bus = smbus.SMBus(1) #I2C1 raspberry 
class I2c_qmc5883l:
    """Classe pour l'utilisation du module qmc5883l avec le
    protocole I2C"""

    def __init__(self):
        """Constructeur de la classe I2c_qmc5883l"""
        self.addr = QMC5883L_ADDRESS
        self._osr = QMC5883L_OSR_512
        self._rng = QMC5883L_RNG_2G
        self._odr = QMC5883L_ODR_200HZ
        self._mode = QMC5883L_MODE_CONTIN
        self._int_n_enb = 0
        self._rol_pnt = 0
        self._soft_rst = 0

        self._status_dor = -1
        self._status_ovl = -1
        self._status_drdy = -1 

        self._magn_x = -1
        self._magn_y = -1
        self._magn_z = -1
        self._temp = -1

        sleep(0.2)
        self.reset()
        

    def __repr__(self):
        """Retourne un affichage des propriétés de l'objet"""
        return "----QMC5883L---- \n\
        --CONFIGURATION-- \n\
        -Adresse: {} \n\
        -Mode: {} \n\
        -Output Data Rate: {}Hz \n\
        -Range: {}G \n\
        -Over Sample Ratio: {} \n\
        -Interrupt Enabling {} \n\
        -Roll-over Pointer {} \n\
        -Soft Reset {} \n\
        --STATUS-- \n\
        -Data Skip: {} \n\
        -Overflow: {} \n\
        -Data Ready: {} \n\
        --TEMP-- \n\
        {}°C \n\
        --MAGNETOMETER-- \n\
        x = {} \n\
        y = {} \n\
        z = {} \n\
        ".format(bin(self.addr), self.mode, self.odr, self.rng, self.osr, self.int_n_enb, self.rol_pnt\
        , self.soft_rst, self.status_dor, self.status_ovl, self.status_drdy, self.temp, self.magn_x\
        , self.magn_y, self.magn_z)

    def reset(self):
        """Méthode qui réinitialise le module qmc5883l"""
        bus.write_byte_data(self.addr, QMC5883L_SET_RESET, QMC5883L_RESET)
        sleep(0.2)
        self.config()
        
    def config(self):
        """Méthode pour envoyer une config au registre configA -> économie/précision"""
        bus.write_byte_data(self.addr, QMC5883L_CONFIG_A, (self.osr|self.rng|self.odr|self.mode))

    def config2(self):
        """Méthode pour envoyer une config au registre configB"""
        bus.write_byte_data(self.addr, QMC5883L_CONFIG_B, (self.soft_rst|self.rol_pnt|self.int_n_enb))

    def data_conv(self, lsb, msb):
        """Méthode qui retourne un binaire 16bits avec deux 8bits, en complément par deux"""
        bin16 = ((msb << 8)|lsb)
        if (bin16 & (1<<15)):
            bin16 -= (1<<16)
        return bin16

    def read_config(self):
        """Méthode pour récupérer la configA -> économie/précision"""
        config_a = bus.read_byte_data(self.addr, QMC5883L_CONFIG_A)
        print("config_a =",bin(config_a))

        if (config_a & QMC5883L_OSR_256) == 64:
            self._osr = 256
        elif (config_a & QMC5883L_OSR_128) == 128:
            self._osr = 128
        elif (config_a & QMC5883L_OSR_64) == 192:
            self._osr = 64
        elif (config_a & QMC5883L_OSR_512) == 0:
            self._osr = 512
        else:
            print("Error with _osr")

        if (config_a & QMC5883L_RNG_8G) == 16:
            self._rng = "8"
        elif (config_a & QMC5883L_RNG_2G) == 0:
            self._rng = "2"
        else:
            print("Error with _rng")

        if (config_a & QMC5883L_ODR_50HZ) == 4:
            self._odr = "50"
        elif (config_a & QMC5883L_ODR_100HZ) == 8:
            self._odr = "100"
        elif (config_a & QMC5883L_ODR_200HZ) == 12:
            self._odr = "200"
        elif (config_a & QMC5883L_ODR_10HZ) == 0:
            self._odr = "10"
        else:
            print("Error with _odr")

        if (config_a & QMC5883L_MODE_CONTIN) == 1:
            self._mode = 1        
        elif (config_a & QMC5883L_MODE_STANDBY) == 0:
            self._mode = 0
        else:
            print("Error with _mode")

    def read_config2(self):
        """Méthode pour récupérer la configB"""
        config_b = bus.read_byte_data(self.addr, QMC5883L_CONFIG_B)
        print("config_b = ",bin(config_b))

        if (config_b & QMC5883L_SOFT_RST) == 128:
            self._soft_rst = 1
        elif (config_b & QMC5883L_SOFT_RST) == 0:
            self._soft_rst = 0
        else:
            print("Error with _soft_rst")

        if (config_b & QMC5883L_ROL_PNT) == 64:
            self._rol_pnt = 1
        elif (config_b & QMC5883L_ROL_PNT) == 0:
            self._rol_pnt = 0
        else:
            print("Error with _rol_pnt")

        if (config_b & QMC5883L_INT_N_ENB) == 1:
            self._int_n_enb = 1
        elif (config_b & QMC5883L_INT_N_ENB) == 0:
            self._int_n_enb = 0
        else:
            print("Error with _soft_rst")
      
    def read_temp(self):
        """Méthode pour récupérer la température"""
        while not self.data_ready:
            sleep(0.1)

        temp_lsb = bus.read_byte_data(self.addr, QMC5883L_TEMP_LSB)
        temp_msb = bus.read_byte_data(self.addr, QMC5883L_TEMP_MSB)
        self._temp = round((int(self.data_conv(temp_lsb, temp_msb))/100) + QMC5883L_TEMP_CORR )
     
    def read_xyz(self):
        """Méthode pour récupérer les valeurs de x y z du magnétomètre"""
        while not self.data_ready:
            sleep(0.1)

        x_lsb = bus.read_byte_data(self.addr, QMC5883L_X_LSB)
        x_msb = bus.read_byte_data(self.addr, QMC5883L_X_MSB)
        self._magn_x = int(self.data_conv(x_lsb, x_msb))

        y_lsb = bus.read_byte_data(self.addr, QMC5883L_Y_LSB)
        y_msb = bus.read_byte_data(self.addr, QMC5883L_Y_MSB)
        self._magn_y = int(self.data_conv(y_lsb, y_msb))

        z_lsb = bus.read_byte_data(self.addr, QMC5883L_Z_LSB)
        z_msb = bus.read_byte_data(self.addr, QMC5883L_Z_MSB)
        self._magn_z = int(self.data_conv(z_lsb, z_msb))
        

    def read_status(self):
        """Méthode pour récupérer les données : DOR, OVL et DRDY"""
        status = bus.read_byte_data(self.addr, QMC5883L_STATUS)

        if (status & QMC5883L_STATUS_DOR) == 4:
            self._status_dor = 1
        elif (status & QMC5883L_STATUS_DOR) == 0:
            self._status_dor = 0
        else:
            print("Error with _status_dor")

        if (status & QMC5883L_STATUS_OVL) == 2:
            self._status_ovl = 1
        elif (status & QMC5883L_STATUS_OVL) == 0:
            self._status_ovl = 0
        else:
            print("Error with _status_ovl")

        if (status & QMC5883L_STATUS_DRDY) == 1:
            self._status_drdy = 1
        elif (status & QMC5883L_STATUS_DRDY) == 0:
            self._status_drdy = 0
        else:
            print("Error with _status_drdy")

    def data_ready(self):
        """Méthode qui actualise STATUS_DRDY et qui retourne vrai ou faux si pret"""
        status = bus.read_byte_data(self.addr, QMC5883L_STATUS)
        data_ready = status & QMC5883L_STATUS_DRDY
        if data_ready == 1:
            self._status_drdy = 1 
        elif data_ready == 0:
            self._status_drdy = 0
        else:
            print("Error with _status_drdy")
        return bool(data_ready)

    #____________#
    def _get_magn_x(self):
        """Méthode qui retourne la dernière valeur de x du magnétomètre"""
        return self._magn_x
    #Property#
    magn_x = property(_get_magn_x)
    #____________#
    #____________#
    def _get_magn_y(self):
        """Méthode qui retourne la dernière valeur de y du magnétomètre"""
        return self._magn_y
    #Property#
    magn_y = property(_get_magn_y)
    #____________#

    #____________#
    def _get_magn_z(self):
        """Méthode qui retourne la dernière valeur de z du magnétomètre"""
        return self._magn_z
    #Property#
    magn_z = property(_get_magn_z)
    #____________#

    #____________#
    def _get_temp(self):
        """Méthode qui retourne la dernière valeur de température"""
        return self._temp
    #Property#
    temp = property(_get_temp)
    #____________#

    #____________#
    def _get_status_dor(self):
        """Méthode qui retourne le dernier status de DOR"""
        return self._status_dor
    #Property#
    status_dor = property(_get_status_dor)
    #____________#

    #____________#
    def _get_status_ovl(self):
        """Méthode qui retourne le dernier status de OVL"""
        return self._status_ovl
    #Property#
    status_ovl = property(_get_status_ovl)
    #____________#

    #____________#
    def _get_status_drdy(self):
        """Méthode qui retourne le dernier status de DRDY"""
        return self._status_drdy
    #Property#
    status_drdy = property(_get_status_drdy)
    #____________#
    
    #____________#
    def _get_osr(self):
        """Méthode qui retourne le paramètre OSR actuel"""
        return self._osr

    def _set_osr(self, new_osr):
        """Méthode pour envoyer un nouveau paramètre OSR"""
        if new_osr == 512:
            self._osr = QMC5883L_OSR_512
        elif new_osr == 256:
            self._osr = QMC5883L_OSR_256
        elif new_osr == 128:
            self._osr = QMC5883L_OSR_128
        elif new_osr == 64:
            self._osr = QMC5883L_OSR_64
        else:
            print("Error with _set_osr(self,new_osr) : input error at new_osr")
        self.config()
    #Property#
    osr = property(_get_osr, _set_osr)
    #____________#


    #____________#
    def _get_rng(self):
        """Méthode qui retourne le paramètre RNG actuel"""
        return self._rng

    def _set_rng(self, new_rng):
        """Méthode pour envoyer un nouveau paramètre RNG"""
        if new_rng == 2:
            self._rng = QMC5883L_RNG_2G
        elif new_rng == 8:
            self._rng = QMC5883L_RNG_8G
        else:
            print("Error with _set_rng(self,new_rng) : input error at new_rng")
        self.config()
    #Property#
    rng = property(_get_rng, _set_rng)
    #____________#
    
    
    #____________#
    def _get_odr(self):
        """Méthode qui retourne le paramètre ODR actuel"""
        return self._odr

    def _set_odr(self, new_odr):
        """Méthode pour envoyer un nouveau paramètre ODR"""
        if new_odr == 10:
            self._odr = QMC5883L_ODR_10HZ
        elif new_odr == 50:
            self._odr = QMC5883L_ODR_50HZ
        elif new_odr == 100:
            self._odr = QMC5883L_ODR_100HZ
        elif new_odr == 200:
            self._odr = QMC5883L_ODR_200HZ
        else:
            print("Error with _set_odr(self,new_odr) : input error at new_odr")
        self.config()
    #Property#
    odr = property(_get_odr, _set_odr)
    #____________#
    
    
    #____________#
    def _get_mode(self):
        """Méthode qui retourne le paramètre MODE actuel"""
        return self._mode

    def _set_mode(self, new_mode):
        """Méthode pour envoyer un nouveau paramètre MODE"""
        if new_mode == 0:
            self._mode = QMC5883L_MODE_STANDBY
        elif new_mode == 1:
            self._mode = QMC5883L_MODE_CONTIN
        else:
            print("Error with _set_mode(self,new_mode) : input error at new_MODE")
            self.config()
    #Property#
    mode = property(_get_mode, _set_mode)
    #____________#

    #____________#
    def _get_soft_rst(self):
        """Méthode qui retourne le paramètre Soft_Reset"""
        return self._soft_rst

    def _set_soft_rst(self, new_val):
        """Méthode pour changer le réglage de Soft_reset"""
        if new_val == 0:
            self._soft_rst = 0
        elif new_val == 1:
            self._soft_rst = QMC5883L_SOFT_RST
        else:
            print("Error with _set_soft_rst(self,new_val) : input error at new_val")
            self.config2()
    #Property#
    soft_rst = property(_get_soft_rst, _set_soft_rst)
    #____________#

    #____________#
    def _get_rol_pnt(self):
        """Méthode qui retourne le paramètre roll_pointer"""
        return self._rol_pnt

    def _set_rol_pnt(self, new_val):
        """Méthode pour changer le réglage de roll_pointer"""
        if new_val == 0:
            self._rol_pnt = 0
        elif new_val == 1:
            self._rol_pnt = QMC5883L_ROL_PNT
        else:
            print("Error with _set_rol_pnt(self,new_val) : input error at new_val")
            self.config2()
    #Property#
    rol_pnt = property(_get_rol_pnt, _set_rol_pnt)
    #____________#

    #____________#
    def _get_int_n_enb(self):
        """Méthode qui retourne le paramètre "interruptor disabler" (dataready) """
        return self._int_n_enb

    def _set_int_n_enb(self, new_val):
        """Méthode pour changer le réglage de "interruptor disabler" (dataready)"""
        if new_val == 0:
            self._int_n_enb = 0
        elif new_val == 1:
            self._int_n_enb = QMC5883L_INT_N_ENB
        else:
            print("Error with _set_int_n_enb(self,new_val) : input error at new_val")
            self.config2()
    #Property#
    int_n_enb = property(_get_int_n_enb, _set_int_n_enb)
    #____________#
    
