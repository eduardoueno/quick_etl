from enum import Enum
from pyspark.sql.types import *


class Delay(Enum):
    YEAR = "Y-"
    MONTH = "M-"
    WEAK = "W-"
    DAY = "D-"


class Window(Enum):
    YEAR = "Ano"
    MONTH = "Mes"
    DAY = "Dia"


class DateFormat(Enum):
    YEAR = "yyyy"
    MONTH = "MM"
    DAY = "dd"


class Operator(Enum):
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    GREATER = ">"
    LESS = "<"
    EQUAL = "="


class SparkType(Enum):
    DataType = "DataType"
    NullType = "NullType"
    CharType = "CharType"
    StringType = "StringType"
    VarcharType = "VarcharType"
    BinaryType = "BinaryType"
    BooleanType = "BooleanType"
    DateType = "DateType"
    TimestampType = "TimestampType"
    TimestampNTZType = "TimestampNTZType"
    DecimalType = "DecimalType"
    DoubleType = "DoubleType"
    FloatType = "FloatType"
    ByteType = "ByteType"
    IntegerType = "IntegerType"
    LongType = "LongType"
    DayTimeIntervalType = "DayTimeIntervalType"
    YearMonthIntervalType = "YearMonthIntervalType"
    Row = "Row"
    ShortType = "ShortType"
    ArrayType = "ArrayType"
    MapType = "MapType"
    StructField = "StructField"
    StructType = "StructType"
