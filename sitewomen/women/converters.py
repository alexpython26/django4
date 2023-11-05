#конвертор для women urls - позволяет создать юрл с 4 цифрами или можно указать свое число

class FourDigitYearConverter:
    regex = "[0-9]{4}"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return "%04d" % value