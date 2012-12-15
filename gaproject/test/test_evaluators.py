
import array
from gaproject.tools.adjacent import checkIfValidAdjacent


def test_validAdjToPath():
    a = array.array('i', [
        19, 59, 99, 90, 92, 54, 100, 66, 9, 55, 5, 111, 112, 39, 36,
         89, 23, 20, 21, 38, 69, 105, 22, 103, 129, 95, 85, 16, 123,
          12, 0, 117, 76, 121, 18, 80, 86, 108, 41, 58, 82, 11, 49,
          104, 52, 61, 65, 42, 24, 48, 83, 27, 67, 28, 37, 57, 87,
          84, 47, 96, 60, 63, 88, 94, 34, 32, 98, 122, 109, 53, 10,
          45, 126, 7, 2, 33, 101, 107, 73, 97, 119, 77, 74, 124, 120,
          8, 114, 31, 106, 81, 50, 91, 79, 44, 127, 17, 130, 64, 46,
          25, 40, 1, 78, 6, 56, 3, 128, 26, 29, 113, 62, 70, 110, 30,
          75, 43, 118, 15, 93, 51, 4, 71, 68, 116, 115, 125, 13, 72,
          35, 102, 14
          ])

    assert not checkIfValidAdjacent(a)

