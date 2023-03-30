class Servo:

    def __init__(self, channel, id):
        self._channel = channel
        self._id = id
        self._accessor = {}
        self._protocol = channel.protocol(self.PROTOCOL)
        if self.model_number.read() != self.model_number.default:
            raise Exception("Wrong servo connected")
        pass

    def __getattr__(self, key):
        if key in self._accessor:
            return self._accessor[key]
        elif key in self.EEPROM:
            self._accessor[key] = self.EEPROM[key].accessor(self)
            return self._accessor[key]
        elif key in self.RAM:
            self._accessor[key] = self.RAM[key].accessor(self)
            return self._accessor[key]
        raise KeyError(key)

    def read(self, row):
        return self._protocol.read(self, row)

    def write(self, row, value):
        self._protocol.write(self, row, value)
        pass

    pass

class Accessor:

    def __init__(self, row, servo):
        self._row = row
        self._servo = servo
        self.default = self._row.default
        pass

    def read(self):
        return self._servo.read(self._row)

    pass

class RWAccessor(Accessor):

    def write(self, value):
        return self._servo.write(self._row, value)

    pass

class Row:

    def __init__(self, name, address, size, default):
        self.name = name
        self.address = address
        self.size = size
        self.default = default
        pass

    def accessor(self, servo):
        return Accessor(self, servo)
    
    def __repr__(self):
        return (f"{self.__class__.__name__}('{self.name}', {self.address}, "
                f"{self.size}, {self.default})")

    pass

class RWRow(Row):

    def accessor(self, servo):
        return RWAccessor(self, servo)

    pass

class IndirectRow:
    def __init__(self, name, addresses, size):
        self.name = name
        self.addresses = addresses
        self.size = size
        pass

    def accessor(self, channel):
        raise Exception("Implement me")

    pass
