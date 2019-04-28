from FLVHelper.TAGHelper.TAG import Tag
from staticData.FLV.TAG import staticTAG
from util import bytesutil
from exception.FLVexception import UnSupportFileFormat,UnSupportAmfValFormat
import struct


class ScriptTag(Tag):
    """
        脚本数据也称元数据metadata，解析起来稍微有点麻烦
        amf0可以查看:
        https://wwwimages2.adobe.com/content/dam/acom/en/devnet/pdf/amf0-file-format-specification.pdf
    """
    numVal = 0
    strVal, lStrVal = "", ""
    objVal = []
    arrVal = {}
    boolVal = False
    nullVal, dateVal = None, None

    def parse(self):
        """解析脚本元meta数据"""
        data = super().getBytes()
        size = len(data)
        while size > 0:
            type = data[0]
            data, size = data[1:], size - 1
            if type == staticTAG.Amf0DataType.FLV_AMF0_NUMBER:
                data, size, self.numVal = self.__parse_number(data, size)
            elif type == staticTAG.Amf0DataType.FLV_AMF0_BOOLEAN:
                data, size, self.boolVal = self.__parse_boolean(data, size)
            elif type == staticTAG.Amf0DataType.FLV_AMF0_STRING:
                data, size, self.strVal = self.__parse_string(data, size)
            elif type == staticTAG.Amf0DataType.FLV_AMF0_NULL:
                data, size, self.nullVal = self.__parse_null(data, size)
            elif type == staticTAG.Amf0DataType.FLV_AMF0_OBJECT:
                data, size, self.objVal = self.__parse_object(data, size)
            elif type == staticTAG.Amf0DataType.FLV_AMF0_DATE:
                data, size, self.dateVal = self.__parse_date(data, size)
            elif type == staticTAG.Amf0DataType.FLV_AMF0_ARRAY:
                data, size, self.arrVal = self.__parse_array(data, size)
            elif type == staticTAG.Amf0DataType.FLV_AMF0_STRICT_ARRAY:
                data, size, self.arrVal = self.__parse_strict_array(data, size)
            elif type == staticTAG.Amf0DataType.FLV_AMF0_LONG_STRING:
                data, size, self.lStrVal = self.__parse_long_string(data, size)
            else:
                raise UnSupportAmfValFormat(type)
        # end of while
        assert size == 0
        return self

    def __parse_number(self, data, size):
        # 利用struct来处理double
        ret = struct.unpack('>d', data[:8])[0]
        return data[8:], size - 8, ret

    def __parse_boolean(self, data, size):
        """解析boolean值"""
        ret = False
        if int(data[0]) != 0:
            ret = True
        return data[1:], size - 1, ret

    def __parse_null(self, data, size):
        """解析null值"""
        return data[1:], size - 1, None

    def __parse_string(self, data, size):
        """解析string值(2字节的长度+N字符串)"""
        offset = bytesutil.bytes2int(data[:2])
        offset += 2
        ret = bytes.decode(data[2:offset])
        return data[offset:], size - offset, str(ret)

    def __parse_long_string(self, data, size):
        """解析string值(4字节的长度+N字符串)"""
        offset = bytesutil.bytes2int(data[:4])
        offset += 4
        ret = bytes.decode(data[4:offset])
        return data[offset:], size - offset, str(ret)

    def __parse_date(self, data, size):
        """解析data值(2字节的时区+8字节的时间戳),返回一个dict"""
        zone = struct.unpack('>d', data[0:2])[0]
        time = struct.unpack('>d', data[2:10])[0]
        return data[10:], size - 10, {"zone": zone, "time": time}

    def __parse_array(self, data, size):
        """ecma解析,实际是map数据"""
        arrLen = bytesutil.bytes2int(data[:4])
        arrVal = None
        data, size, arrVal = self.__parse_object(data[4:], size - 4)
        return data, size, {"len": arrLen, "val": arrVal}

    def __parse_strict_array(self, data, size):
        """strict解析array,strict数组是没有key的"""
        alen = bytesutil.bytes2int(data[:4])
        ret = []
        tmp = None
        data, size = data[4:], size - 4
        while size > 0:
            size -= 1
            if data[0] == staticTAG.Amf0DataType.FLV_AMF0_END_OF_OBJECT:
                data = data[1:]
                break
            elif data[0] == staticTAG.Amf0DataType.FLV_AMF0_NUMBER:
                data, size, tmp = self.__parse_number(data[1:], size)
                ret.append(tmp)
            elif data[0] == staticTAG.Amf0DataType.FLV_AMF0_BOOLEAN:
                data, size, tmp = self.__parse_boolean(data[1:], size)
                ret.append(tmp)
            elif data[0] == staticTAG.Amf0DataType.FLV_AMF0_STRING:
                data, size, tmp = self.__parse_string(data[1:], size)
                ret.append(tmp)
            elif data[0] == staticTAG.Amf0DataType.FLV_AMF0_NULL:
                data, size, tmp = self.__parse_null(data[1:], size)
                ret.append(tmp)
            elif data[0] == staticTAG.Amf0DataType.FLV_AMF0_OBJECT:
                data, size, tmp = self.__parse_object(data[1:], size)
                ret.append(tmp)
            elif data[0] == staticTAG.Amf0DataType.FLV_AMF0_DATE:
                data, size, tmp = self.__parse_date(data[1:], size)
                ret.append(tmp)
            elif data[0] == staticTAG.Amf0DataType.FLV_AMF0_ARRAY:
                data, size, tmp = self.__parse_array(data[1:], size)
                ret.append(tmp)
            elif data[0] == staticTAG.Amf0DataType.FLV_AMF0_STRICT_ARRAY:
                data, size, tmp = self.__parse_strict_array(data[1:], size)
                ret.append(tmp)
            elif data[0] == staticTAG.Amf0DataType.FLV_AMF0_LONG_STRING:
                data, size, tmp = self.__parse_long_string(data[1:], size)
                ret.append(tmp)
        return data, size, ret

    def __parse_object(self, data, size):
        """解析object信息，object由一组[key+value],其中value可以是object来嵌套使用"""
        ret = dict()
        while size > 0:
            if data[0] == staticTAG.Amf0DataType.FLV_AMF0_END_OF_OBJECT:
                data = data[1:]
                size -= 1
                break
            # 获取key的长度
            keyLen = bytesutil.bytes2int(data[:2])
            keyLen += 2
            keyVal = bytes.decode(data[2:keyLen])
            data, size = data[keyLen:], size - keyLen - 1
            # 判断object-value类型
            if data[0] == staticTAG.Amf0DataType.FLV_AMF0_NUMBER:
                data, size, ret[keyVal] = self.__parse_number(data[1:], size)
            elif data[0] == staticTAG.Amf0DataType.FLV_AMF0_BOOLEAN:
                data, size, ret[keyVal] = self.__parse_boolean(data[1:], size)
            elif data[0] == staticTAG.Amf0DataType.FLV_AMF0_STRING:
                data, size, ret[keyVal] = self.__parse_string(data[1:], size)
            elif data[0] == staticTAG.Amf0DataType.FLV_AMF0_NULL:
                data, size, ret[keyVal] = self.__parse_null(data[1:], size)
            elif data[0] == staticTAG.Amf0DataType.FLV_AMF0_OBJECT:
                data, size, ret[keyVal] = self.__parse_object(data[1:], size)
            elif data[0] == staticTAG.Amf0DataType.FLV_AMF0_DATE:
                data, size, ret[keyVal] = self.__parse_date(data[1:], size)
            elif data[0] == staticTAG.Amf0DataType.FLV_AMF0_ARRAY:
                data, size, ret[keyVal] = self.__parse_array(data[1:], size)
            elif data[0] == staticTAG.Amf0DataType.FLV_AMF0_STRICT_ARRAY:
                data, size, ret[keyVal] = self.__parse_strict_array(data[1:], size)
            elif data[0] == staticTAG.Amf0DataType.FLV_AMF0_LONG_STRING:
                data, size, ret[keyVal] = self.__parse_long_string(data[1:], size)
        return data, size, ret

