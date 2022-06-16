#!/usr/bin/python3
"""
Copyright © 2022 cyb_cqu. All rights reserved.

@file polynomial_ cubic.py
@date: 23:25:30, June 15, 2022
"""

import numpy as np
import matplotlib.pyplot as plt

class StateCubicPolynomial:
    """
    定义三次多项式使用的类对象状态变量（类似c语言结构体）
    t：时间
    q：位置
    v:速度
    a:加速度
    """
    def __init__(self,t = 0.0,q = 0.0,v = 0.0):
        self.t = t
        self.q = q
        self.v = v
        self.a = 0.0

    def PrintState(self):
        """
        打印类对象状态量
        :return:
        """
        print(self.t, end="  ")
        print(self.q, end="  ")
        print(self.v)

class CoefficientsCubicPolynomial:
    """
       定义三次多项式系数：a_0、a_1,a_2,a_3
    """
    def __ini__(self):
        self.a_0 = 0
        self.a_1 = 0
        self.a_2 = 0
        self.a_3 = 0

class CubicPolynomial:
    """
    三次多项式系数及函数值求解
    其中三次多项式为：q_t = a_0 + a_1 * (t - t_0) + a_2 * (t - t_0)**2 + a_3 * (t - t_0)**3
    """
    def __init__(self, state_0 = StateCubicPolynomial(0.0,0.0,0.0),state_f = StateCubicPolynomial(0.0,0.0,0.0)):
        self.coefficients = CoefficientsCubicPolynomial()
        self.coefficients = self.CalcuCoefficients(state_0,state_f)

    def CalcuCoefficients(self, state_0 = StateCubicPolynomial(0.0,0.0,0.0),state_f = StateCubicPolynomial(0.0,0.0,0.0)):
        """
        三次多项式系数及函数值求解函数
        :param state_0: class StateCubicPolynomial 三次多项式求解的初始条件
        :param state_f: class StateCubicPolynomial 三次多项式求解的末端条件
        :return: class CoefficientsCubicPolynomial 类型的三次多项式系数
        """
        h = state_f.q - state_0.q
        T = state_f.t - state_0.t
        Coefficients = CoefficientsCubicPolynomial()
        Coefficients.a_0 = state_0.q
        Coefficients.a_1 = state_0.v
        Coefficients.a_2 = (3*h - (state_f.v + 2*state_0.v)*T)/(T*T)
        Coefficients.a_3 = (-2 * h + (state_f.v + state_0.v) * T) / (T **3)
        return Coefficients

    def PrintCoefficients(self):
        """
        打印三次多项式系数 a_0,a_1,a_2,a_3,
        :return:
        """
        print(self.coefficients.a_0, end="  ")
        print(self.coefficients.a_1, end="  ")
        print(self.coefficients.a_2, end="  ")
        print(self.coefficients.a_3)

    def CalcuCubicPolynomial(self,coefficients = CoefficientsCubicPolynomial(),t = 0.0,t_0 = 0.0):
        """
        三次多项式位置、速度和加速度状态量求解
        :param coefficients: class CoefficientsCubicPolynomial
        :param t: 末端时刻
        :param t_0: 初始时刻
        :return: 返回 t 时刻的 class StateCubicPolynomial 类型对象，包含位置、速度、加速度状态量
        """
        state = StateCubicPolynomial(0.0, 0.0, 0.0)
        state.t = t
        state.q = coefficients.a_0 + coefficients.a_1 * (t - t_0) + coefficients.a_2 * (t - t_0)**2 + coefficients.a_3 * (t - t_0)**3
        state.v = coefficients.a_1 + 2 * coefficients.a_2 * (t -t_0) + 3*coefficients.a_3 * (t - t_0)**2
        state.a = 2*coefficients.a_2 + 6 * coefficients.a_3 * (t -t_0)
        return state


if __name__ == "__main__":
    # 实例化并赋初值
    state_0 = StateCubicPolynomial()
    state_0.t = 0
    state_0.q = 0
    state_0.v = 0
    print(state_0.PrintState())
    plt.plot(state_0.t,state_0.q,"ro")

    # 实例化并赋末端值
    state_f = StateCubicPolynomial()
    state_f.t = 5
    state_f.q = 10
    state_f.v = 0
    print(state_f.PrintState())
    plt.plot(state_f.t, state_f.q, "ro")
    # plt.show()

    cubicPolynomial = CubicPolynomial(state_0,state_f)
    cubicPolynomial.PrintCoefficients()

    step = 0.1
    t_list = np.arange(state_0.t,state_f.t + step,step)
    print(t_list)
    q_list = []
    v_list = []
    a_list = []

    # 三次多现实位置、速度和加速度求解
    for t in t_list:
        q_t = cubicPolynomial.CalcuCubicPolynomial(cubicPolynomial.coefficients,t,state_0.t)
        q_list.append(q_t.q)
        v_list.append(q_t.v)
        a_list.append(q_t.a)

    # 设置标题
    plt.suptitle("QuinticPolynomial")

    # 绘制位置曲线
    plt.subplot(311)
    plt.plot(state_0.t, state_0.q, "ro")
    plt.plot(state_f.t, state_f.q, "ro")
    plt.plot(t_list, q_list,"r")
    plt.grid('on')
    plt.ylabel("Position")
    # plt.xlim(t_list[0] - 1, t_list[-1] + 1)

    # 绘制速度曲线
    plt.subplot(312)
    plt.plot(state_0.t, state_0.v, "ro")
    plt.plot(state_f.t, state_f.v, "ro")
    plt.plot(t_list, v_list,"g")
    plt.ylabel("Velocity")
    plt.grid('on')

    # 绘制加速度曲线
    plt.subplot(313)
    plt.plot(state_0.t, state_0.a, "ro")
    plt.plot(state_f.t, state_f.a, "ro")
    plt.plot(t_list, a_list,"b")
    plt.ylabel("Acceleration")
    plt.grid('on')

    plt.xlabel("time")
    plt.show()



