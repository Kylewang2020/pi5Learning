import threading
import time
import lgpio


def gpio_init(gpiochip):
    '''lgpio 初始化'''
    print("  gpio_init:   gpio_ver=", lgpio.get_module_version())
    # 打开 GPIO 芯片 4 (当前我的 GPIO 芯片的编号 为4)
    chip = lgpio.gpiochip_open(gpiochip)
    print("  gpio_init:   handle =", chip)
    return chip


def gpio_close(chip, pin_in, pin_out):
    '''lgpio 终止'''
    lgpio.gpio_free(chip, pin_in)
    lgpio.gpio_write(chip, pin_out, 0)
    lgpio.gpio_free(chip, pin_out)
    lgpio.gpiochip_close(chip)
    print("  gpio_close:   done")


def get_duty_cycle(angle):
    '''依据角度计算sg90的占空比'''
    speed = 0.002 # 速度约为 0.12 秒/60度，即0.002 秒/度
    if angle>=360:  sg_angle = angle - 360
    elif angle>180: sg_angle = angle-180
    else: sg_angle = angle
    # 角度和脉冲时长的关系:
    #    [[0°, 0.5ms], [45°, 1ms], [90°, 1.5ms], [135°, 2ms], [180°, 2.5ms]]
    duty_cycle = (sg_angle/45.0)*2.5 + 2.5
    wait_time = speed*180+0.2
    return duty_cycle, wait_time


def PWM(chip, pin, angle, frequency=50):
    '''使用 lgpio 库模拟 PWM函数'''
    duty_cycle, wait_time = get_duty_cycle(angle)
    # 计算周期（秒）
    period = 1 / frequency
    high_time = period * (duty_cycle / 100)  # 高电平持续时间
    low_time = period - high_time  # 低电平持续时间
    print("    PWM: 角度:{:>3}; set fps={}; period={:.0f}ms; 占空比={:3.1f}%; high_time={:4.2f}ms".format(
        angle, frequency, period*1000, duty_cycle, high_time*1000))

    try:
        runTime = 0.0
        while True:
            # 输出高电平
            lgpio.gpio_write(chip, pin, 1)
            time.sleep(high_time)
            # 输出低电平
            lgpio.gpio_write(chip, pin, 0)
            time.sleep(low_time)
            runTime += period
            if runTime > wait_time: break
        lgpio.gpio_write(chip, pin, 0)
    except KeyboardInterrupt:
        print("    PWM: 键盘终止 PWM函数退出")


def voice_detect(chip, pin_in, time_span=1):
    '''使用 lgpio 库模拟 PWM函数'''
    try:
        run_time = 0.0
        time_sleep = 0.01
        while True:  # 检查事件是否被设置
            value = lgpio.gpio_read(chip, pin_in)
            if value == 0:
                print(f"    GPIO-{pin_in} 低电平: 检测到声音信号!")
                return True
            time.sleep(time_sleep)
            run_time += time_sleep
            if run_time>=time_span: break
        print(f"    GPIO-{pin_in} 高电平")
        return False
    except Exception as e:
        print("    voice_detect: ", e)


# 主函数
def main():
    # 参数设置 
    pin_in = 12
    pin_out = 18    # pwm 输出gpio 针脚
    gpiochip = 4

    chip = gpio_init(gpiochip)
    # 设置 GPIO 引脚为 输出
    r = lgpio.gpio_claim_output(chip, pin_out)
    print("main: set GPIO-{} to 输出 {}".format(pin_out, "成功" if r>=0 else "失败!"))
    # 设置 GPIO 引脚为 输入
    r = lgpio.gpio_claim_input(chip, pin_in)
    print("main: set GPIO-{} to 输入 {}".format(pin_out, "成功" if r>=0 else "失败!"))

    try:
        for angle in [0, 45, 90, 135, 180, 0]:
            isVoice = voice_detect(chip, pin_in, 2)
            if isVoice:
                PWM(chip, pin_out, angle)
    except KeyboardInterrupt:
        # 设置停止事件，通知所有线程退出
        print("main: 键盘终止 主线程通知所有线程退出...")

    finally:
        gpio_close(chip, pin_in, pin_out)
        print("main: 退出程序")
        
if __name__ == "__main__":
    main()
