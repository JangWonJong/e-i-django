from dataclasses import dataclass
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

@dataclass
class Machine(object):
    num1 : float
    num2 : float
    opcode : str

    @property
    def num1(self) -> float: return self._num1
    @num1.setter
    def num1(self, num1):self._num1 = num1

    @property
    def num2(self) -> float: return self._num2

    @num2.setter
    def num2(self, num2): self._num2 = num2

    @property
    def opcode(self) -> str: return self._opcode

    @opcode.setter
    def opcode(self, opcode): self._opcode = opcode




class Solution:
    #외부에서 주입되는 파라미터 -> payload
    def __init__(self, payload):
        self._num1 = payload._num1
        self._num2 = payload._num2


    @tf.function
    def add(self):
        return tf.add(self._num1, self._num2)

    @tf.function
    def sub(self):
        return tf.subtract(self._num1, self._num2)

    @tf.function
    def mul(self):
        return tf.multiply(self._num1, self._num2)

    @tf.function
    def div(self):
        return tf.divide(self._num1, self._num2)


class UseModel:
    def __init__(self):
        pass

    def calc(self, num1, num2, opcode):
        model = Machine(num1, num2, opcode)
        model.num1 = num1
        model.num2 = num2
        model.opcode = opcode
        result = ''
        solution = Solution(model)
        if opcode == '+':
            result = solution.add()
        elif opcode == '-':
            result = solution.sub()
        elif opcode == '*':
            result = solution.mul()
        elif opcode == '/':
            result = solution.div()
        return result

if __name__ == '__main__':
    num1 = 5
    num2 = 5
    opcode = '*'
    print(UseModel().calc(num1, num2, opcode))


